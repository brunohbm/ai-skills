# Browser fallback (Playwright MCP)

Use a browser only for **public pages that have no API** and only when they fill a real gap in the answer. A browser is slower, breaks when layouts change, and is more likely to hit bot checks than an API.

## 1. Pick the tool

Use whichever of these is already available, in this order:

1. **Playwright MCP**: tools named `browser_navigate`, `browser_snapshot`, and so on, often prefixed with `mcp__playwright__`.
2. **Claude in Chrome** (`mcp__claude-in-chrome__*`) or the **built-in browser** (`mcp__Claude_Browser__*`). Load their own skills first. These run with the user's real sign-ins, so read only public pages and never act on the user's account.
3. **WebFetch or `curl`**, for pages that are plain HTML without JavaScript rendering. AnimeFillerList, Wikipedia, and many official sites work this way. Try this before a browser.

If none of these is available and the gap matters, tell the user once:

> To let me read pages that have no API, install Playwright MCP: `claude mcp add playwright npx @playwright/mcp@latest` (needs Node.js 18+). Then restart the session.

Useful flags: `--headless` (no window) and `--isolated` (a fresh in-memory profile with no saved cookies, which keeps research separate from the user's sessions).

## 2. The loop

1. `browser_navigate` to a **known URL**. Do not search inside the site when you can build the URL from an API result.
2. `browser_snapshot` returns the accessibility tree. Read the text from it; it costs far less than screenshots.
3. If the content has not loaded yet, use `browser_wait_for` with a text you expect, and then take another snapshot.
4. For structured blocks such as tables and lists, `browser_evaluate` with a short read-only expression is fine. For example: `[...document.querySelectorAll('h1, [data-t="description"]')].map(e => e.innerText)`.
5. Close the tab when you are done. Record the URL and the time for the source line.

Keep it to a few pages per question. Do not paginate through whole catalogs.

## 3. Site recipes

### Crunchyroll (pt-BR titles and synopses)

- Get the URL from the APIs: `episode` returns `streaming.url` from AniList, `airing` returns `streaming_links`, and Kitsu has `/anime/{id}/streaming-links`.
- Change it to the Brazilian page by inserting `/pt-br/` after the domain:
  `http://www.crunchyroll.com/watch/G14U49MDV/phantoms-of-the-dead` → `https://www.crunchyroll.com/pt-br/watch/G14U49MDV/phantoms-of-the-dead`.
  For a series page: `https://www.crunchyroll.com/pt-br/series/<id>/<slug>`.
- The episode page usually shows the localized title and description without logging in. The video itself needs an account; ignore it.
- Do not use `/search`, which robots.txt disallows. Do not open `/watchlist` or account pages.
- Title or description in Portuguese missing: report it and fall back to the English synopsis with a translation note.

### Official Japanese sites

- Take the URL from AniList `externalLinks` with site "Official Site" (the `airing` output includes it).
- Look for a story page, often `/story/`, `/episode/`, or あらすじ in the menu. Japanese synopses are official; translate them and say so.

### Schedules (LiveChart.me, AnimeSchedule web)

- Use them only when AniList `airing` lacks the date, or to get release times for a region or service. Read the show's page, not the internal API.

### Fandom wikis

- Try the MediaWiki API first (`wiki` command with `--api`). Use the browser only if the API is blocked, and skip ads and pop-ups.

## 4. Stop rules

Stop using that site and switch to another source when:

- a login wall, paywall, or age gate appears;
- a CAPTCHA, a Cloudflare "checking your browser" page, or any other bot challenge appears;
- the site returns 403 or 429, or shows a "too many requests" page;
- the page's terms or robots.txt disallow the path.

Do not retry with a different user-agent, stealth plugins, proxies, or automation-hiding flags. Tell the user briefly which source was unavailable and what you used instead.
