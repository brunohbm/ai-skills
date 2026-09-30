#!/usr/bin/env python3
"""Anime lookup helper for the anime-search skill. Standard library only.

Every command prints JSON to stdout. Each provider is queried independently:
a failure is reported under "errors" and never hides data from the others.

  search   "<title>" [--limit 5]                 candidates from AniList (Kitsu as fallback)
  ids      --anilist ID | --mal ID | --kitsu ID  cross-provider IDs + pt-BR title (Kitsu)
  episodes --anilist ID | --mal ID | --kitsu ID  [--from N] [--to M] [--source all|kitsu|jikan] [--full]
  episode  --anilist ID | --mal ID | --kitsu ID  --number N
  airing   --anilist ID                          next episode + upcoming schedule + streaming links
  filler   "<show name or AnimeFillerList slug>" [--number N | --from N --to M]
  wiki     search "<query>" [--api URL]
  wiki     episodes "<page title>" [--number N] [--api URL]

Responses are cached for 24 h in ~/.cache/anime-search (airing: 1 h). Use --no-cache to bypass.
"""
import argparse
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

UA = "anime-search-skill/1.0 (personal research assistant)"
ANILIST = "https://graphql.anilist.co"
KITSU = "https://kitsu.app/api/edge"
JIKAN = "https://api.jikan.moe/v4"
AFL = "https://www.animefillerlist.com"
WIKI_PT = "https://pt.wikipedia.org/w/api.php"

# Minimum seconds between requests to the same host (published limits or robots.txt).
MIN_INTERVAL = {
    "graphql.anilist.co": 2.1,        # 90/min nominal, currently degraded to 30/min
    "api.jikan.moe": 1.1,             # 3/s and 60/min
    "kitsu.app": 0.5,                 # no published limit; stay polite
    "www.animefillerlist.com": 10.0,  # robots.txt Crawl-delay: 10
}
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "anime-search")
USE_CACHE = True
_last_call = {}
BRT = timezone(timedelta(hours=-3))


class FetchError(Exception):
    pass


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _cache_path(key):
    return os.path.join(CACHE_DIR, hashlib.sha1(key.encode("utf-8")).hexdigest() + ".json")


def fetch(url, body=None, ttl=86400, as_json=True):
    """GET (or POST JSON when body is given) with cache, per-host pacing and retries."""
    key = url + "\n" + (json.dumps(body, sort_keys=True) if body else "")
    path = _cache_path(key)
    if USE_CACHE and ttl and os.path.exists(path) and time.time() - os.path.getmtime(path) < ttl:
        with open(path, encoding="utf-8") as f:
            return json.load(f)["payload"]

    host = urllib.parse.urlparse(url).hostname
    accept = "application/vnd.api+json" if host == "kitsu.app" else "application/json"  # Kitsu answers 406 otherwise
    headers = {"User-Agent": UA, "Accept": accept if as_json else "text/html"}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    last_err = None
    for attempt in range(4):
        wait = MIN_INTERVAL.get(host, 0.3) - (time.time() - _last_call.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        _last_call[host] = time.time()
        try:
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=25) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
            payload = json.loads(raw) if as_json else raw
            if USE_CACHE and ttl:
                os.makedirs(CACHE_DIR, exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    json.dump({"url": url, "payload": payload}, f, ensure_ascii=False)
            return payload
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code} from {host}"
            if e.code == 429 or e.code >= 500:
                retry_after = e.headers.get("Retry-After")
                delay = float(retry_after) if retry_after and retry_after.isdigit() else 2 ** (attempt + 1)
                time.sleep(min(delay, 60))
                continue
            raise FetchError(last_err)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            last_err = f"{type(e).__name__} from {host}: {e}"
            time.sleep(2 ** attempt)
    raise FetchError(last_err or f"failed: {url}")


def clip(text, n):
    if not text:
        return text
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def strip_html(text):
    if not text:
        return text
    return html.unescape(re.sub(r"<[^>]+>", " ", text)).strip()


# ---------------------------------------------------------------- AniList

SEARCH_Q = """query($s:String,$n:Int){Page(perPage:$n){media(search:$s,type:ANIME,sort:SEARCH_MATCH){
 id idMal format status season seasonYear episodes duration siteUrl
 title{romaji english native} synonyms
 relations{edges{relationType node{id idMal type format seasonYear title{romaji}}}}}}}"""

