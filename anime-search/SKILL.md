---
name: anime-search
description: Looks up anime and episode information by name. It resolves which work the user means (seasons, sequels, films, OVAs, Brazilian titles), then it fetches episode titles, air dates, synopses, filler/canon status, next airing time, and where to watch. API-first (AniList, Kitsu, Jikan, Wikipedia), with a browser (Playwright MCP) only for pages without an API; cites sources and never invents missing data. Use whenever the user asks about an anime or its episodes (what happens in an episode, episode lists, filler, episode or season count, next episode, watch order, where to watch), even if they only name a show and a number ("frieren ep 5"), or wants to build or test an anime-lookup agent. Portuguese triggers include "o que acontece no episódio", "resumo do episódio", "lista de episódios", "é filler", "quando sai o próximo episódio", "quantas temporadas", "ordem para assistir", "onde assistir", and "título em português".
license: MIT
compatibility: Python 3 (standard library only) for scripts/anime_api.py. A browser tool (Playwright MCP, Claude in Chrome, or the built-in browser) is optional and used only as a fallback.
metadata:
  tags: "Anime, Episodes, Research, APIs, Playwright, pt-BR"
  category: "research"
---

# Anime search: find the right work, then the episode

## Goal

Answer questions about an anime or one of its episodes with facts the user can trust. Two steps decide the quality of the answer:

1. **Identify the work.** Titles are not unique. "Frieren season 2", "Shippuden", "the Brotherhood one", and Brazilian release titles each point to a different catalog entry. Most wrong answers come from choosing the wrong entry, not from a bad API.
2. **Treat every field as sourced or missing.** Episode synopses, Portuguese titles, and dates are often absent or disagree between catalogs. Say where each fact came from, and say plainly when no source has it. Never fill a gap from memory and present it as looked up.

## Tools, in order of preference

| Tier | Tool | Use for |
| --- | --- | --- |
| 1 | `scripts/anime_api.py` (bundled) | Everything it covers: search, IDs, episode lists, one episode, next airing, filler, Wikipedia or Fandom episode lists. It handles caching, rate limits, retries, and cross-provider IDs. |
| 2 | Direct HTTP (`curl` or WebFetch) | When Python is not available, or for an endpoint the script does not cover. Recipes are in `references/sources.md`. |
| 3 | Browser (Playwright MCP) | Public pages that render with JavaScript and have no API, such as the Brazilian Crunchyroll page of an episode, an official Japanese site, or a schedule page. See `references/browser.md`. |
| 4 | Web search | Last resort, to discover a page. Then read the page itself; do not answer from search snippets. |

Run the script from the skill's folder (use `python3` if `python` is not on the path):

```bash
python scripts/anime_api.py search "frieren"
python scripts/anime_api.py episode --anilist 154587 --number 5
```

Commands: `search`, `ids`, `episodes`, `episode`, `airing`, `filler`, `wiki search`, `wiki episodes`. Run it with `--help` for the flags. Each prints JSON that reports provider failures under `errors` without hiding what the other providers returned. A provider being down is normal (Jikan often returns 504 when MyAnimeList is unavailable). Continue with the others and mention the gap only if it affects the answer.

## Workflow

### 1. Classify the question

| The user wants | Primary source | Fallback |
| --- | --- | --- |
| Which work, format, year, episode count, related seasons, watch order | `search` (AniList `relations`) | Kitsu search via `search` |
| Episode list with titles and dates | `episodes` (Kitsu + Jikan) | `wiki episodes` |
| What happens in episode N | `episode` (Kitsu synopsis, Jikan synopsis) and, for Portuguese, `wiki episodes ... --number N` | Browser: Crunchyroll pt-BR episode page |
| Filler, canon, recap | `filler` (AnimeFillerList) and the `filler`/`recap` flags from Jikan | `wiki` or a fandom page |
| Next episode, release time | `airing` (AniList) | Browser: an official or streaming schedule |
| Where to watch | `airing` (`streaming_links`) or Kitsu streaming links | Browser: the service's pt-BR page |
| Brazilian title | `ids` (`title_pt_br` from Kitsu) and Wikipedia PT | AniList `synonyms` |
| Dialogue or quotes | See **Dialogue** below | None |

### 2. Resolve the work

- Run `search` with the user's words. **AniList does not match Brazilian titles**, and the script falls back to Kitsu when AniList finds nothing. If the query looks like a Portuguese title and the AniList results look off, run it through Kitsu too (`references/sources.md`).
- Seasons are separate entries in AniList, Kitsu, and MyAnimeList. For "season 2, episode 3", find the season-2 entry through `related` (SEQUEL), then ask for episode 3 of *that* entry. Some long shows (One Piece, Detective Conan) are one entry with continuous numbering.
- Choose without asking when one candidate clearly fits, and state the choice in one line ("I took the 2023 TV series, not the 2026 season 2"). Ask only when two readings are plausible **and** would give different answers. Then offer at most 3–4 options with format, year, and episode count.
- Once resolved, pass the AniList ID (`--anilist`). The script resolves the MyAnimeList and Kitsu IDs through AniList and Kitsu mappings. IDs are specific to each provider and never interchangeable.

