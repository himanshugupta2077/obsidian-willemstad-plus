# Willemstad Plus

[Willemstad](https://github.com/tingmelvin/willemstad-x) by Melvin Ting (@tingmelvin), with my patches on top. Installs as a separate theme, **Willemstad Plus**, so Obsidian's theme updater never overwrites it.

## Patches

- `patches/folders.css`: Blue Topaz-style colorful folders. Each top-level folder in the file explorer is an outlined box with a colored left edge, and its subfolders, icons, hover and active note take that color. Works with the Workspace Folder Scope plugin (the scoped folder's subfolders become the boxes).
- `patches/tabs.css`: every tab in the main area is an outlined box instead of bare text. Pinned tabs get an accent tint, and the active tab gets a stronger accent outline.

## Size

Upstream embeds full-coverage fonts, so its `theme.css` is over Obsidian Sync's 5 MB per-file limit and never reaches your other devices. `build.sh` subsets the text fonts (Inter, Manrope, DM Sans, Crimson Pro) to Latin scripts, punctuation and symbols with `tools/subset_fonts.py`, keeping every weight, variable axis and OpenType feature. That brings it to about 4 MB. Characters outside the subset (e.g. Cyrillic or Greek) fall back to a system font. Icon, math and monospace fonts are untouched. The first build creates `.venv` with fonttools and brotli.

## Layout

| Path | What it is |
| --- | --- |
| `upstream/` | Unmodified `theme.css` and `manifest.json` from tingmelvin/willemstad-x |
| `patches/*.css` | My overrides, appended after upstream in name order |
| `build.sh` | Writes `dist/` (with fonts subset to fit Sync) and installs it into each vault in `$VAULTS` |
| `tools/subset_fonts.py` | Subsets the embedded text fonts in a built `theme.css` |
| `update-upstream.sh` | Pulls the latest upstream release, then runs `build.sh` |

```sh
VAULTS="$HOME/Documents/obsidian/personal" ./build.sh            # rebuild after editing a patch
VAULTS="$HOME/Documents/obsidian/personal" ./update-upstream.sh  # take a new Willemstad release
```

Patches only override upstream rules and never edit `upstream/`, so a new upstream release carries them over. If one stops applying, fix the patch file and rebuild.

## License

GPL-3.0, same as upstream. See `LICENSE`.