MEDIA_Q = """query($id:Int){Media(id:$id,type:ANIME){
 id idMal format status seasonYear episodes siteUrl title{romaji english native}
 nextAiringEpisode{episode airingAt}
 airingSchedule(notYetAired:true,perPage:5){nodes{episode airingAt}}
 streamingEpisodes{title url site}
 externalLinks{site url language type}}}"""


def anilist(query, variables, ttl=86400):
    res = fetch(ANILIST, {"query": query, "variables": variables}, ttl=ttl)
    if res.get("errors"):
        raise FetchError("AniList: " + "; ".join(e.get("message", "?") for e in res["errors"]))
    return res["data"]


def anilist_media(aid, ttl=86400):
    return anilist(MEDIA_Q, {"id": int(aid)}, ttl=ttl)["Media"]


def ts(epoch):
    d = datetime.fromtimestamp(epoch, timezone.utc)
    return {"utc": d.isoformat(timespec="minutes"), "brasilia": d.astimezone(BRT).isoformat(timespec="minutes")}


# ---------------------------------------------------------------- Kitsu

def kitsu_anime(kid):
    a = fetch(f"{KITSU}/anime/{kid}?fields[anime]=canonicalTitle,titles,subtype,startDate,episodeCount")["data"]
    return a


def kitsu_by_external(site, ext_id):
    q = urllib.parse.urlencode({"filter[externalSite]": site, "filter[externalId]": ext_id, "include": "item"})
    res = fetch(f"{KITSU}/mappings?{q}")
    for item in res.get("included", []):
        if item.get("type") == "anime":
            return int(item["id"])
    return None


def kitsu_mappings(kid):
    res = fetch(f"{KITSU}/anime/{kid}/mappings?page[limit]=20")
    out = {}
    for m in res.get("data", []):
        a = m["attributes"]
        out[a["externalSite"]] = a["externalId"]
    return out


def kitsu_search(q, limit):
    params = urllib.parse.urlencode({
        "filter[text]": q, "page[limit]": min(limit, 20),
        "fields[anime]": "canonicalTitle,titles,subtype,startDate,episodeCount"})
    res = fetch(f"{KITSU}/anime?{params}")
    return [{
        "kitsu_id": a["id"], "title": a["attributes"]["canonicalTitle"],
        "titles": a["attributes"].get("titles"), "format": a["attributes"].get("subtype"),
        "start_date": a["attributes"].get("startDate"), "episodes": a["attributes"].get("episodeCount"),
        "url": f"https://kitsu.app/anime/{a['id']}"} for a in res.get("data", [])]


def kitsu_episodes(kid, start, end, full):
    fields = "number,seasonNumber,titles,canonicalTitle,synopsis,airdate,length"
    offset = max(start - 1, 0)
    out = []
    while True:
        q = urllib.parse.urlencode({"sort": "number", "page[limit]": 20, "page[offset]": offset,
                                    "fields[episodes]": fields})
        res = fetch(f"{KITSU}/anime/{kid}/episodes?{q}")
        data = res.get("data", [])
        for e in data:
            a = e["attributes"]
            n = a.get("number")
            if n is None or n < start:
                continue
            if n > end:
                return out
            syn = a.get("synopsis") or a.get("description")
            out.append({"number": n, "season": a.get("seasonNumber"),
                        "title": a.get("canonicalTitle"), "titles": a.get("titles"),
                        "airdate": a.get("airdate"), "minutes": a.get("length"),
                        "synopsis": syn if full else clip(syn, 220)})
        if not data or "next" not in res.get("links", {}):
            return out
        offset += 20


# ---------------------------------------------------------------- Jikan

def jikan_episodes(mal, start, end):
    out = []
    page = (max(start, 1) - 1) // 100 + 1
    while True:
        res = fetch(f"{JIKAN}/anime/{mal}/episodes?page={page}")
        for e in res.get("data", []):
            n = e.get("mal_id")
            if n < start:
                continue
            if n > end:
                return out
            out.append({"number": n, "title": e.get("title"), "title_romaji": (e.get("title_romanji") or "").strip() or None,
                        "title_japanese": e.get("title_japanese"), "aired": (e.get("aired") or "")[:10] or None,
                        "filler": e.get("filler"), "recap": e.get("recap"), "url": e.get("url")})
        if not res.get("pagination", {}).get("has_next_page"):
            return out
        page += 1


