# OpenBarX marketplace

One index of widgets, bar apps and hotkey packs for the Sanytron UltraBar X, shared by every client that drives the bar: [Deckhand](https://github.com/DeNoronha/UltraWorkspaceMac) on macOS, the Windows client, and anything that comes next. A client reads `index.json`, lists what fits it, checks the `sha256` and installs.

## What is in it

| Kind | What it is | Where the file lives |
|---|---|---|
| `widget` | A card drawn from a small web page, in the shared [widget format](docs/widget-format.md). | `widgets/<id>/` in this repo, released as a zip. |
| `bar-app` | An Android app that runs on the CoreBar itself. | Its own project; Deckhand's are bundled with Deckhand; the vendor's are installed by the bar from the vendor's cloud. |
| `cube-card` | A card Deckhand draws for the VivoCube (built in, native). | Bundled with Deckhand. |
| `screensaver` | A screensaver app for the CoreBar. | The vendor's own download, listed with its checksum. |
| `hotkey-pack` | A set of buttons for a DotKey/KnobKey page: keyboard shortcuts, websites or text. | The vendor's own download. Listed here with its checksum, **not copied**. |

The vendor's apps, screensavers and nine hotkey packs are the vendor's files. This index only describes them and points at the vendor's download; whether they keep serving them is up to the vendor. The packs' keyboard shortcuts are written for Windows (Ctrl, the Windows key); a macOS client has to translate them.

## Files

- `index.json`: the index, format 1.
- `schema/index.schema.json`: JSON Schema for the index.
- `docs/widget-format.md`: the widget format, version 1 (draft, open for review).
- `tools/validate.py`: checks the index; `--fetch` also downloads every item and checks its `sha256`. CI runs it on every push and pull request.
- `widgets/`: widget sources, one folder per widget id.

## Adding something

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: one pull request per item, with its entry in `index.json`, a public source, a licence, and a checksum that matches the download.

## Licence

The index, schema, tools and docs are MIT licensed. Every listed item keeps its own licence, stated in its entry.
