# UltraBar widget format, version 1 (draft)

A shared format for widgets that any UltraBar X client can render: Deckhand on macOS, the Windows client, and whatever comes next. One widget package, drawn the same everywhere. Status: **draft for review**; comments as `> TDI:` or `> DNC:` lines under the paragraph they concern.

## 1. What a widget is

A widget is a small web page that draws one card. A client loads it in an offscreen web view at an exact pixel size, gives it data, and takes a picture of it (a *snapshot*), or keeps it running on a display that has its own web runtime (*live*). Widgets use standard HTML, CSS, JavaScript and Canvas/SVG only, plus the one object in section 4. Nothing renderer-specific: no WKWebView, WebView2 or Android WebView APIs, no Node, no file system.

## 2. Package

A folder (or a `.zip` of it) with at least:

```
manifest.json
index.html          (the entry point named in the manifest)
...                 (scripts, styles, fonts, images; all local, relative paths)
```

Fonts and images ship inside the package. A widget that loads anything from the network must declare the host (section 3, `network`).

## 3. manifest.json

```json
{
  "format": 1,
  "id": "com.example.weather-pro",
  "name": "Weather Pro",
  "version": "1.0.0",
  "author": "Name <email or URL>",
  "license": "MIT",
  "description": "One sentence for the store.",
  "entry": "index.html",
  "targets": [
    { "surface": "vivocube", "width": 240, "height": 240 },
    { "surface": "corebar-cover", "width": 480, "height": 480 }
  ],
  "mode": "snapshot",
  "refreshSeconds": 600,
  "data": ["clock", "weather"],
  "network": [],
  "settings": [
    { "key": "units", "type": "choice", "label": "Units", "options": ["metric", "imperial"], "default": "metric" }
  ]
}
```

| Field | Rule |
|---|---|
| `format` | `1` for this spec. Clients refuse higher numbers they do not know. |
| `id` | Reverse-DNS, lowercase, unique in a marketplace. Never reused for a different widget. |
| `version` | Semantic version. A client updates when the marketplace has a higher one. |
| `targets` | The surfaces and pixel sizes the widget can draw. The client picks one and renders at exactly that size, `devicePixelRatio` 1. Known surfaces: `vivocube` (240×240), `corebar-cover` (the TIME card cover). More can be added without a new format number. |
| `mode` | `snapshot`: the picture stays valid for `refreshSeconds` (what a VivoCube can show, since it has no runtime). `live`: the widget may animate; clients that can only send pictures treat it as a snapshot. |
| `refreshSeconds` | How long one snapshot stays correct. Minimum 60. A client may refresh less often (the VivoCube flashes at most every few minutes) but never more often. |
| `data` | The data the widget asks for, from the list in section 5. A client that cannot supply one shows the widget with that key missing, or refuses it with a reason. |
| `network` | Hosts the widget may fetch from itself (for example `["api.open-meteo.com"]`). Empty means no network at all. Clients enforce it. |
| `settings` | User options. Types: `text`, `number` (`min`, `max`), `bool`, `choice` (`options`), `color`. Values arrive in section 4. |

## 4. The runtime contract

Before the page's own scripts run, the client defines one global object:

```js
window.ultrabar = {
  format: 1,
  surface: "vivocube", width: 240, height: 240,   // the chosen target
  mode: "snapshot",
  locale: "nl-NL", timeZone: "Europe/Amsterdam", now: 1793970000000,
  settings: { units: "metric" },
  data: { clock: {...}, weather: {...} },          // only the keys from the manifest
  onData(callback) {},                             // live mode: called with new data
  ready() {}                                       // call when the card is fully drawn
};
```

- The widget draws using `ultrabar.data` and `ultrabar.settings`, then calls `ultrabar.ready()`.
- The client takes the snapshot after `ready()`, or after 5 seconds if it never comes, and then discards the page (snapshot mode).
- Time comes from `ultrabar.now` and `ultrabar.timeZone`, not from the machine clock, so a client can render ahead of time.
- The body background must be opaque: the VivoCube panel is RGB565 without alpha.

## 5. Data keys

| Key | Contents |
|---|---|
| `clock` | `now` (ms), `timeZone`, `clock24h` |
| `weather` | `place`, `temp`, `unit`, `code` (WMO), `isDay`, `humidity`, `wind`, `days[]` (`date`, `code`, `max`, `min`, `rain`) |
| `system` | `cpu`, `mem`, `disk` (percent), `down`, `up` (bytes/s), `host` |
| `nowPlaying` | `playing`, `title`, `artist`, `album`, `art` (data URL or null) |
| `calendar` | `days[]` with `name`, `date`, `events[]` (`title`, `time`, `allDay`, `color`, `past`) |
| `location` | `lat`, `lon`, `place` |

Field names follow what Deckhand already serves to its bar apps (`/weather/data.json` and friends), so existing pages map onto widgets without a translation layer. New keys are added to this table by agreement; a client ignores keys it does not know.

## 6. Marketplace entry

A marketplace lists widgets in one JSON index:

```json
{ "id": "com.example.weather-pro", "kind": "widget", "name": "Weather Pro", "version": "1.0.0",
  "format": 1, "targets": ["vivocube"], "author": "…", "license": "MIT",
  "download": "https://…/weather-pro-1.0.0.zip", "sha256": "…", "source": "https://github.com/…" }
```

Clients check `sha256` before installing and refuse a `format` they do not support.

## 7. Open questions

- Should `live` widgets on the CoreBar run inside a bar app's WebView (the bar has one), or stay a Mac/PC-side thing?
- Tap handling on the cube (`dataConfig`): out of scope for format 1, or a `tap` field now?
- Signing of packages beyond `sha256`.