def jikan_episode(mal, n):
    e = fetch(f"{JIKAN}/anime/{mal}/episodes/{n}")["data"]
    return {"number": n, "title": e.get("title"), "title_romaji": e.get("title_romanji"),
            "title_japanese": e.get("title_japanese"), "aired": (e.get("aired") or "")[:10] or None,
            "minutes": round(e["duration"] / 60) if e.get("duration") else None,
            "filler": e.get("filler"), "recap": e.get("recap"), "synopsis": e.get("synopsis"), "url": e.get("url")}


# ---------------------------------------------------------------- ID resolution

def resolve(args, errors):
    """Return {'anilist','mal','kitsu','title','title_pt_br'} using whatever the caller gave."""
    ids = {"anilist": args.anilist, "mal": args.mal, "kitsu": args.kitsu}
    if ids["anilist"] and not ids["mal"]:
        try:
            ids["mal"] = anilist_media(ids["anilist"]).get("idMal")
        except FetchError as e:
            errors["anilist"] = str(e)
    if not ids["kitsu"]:
        for site, key in (("anilist/anime", "anilist"), ("myanimelist/anime", "mal")):
            if ids[key]:
                try:
                    ids["kitsu"] = kitsu_by_external(site, ids[key])
                except FetchError as e:
                    errors["kitsu"] = str(e)
                if ids["kitsu"]:
                    break
    if ids["kitsu"] and not (ids["anilist"] and ids["mal"]):
        try:
            m = kitsu_mappings(ids["kitsu"])
            ids["anilist"] = ids["anilist"] or m.get("anilist/anime")
            ids["mal"] = ids["mal"] or m.get("myanimelist/anime")
        except FetchError as e:
            errors["kitsu"] = str(e)
    if ids["kitsu"]:
        try:
            a = kitsu_anime(ids["kitsu"])["attributes"]
            ids["title"] = a.get("canonicalTitle")
            ids["title_pt_br"] = (a.get("titles") or {}).get("pt_br")
            ids["kitsu_episode_count"] = a.get("episodeCount")
        except FetchError as e:
            errors["kitsu"] = str(e)
    ids["links"] = {
        "anilist": f"https://anilist.co/anime/{ids['anilist']}" if ids["anilist"] else None,
        "mal": f"https://myanimelist.net/anime/{ids['mal']}" if ids["mal"] else None,
        "kitsu": f"https://kitsu.app/anime/{ids['kitsu']}" if ids["kitsu"] else None,
    }
    return ids


# ---------------------------------------------------------------- commands

def cmd_search(a):
    errors, out = {}, {"query": a.query, "retrieved_at": now_iso()}
    try:
        media = anilist(SEARCH_Q, {"s": a.query, "n": a.limit})["Page"]["media"]
        out["candidates"] = [{
            "anilist_id": m["id"], "mal_id": m.get("idMal"), "format": m.get("format"),
            "status": m.get("status"), "year": m.get("seasonYear"), "season": m.get("season"),
            "episodes": m.get("episodes"), "title": m["title"], "synonyms": (m.get("synonyms") or [])[:12],
            "url": m.get("siteUrl"),
            "related": [{"relation": e["relationType"], "anilist_id": e["node"]["id"], "format": e["node"]["format"],
                         "year": e["node"].get("seasonYear"), "title": e["node"]["title"]["romaji"]}
                        for e in m["relations"]["edges"] if e["node"].get("type") == "ANIME"][:10],
        } for m in media]
        out["source"] = "AniList"
    except FetchError as e:
        errors["anilist"] = str(e)
    if not out.get("candidates"):
        try:
            out["candidates"] = kitsu_search(a.query, a.limit)
            out["source"] = "Kitsu"
        except FetchError as e:
            errors["kitsu"] = str(e)
    out["errors"] = errors
    return out


def cmd_ids(a):
    errors = {}
    ids = resolve(a, errors)
    return {"ids": ids, "retrieved_at": now_iso(), "errors": errors}