### 3. Fetch

- Request only the range you need (`--from/--to`, `--number`). Long shows have more than 1,000 episodes.
- The Jikan episode list carries titles and filler/recap flags but no synopses. `episode` fetches the synopsis for one episode.
- Kitsu synopses often come from Crunchyroll and are in English. The Portuguese Wikipedia sometimes has detailed synopses in pt-BR (`wiki episodes "<list page>" --number N`). Find the page with `wiki search "lista de episódios <title>"`. The script follows the per-season pages that the list page transcludes. It matches both the overall number and the number within a season, so pick the result by `page`.
- A fandom wiki answers through the same MediaWiki API: `--api https://<wiki>.fandom.com/pt/api.php`.
- If sources disagree on numbering, titles, or dates, show the difference and its sources instead of merging them silently.

### 4. Use the browser only to fill a real gap

Open a browser only when the APIs and MediaWiki lack something the user asked for, such as a pt-BR synopsis when Wikipedia has none, or a page that exists only on an official site. Go straight to a known URL: take the Crunchyroll link from `episode` (`streaming`) or from `airing`, and insert `/pt-br/` after the domain. Do not use the site's search, because Crunchyroll's robots.txt disallows `/search`. Follow `references/browser.md`, including its stop rules.

If no browser tool is available and the gap matters, tell the user in one line how to add one (`claude mcp add playwright npx @playwright/mcp@latest`) and answer with what you have.

### 5. Answer

- Write in the user's language. Lead with the answer, not with the process.
- **Header line:** the title the user will recognize (the pt-BR title when one exists, with the original in parentheses the first time), the episode number, the episode title, and the air date.
- **Translation:** if you translate an English synopsis, say so in a few words, such as "(sinopse da Crunchyroll via Kitsu, traduzida)". Keep the translation faithful and do not add events that are not in the source.
- **Spoilers:** answer what was asked. Warn before revealing anything beyond it, such as later episodes or twists of the arc.
- **Missing data:** say what is missing and what you tried ("Nenhuma fonte tem sinopse deste episódio; Kitsu e MyAnimeList só têm o título"). Offer the next step, such as the browser or another episode.
- **Sources:** end with a single line of linked sources, with the date you consulted them.
- Keep synopses short. Quote at most a short passage from any source and link to the rest, because these texts are copyrighted.

Example (Portuguese conversation):

```markdown
**Frieren e a Jornada para o Além (Sousou no Frieren), ep. 5: "Phantoms of the Dead"**, exibido em 06/10/2023

Frieren e Fern investigam aparições de fantasmas em uma vila onde pessoas começaram a desaparecer.
*(sinopse oficial da Crunchyroll via Kitsu, traduzida)*

Onde ver: [Crunchyroll](https://www.crunchyroll.com/pt-br/watch/G14U49MDV/phantoms-of-the-dead)

Fontes: [Kitsu](https://kitsu.app/anime/46474), [AniList](https://anilist.co/anime/154587) (consultados em 30/09/2026)
```

## Boundaries

- **TMDB is excluded.** Its API terms prohibit use with LLM or AI chatbots and interactive query-response systems. Do not use it even though it has pt-BR synopses.
- **No evasion.** Do not use stealth plugins, spoofed fingerprints, proxy rotation, or CAPTCHA solving. Do not log in for the user, and do not work around paywalls, DRM, or Cloudflare challenges. If a site blocks automated access, stop and use another source. Some guides recommend these techniques; they break site terms and are out of scope.
- **Respect published limits.** The script paces each host (AniList 30–90/min, Jikan 3/s and 60/min, AnimeFillerList crawl-delay 10 s) and caches for 24 hours. When you call these services directly, keep the same pace.
- **No streaming or piracy links.** Point only to official services.

### Dialogue

There is no legitimate, open source of full anime transcripts in pt-BR. Do not reconstruct scripts or subtitles, and do not extract subtitles from streaming services. You can:

- describe what a scene is about, from synopses;
- quote a short, well-known line when a source you consulted contains it, citing that source;
- analyze a subtitle file (`.srt`, `.ass`, `.vtt`) that the user already has and gives you.

OpenSubtitles has an API with pt-BR subtitles, but it needs the user's own API key and has small daily download quotas. Its files are user uploads whose licensing varies. Mention it only if the user wants to set it up.

## References

- `references/sources.md`: every provider's endpoints, fields, limits, quirks verified on 2026-09-30, raw `curl` recipes, and the providers left out and why. Read it when the script fails, when you call an API directly, or when the user asks why a source was or was not used.
- `references/browser.md`: setting up Playwright MCP, the navigate → snapshot → extract loop, recipes for each site, and when to stop. Read it before the first browser step.
