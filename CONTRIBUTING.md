# Contributing

One pull request per item. `python3 tools/validate.py --fetch` must pass (CI runs it).

## A widget

1. Build it to the [widget format](docs/widget-format.md): `manifest.json`, an entry page, everything local, no renderer-specific APIs, opaque background.
2. Put the source in `widgets/<id>/` (the id from the manifest, reverse-DNS).
3. Zip the folder's contents, attach the zip to a GitHub release (yours or this repo's), and add an entry to `index.json` with `kind: "widget"`, `format`, `targets`, `download`, `sha256` and `source`.
4. Test it in at least one client and say which in the pull request.

## A bar app

An entry with `kind: "bar-app"`, a public `source`, a `license` and either a `download` with `sha256` or `distribution: "bundled-with-deckhand"`. Say what the app sends where (its network use) in the pull request.

## A hotkey pack

Your own packs: as a widget, with the pack zip in a release and `actions` and `platform` filled in. Packs from someone else, such as the vendor: link to their download with its `sha256`; do not copy their files into this repo.

## Rules

- Ids never change and are never reused.
- Raise `version` for every change to a download.
- No tracking, no hidden network use: what a widget fetches is declared in its manifest (`network`).
