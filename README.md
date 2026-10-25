# Willemstad Plus

[Willemstad](https://github.com/tingmelvin/willemstad-x) by Melvin Ting (@tingmelvin), with my patches on top. Installs as a separate theme, **Willemstad Plus**, so Obsidian's theme updater never overwrites it.

## Patches

- `patches/tabs.css`: every tab in the main area is an outlined box instead of bare text. Pinned tabs get an accent tint, and the active tab gets a stronger accent outline.

## Layout

| Path | What it is |
| --- | --- |
| `upstream/` | Unmodified `theme.css` and `manifest.json` from tingmelvin/willemstad-x |
| `patches/*.css` | My overrides, appended after upstream in name order |
| `build.sh` | Writes `dist/` and installs it into each vault in `$VAULTS` |
| `update-upstream.sh` | Pulls the latest upstream release, then runs `build.sh` |

```sh
VAULTS="$HOME/Documents/obsidian/personal" ./build.sh            # rebuild after editing a patch
VAULTS="$HOME/Documents/obsidian/personal" ./update-upstream.sh  # take a new Willemstad release
```

Patches only override upstream rules and never edit `upstream/`, so a new upstream release carries them over. If one stops applying, fix the patch file and rebuild.

## License

GPL-3.0, same as upstream. See `LICENSE`.
