# AdditDownloader

`AdditDownloader` is a small Python CLI for registering local files and copying
them into your current directory.

## Commands

- `additdownloader help` shows the guided help screen
- `additdownloader mkf <file>` registers a local file path
- `additdownloader install <name>` copies a registered file into your directory

Compatibility aliases:

- `additdownloader mk <file>`
- `additdownloader download <name>`
- `additdownloader dwnd <name>`

## Install

From source:

```bash
python3 addit.py help
```

Install as a command:

```bash
python3 -m pip install .
```

Homebrew tap:

```bash
brew tap marzio-cloud/AdditDownloader
brew install additdownloader
```

## Notes

- Registry data is stored in `registry.json` in the current working directory.
- `registry.json` is local runtime state and should not be committed.

