# Sources: endpoints, limits, quirks

Everything marked **verified** was tested with live requests on 2026-09-30. APIs change, so if a recipe fails, check the provider's docs before assuming the data does not exist.

## Contents

1. [AniList](#anilist): resolve the work, relations, airing, streaming links
2. [Kitsu](#kitsu): episodes with synopses, pt-BR titles, ID mappings
3. [Jikan (MyAnimeList)](#jikan-myanimelist): episode titles, filler/recap flags, synopses
4. [AnimeFillerList](#animefillerlist): canon/filler classification
5. [Wikipedia and Fandom (MediaWiki)](#wikipedia-and-fandom-mediawiki): pt-BR titles and synopses
6. [Optional sources](#optional-sources): AniDB, AnimeSchedule, MAL official, OpenSubtitles
7. [Excluded sources](#excluded-sources) and why

---

## AniList

- **Endpoint:** `POST https://graphql.anilist.co`, with a JSON body `{"query": ..., "variables": ...}`. No authentication for reads.
- **Limit:** 90 requests per minute nominally. **Verified:** the `X-RateLimit-Limit` header currently says **30**. Read `X-RateLimit-Remaining`, and on a 429 wait for `Retry-After`.
- **Best for:** search with candidates, `idMal` (the bridge to Jikan), format, year, episode count, `relations` (SEQUEL, PREQUEL, SIDE_STORY…), `nextAiringEpisode`, `airingSchedule`, `externalLinks` (streaming and official sites), and `streamingEpisodes` (per-episode titles and Crunchyroll URLs for licensed shows).
- **Quirks (verified):**
  - `search:` does **not** match Brazilian titles such as "Frieren e a Jornada para o Além", even though they appear in `synonyms`. Use Kitsu for those.
  - `streamingEpisodes` titles look like `"Episode 5 - Phantoms of the Dead"`. Their numbering follows the streaming service and may be continuous across seasons.
  - `airingAt` is a Unix timestamp for the original (usually Japanese) broadcast, not for the streaming release.
- **Terms:** no mass collection or hoarding, no use as a backup database, no competing services, and commercial use above a threshold requires a license. A personal research assistant querying on demand is within normal use.

```bash
curl -s -X POST https://graphql.anilist.co -H "Content-Type: application/json" \
  -d '{"query":"query($s:String){Page(perPage:5){media(search:$s,type:ANIME){id idMal format seasonYear episodes title{romaji english native} relations{edges{relationType node{id format title{romaji}}}}}}}","variables":{"s":"frieren"}}'
```

## Kitsu

- **Base:** `https://kitsu.app/api/edge` (JSON:API). The site moved from `kitsu.io` to `kitsu.app`. **Verified:** both domains still answer the API, and the script uses `kitsu.app`.
- **Header:** `Accept: application/vnd.api+json`. **Verified:** a plain `application/json` gets **406**.
- **Limit:** none published. Pages hold at most 20 items. Keep requests serial.
- **Best for:**
  - Search with **pt-BR titles** (`titles.pt_br`), which AniList search misses: `GET /anime?filter[text]=<q>`.
  - Episodes with titles, **synopsis**, air date, and season number: `GET /anime/{id}/episodes?sort=number&page[limit]=20&page[offset]=N`. Synopses are often the official Crunchyroll text, in English, ending with "(Source: Crunchyroll)".
  - Cross-IDs: `GET /mappings?filter[externalSite]=anilist/anime&filter[externalId]=<id>&include=item` (also `myanimelist/anime`), or `GET /anime/{id}/mappings`.
  - Streaming links with subtitle and dub languages: `GET /anime/{id}/streaming-links`.
- **Quirks:** each season is its own entry. Episode fields are often empty for older or niche shows. Some filter names changed over time (for example, `mediaId` is deprecated).

```bash
curl -s -H "Accept: application/vnd.api+json" \
  "https://kitsu.app/api/edge/anime?filter%5Btext%5D=frieren&fields%5Banime%5D=canonicalTitle,titles,episodeCount,subtype,startDate"
curl -s -H "Accept: application/vnd.api+json" \
  "https://kitsu.app/api/edge/anime/46474/episodes?sort=number&page%5Blimit%5D=20&fields%5Bepisodes%5D=number,seasonNumber,canonicalTitle,synopsis,airdate"
```

## Jikan (MyAnimeList)

- **Base:** `https://api.jikan.moe/v4`. It is unofficial: it scrapes MyAnimeList pages and caches them for 24 hours. No authentication.
- **Limit:** 3 requests per second and 60 per minute.
- **Endpoints:**
  - `GET /anime?q=<title>` returns candidates.
  - `GET /anime/{mal_id}/episodes?page=N` returns 100 episodes per page, with title, Japanese and romaji titles, air date, and `filler` and `recap` flags. **Verified:** the list has **no synopsis**.
  - `GET /anime/{mal_id}/episodes/{n}` returns one episode, including its synopsis when MyAnimeList has one.
- **Quirks (verified):** it returns **504** whenever MyAnimeList is down or refusing connections. This happened several times during testing, so treat Jikan as best-effort and never as the only source.

## AnimeFillerList

- **Site:** `https://www.animefillerlist.com/shows/<slug>`. There is no API; the page is static HTML, so the script or WebFetch is enough and a browser is not needed.
- **robots.txt:** `Crawl-delay: 10`. Make one request per show and cache it.
- **Markup (verified):** `<tr class="filler odd" id="eps-57">`, with cells `Number`, `Title`, `Type` (Manga Canon, Mixed Canon/Filler, Filler, Anime Canon), and `Date`. The full show list is at `/shows`.
- **Coverage:** mainly long shōnen series, about 370 shows. For a show that is not listed, say so and use Jikan's `filler`/`recap` flags, which are also often empty.

## Wikipedia and Fandom (MediaWiki)

- **API:** `https://pt.wikipedia.org/w/api.php` (or `en.`). Send a descriptive User-Agent.
  - Search: `?action=query&list=search&srsearch=<q>&format=json`
  - Wikitext: `?action=parse&page=<title>&prop=wikitext&redirects=1&format=json&formatversion=2`
- **pt-BR episode templates (verified):** `{{Lista de episódio/sublista|...}}` with `NúmeroEpisódio` (overall), `NúmeroEpisódio2` (within the season), `Título`, `TítuloNativo`, `DataTransmissãoOriginal = {{Data de início|2013|4|7}}`, and `Sinopse`. English Wikipedia uses `{{Episode list|EpisodeNumber=|Title=|OriginalAirDate=|ShortSummary=}}`.
- **Transclusion (verified):** list pages often pull in each season with `{{:Shingeki no Kyojin (1.ª temporada)}}`. The episodes live on those subpages, and `wiki episodes` follows them.
- **Coverage:** uneven. Popular shows sometimes have detailed pt-BR synopses, and many pages list only titles and dates. Content is CC BY-SA, so cite the page.
- **Fandom:** same API at `https://<wiki>.fandom.com/<lang>/api.php` (verified on `onepiece.fandom.com/pt`). Episode pages there have free-form layouts, so read the wikitext and pick out the summary section.

## Optional sources

Use these only when a user needs them and accepts the setup:

- **AniDB HTTP API:** detailed episode data and multilingual titles. It requires a **registered client name**, one request every 2 seconds at most, and heavy caching. Repeating a request on the same day can get the IP banned. For title search, download the daily `anime-titles.xml.gz` dump once per day. Not worth it for on-demand chat use.
- **AnimeSchedule API v3:** release timetables, including English sub and dub times. Requires an account and an application token.
- **MyAnimeList API v2 (official):** needs a client ID. It has series metadata but no per-episode synopses, so Jikan covers more for this skill.
- **OpenSubtitles API:** pt-BR subtitle search. It needs the user's API key and has small daily download quotas, and files are user uploads with varying licenses. See **Dialogue** in SKILL.md.

## Excluded sources

| Source | Why it is excluded |
| --- | --- |
| **TMDB** | Its API terms prohibit use "on or in connection with … interactive query-response system (including large language model (LLM), artificial intelligence … or chatbots)". Verified on 2026-09-30. |
| **Crunchyroll search** | robots.txt disallows `*/search`. Open known series or episode URLs instead; see `browser.md`. There is no public API. |
| **Netflix and other streamers' subtitles** | The content is copyrighted and protected; extracting it is not allowed. |
| **LiveChart.me internal API** | Only unofficial community documentation exists. Open the public page in a browser if needed. |
| **Piracy and aggregator sites** | Not official sources, and links to them must not be given. |
| **Stealth scraping** (playwright-stealth, proxy rotation, fingerprint spoofing) | Evades site controls. Out of scope, whatever other guides recommend. |