def cmd_episodes(a):
    errors = {}
    ids = resolve(a, errors)
    start = a.start or 1
    end = a.end or (start + a.limit - 1)
    out = {"ids": ids, "range": [start, end], "retrieved_at": now_iso()}
    if a.source in ("all", "kitsu") and ids.get("kitsu"):
        try:
            out["kitsu"] = kitsu_episodes(ids["kitsu"], start, end, a.full)
        except FetchError as e:
            errors["kitsu"] = str(e)
    if a.source in ("all", "jikan") and ids.get("mal"):
        try:
            out["jikan"] = jikan_episodes(ids["mal"], start, end)
        except FetchError as e:
            errors["jikan"] = str(e)
    out["errors"] = errors
    out["note"] = ("Jikan list has no synopses (use `episode` for one). Kitsu synopses are clipped "
                   "unless --full. Numbering may differ between sources; compare titles and dates.")
    return out


def cmd_episode(a):
    errors = {}
    ids = resolve(a, errors)
    n = a.number
    out = {"ids": ids, "number": n, "retrieved_at": now_iso()}
    if ids.get("kitsu"):
        try:
            eps = kitsu_episodes(ids["kitsu"], n, n, True)
            out["kitsu"] = eps[0] if eps else None
        except FetchError as e:
            errors["kitsu"] = str(e)
    if ids.get("mal"):
        try:
            out["jikan"] = jikan_episode(ids["mal"], n)
        except FetchError as e:
            errors["jikan"] = str(e)
    if ids.get("anilist"):
        try:
            for s in anilist_media(ids["anilist"]).get("streamingEpisodes") or []:
                m = re.match(r"Episode\s+(\d+)\s*-\s*(.*)", s.get("title") or "")
                if m and int(m.group(1)) == n:
                    out["streaming"] = {"site": s["site"], "title": m.group(2), "url": s["url"]}
                    break
        except FetchError as e:
            errors["anilist"] = str(e)
    out["errors"] = errors
    return out


def cmd_airing(a):
    errors, out = {}, {"retrieved_at": now_iso()}
    try:
        m = anilist_media(a.anilist, ttl=3600)
        out.update({
            "anilist_id": m["id"], "title": m["title"], "status": m.get("status"), "episodes": m.get("episodes"),
            "next": ({"episode": m["nextAiringEpisode"]["episode"], **ts(m["nextAiringEpisode"]["airingAt"])}
                     if m.get("nextAiringEpisode") else None),
            "upcoming": [{"episode": x["episode"], **ts(x["airingAt"])} for x in m["airingSchedule"]["nodes"]],
            "streaming_links": [{"site": x["site"], "url": x["url"], "language": x.get("language")}
                                for x in m.get("externalLinks") or [] if x.get("type") == "STREAMING"],
            "official_links": [{"site": x["site"], "url": x["url"]}
                               for x in m.get("externalLinks") or [] if x.get("site") == "Official Site"],
            "note": "Times are the original (usually Japanese) broadcast; streaming release can differ by region.",
        })
    except FetchError as e:
        errors["anilist"] = str(e)
    out["errors"] = errors
    return out


