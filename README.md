# Default Icons

A collection of [Google Material Symbols](https://fonts.google.com/icons), sorted into category folders.

These icons serve as a base for tests and the [WordPress Plugin Icon Library](https://github.com/svgforge/icon-library).

## Categories

| Folder | Description |
|--------|-------------|
| `actions/` | Actions such as Edit, Delete, Check, Download... |
| `communication/` | Communication such as Mail, Link, Globe... |
| `content/` | Content such as Bolt, Article, Cycle... |
| `navigation/` | Navigation such as Home, Search, Arrow... |
| `people/` | People such as Face, Person, Psychology... |
| `status/` | Status such as Clock, Schedule, Info... |

## Build

The build script uses [svgforge-cli](https://github.com/svgforge/svgforge-cli) to generate a symbol sprite (`OUT/symbol/sprite.svg`) from the individual SVG files and starts a local web server to preview the result.

```sh
./build.sh
```

The generated `OUT/` directory is excluded via `.gitignore`.

## License

Apache License 2.0 (icons via Google Fonts)