def _norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def cmd_filler(a):
    errors, out = {}, {"retrieved_at": now_iso()}
    slug = a.show if re.fullmatch(r"[a-z0-9%\-]+", a.show) else None
    try:
        if not slug:
            shows = re.findall(r'<a href="/shows/([^"]+)">([^<]+)</a>', fetch(f"{AFL}/shows", as_json=False))
            target = _norm(a.show)
            ranked = sorted(shows, key=lambda s: (target not in _norm(s[1]), abs(len(_norm(s[1])) - len(target))))
            if not ranked or target not in _norm(ranked[0][1]):
                out["matched_candidates"] = [{"slug": s, "name": html.unescape(n)} for s, n in ranked[:5]]
                out["errors"] = {"animefillerlist": "no confident match; pick a slug from matched_candidates"}
                return out
            if _norm(ranked[0][1]) != target:
                out["matched_candidates"] = [{"slug": s, "name": html.unescape(n)} for s, n in ranked[:3]]
            slug = ranked[0][0]
        page = fetch(f"{AFL}/shows/{slug}", as_json=False)
        rows = re.findall(r'<tr class="([^"]+?)(?: odd| even)?" id="eps-(\d+)">.*?<td class="Title"><a[^>]*>([^<]*)</a>'
                          r'.*?<td class="Type"><span>([^<]*)</span>.*?<td class="Date">([^<]*)</td>', page, re.S)
        eps = [{"number": int(n), "title": html.unescape(t), "type": ty, "airdate": d} for _, n, t, ty, d in rows]
        if a.number:
            eps = [e for e in eps if e["number"] == a.number]
        elif a.start or a.end:
            eps = [e for e in eps if (a.start or 0) <= e["number"] <= (a.end or 10 ** 6)]
        if a.number or a.start or a.end:
            out["episodes"] = eps
        else:  # whole show: summarise as ranges to keep output small
            ranges = {}
            for e in eps:
                r = ranges.setdefault(e["type"], [])
                if r and r[-1][1] == e["number"] - 1:
                    r[-1][1] = e["number"]
                else:
                    r.append([e["number"], e["number"]])
            out["ranges"] = {k: ", ".join(f"{x}" if x == y else f"{x}-{y}" for x, y in v) for k, v in ranges.items()}
            out["total"] = len(eps)
        out.update({"slug": slug, "source": "AnimeFillerList", "url": f"{AFL}/shows/{slug}"})
    except FetchError as e:
        errors["animefillerlist"] = str(e)
    out["errors"] = errors
    return out


# ---------------------------------------------------------------- MediaWiki (Wikipedia, Fandom)

EP_TEMPLATES = ("lista de episódio", "lista de episódios", "episode list", "japanese episode list")
PARAMS = {
    "number": ("númeroepisódio", "episodenumber", "númerogeral"),
    "number_in_season": ("númeroepisódio2", "episodenumber2"),
    "title": ("título", "title", "englishtitle"),
    "title_native": ("títulonativo", "nativetitle", "kanjititle"),
    "date": ("datatransmissãooriginal", "originalairdate"),
    "synopsis": ("sinopse", "resumobreve", "shortsummary", "resumo"),
}


def _split_top(s, sep="|"):
    parts, depth, cur, i = [], 0, [], 0
    while i < len(s):
        two = s[i:i + 2]
        if two in ("{{", "[["):
            depth += 1; cur.append(two); i += 2; continue
        if two in ("}}", "]]"):
            depth -= 1; cur.append(two); i += 2; continue
        if s[i] == sep and depth == 0:
            parts.append("".join(cur)); cur = []
        else:
            cur.append(s[i])
        i += 1
    parts.append("".join(cur))
    return parts


def _clean_wiki(t):
    t = re.sub(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>", "", t, flags=re.S)
    t = re.sub(r"\{\{\s*(?:start date|dts|data de início)\s*\|\s*(\d{4})\s*\|\s*(\d{1,2})\s*\|\s*(\d{1,2})[^}]*\}\}",
               lambda m: f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}", t, flags=re.I)
    for _ in range(5):
        t = re.sub(r"\{\{[^{}]*\}\}", "", t)
    t = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"<br\s*/?>", " ", t)
    t = re.sub(r"<[^>]+>|'''?", "", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def wiki_episode_blocks(wikitext):
    low = wikitext.lower()
    i = 0
    while True:
        i = low.find("{{", i)
        if i < 0:
            return
        head = low[i + 2:i + 40].lstrip()
        if not head.startswith(EP_TEMPLATES):
            i += 2; continue
        depth, j = 0, i
        while j < len(wikitext):
            if wikitext.startswith("{{", j):
                depth += 1; j += 2
            elif wikitext.startswith("}}", j):
                depth -= 1; j += 2
                if depth == 0:
                    break
            else:
                j += 1
        params = {}
        for part in _split_top(wikitext[i + 2:j - 2])[1:]:
            if "=" in part:
                k, v = part.split("=", 1)
                params[k.strip().lower()] = v
        ep = {}
        for field, keys in PARAMS.items():
            for k in keys:
                if params.get(k, "").strip():
                    ep[field] = _clean_wiki(params[k]); break
        if ep:
            yield ep
        i = j


def cmd_wiki(a):
    api = a.api or WIKI_PT
    errors, out = {}, {"api": api, "retrieved_at": now_iso()}
    try:
        if a.action == "search":
            q = urllib.parse.urlencode({"action": "query", "list": "search", "srsearch": a.text,
                                        "srlimit": 8, "format": "json", "formatversion": 2})
            out["results"] = [{"title": r["title"], "snippet": strip_html(r.get("snippet"))}
                              for r in fetch(f"{api}?{q}")["query"]["search"]]
        else:
            def page_url(title):
                base = api.replace("/w/api.php", "/wiki/").replace("/api.php", "/wiki/")
                return base + urllib.parse.quote(title.replace(" ", "_"))

            def parse(title):
                q = urllib.parse.urlencode({"action": "parse", "page": title, "prop": "wikitext",
                                            "redirects": 1, "format": "json", "formatversion": 2})
                res = fetch(f"{api}?{q}")
                if "error" in res:
                    raise FetchError(res["error"].get("info", "parse error"))
                return res["parse"]["title"], res["parse"]["wikitext"]

            title, text = parse(a.text)
            pages = [(title, text)]
            # Episode lists are often split per season and transcluded as {{:Page}}; follow them.
            for sub in re.findall(r"\{\{:([^{}|]+)\}\}", text)[:10]:
                try:
                    pages.append(parse(sub.strip()))
                except FetchError as e:
                    errors.setdefault("wiki_subpages", []).append(f"{sub}: {e}")
            eps = []
            for t, wt in pages:
                eps += [{**e, "page": t, "url": page_url(t)} for e in wiki_episode_blocks(wt)]
            if a.number is not None:
                num = lambda v: (v or "").strip()  # exact: "3.5" (OVA) must not match 3
                eps = [e for e in eps if str(a.number) in (num(e.get("number")), num(e.get("number_in_season")))]
            out.update({"page": title, "url": page_url(title), "pages_read": [t for t, _ in pages],
                        "episodes": eps})
            if a.number is not None and len(eps) > 1:
                out["note"] = "Same number found on several pages (seasons/OVAs); pick by page and date."
            if not eps:
                out["note"] = "No episode-list templates found; the page may use plain tables or link to season pages."
    except FetchError as e:
        errors["wiki"] = str(e)
    out["errors"] = errors
    return out


# ---------------------------------------------------------------- CLI

def main():
    global USE_CACHE
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--no-cache", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search"); s.add_argument("query"); s.add_argument("--limit", type=int, default=5)

    def id_args(sp):
        sp.add_argument("--anilist", type=int); sp.add_argument("--mal", type=int); sp.add_argument("--kitsu", type=int)

    s = sub.add_parser("ids"); id_args(s)
    s = sub.add_parser("episodes"); id_args(s)
    s.add_argument("--from", dest="start", type=int); s.add_argument("--to", dest="end", type=int)
    s.add_argument("--limit", type=int, default=100)
    s.add_argument("--source", choices=["all", "kitsu", "jikan"], default="all")
    s.add_argument("--full", action="store_true", help="do not clip synopses")
    s = sub.add_parser("episode"); id_args(s); s.add_argument("--number", type=int, required=True)
    s = sub.add_parser("airing"); s.add_argument("--anilist", type=int, required=True)
    s = sub.add_parser("filler"); s.add_argument("show"); s.add_argument("--number", type=int)
    s.add_argument("--from", dest="start", type=int); s.add_argument("--to", dest="end", type=int)
    s = sub.add_parser("wiki"); s.add_argument("action", choices=["search", "episodes"]); s.add_argument("text")
    s.add_argument("--number", type=int); s.add_argument("--api", help="MediaWiki api.php URL (default pt.wikipedia)")

    a = p.parse_args()
    USE_CACHE = not a.no_cache
    if a.cmd in ("ids", "episodes", "episode") and not (a.anilist or a.mal or a.kitsu):
        p.error("give --anilist, --mal or --kitsu")
    handler = {"search": cmd_search, "ids": cmd_ids, "episodes": cmd_episodes, "episode": cmd_episode,
               "airing": cmd_airing, "filler": cmd_filler, "wiki": cmd_wiki}[a.cmd]
    print(json.dumps(handler(a), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
