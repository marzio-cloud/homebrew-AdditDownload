# AdditDownloader

`AdditDownloader` is a small Python CLI for managing a local registry of downloadable apps and generating a simple window-cask scaffold.

## Commands

- `additdownloader mk <name> <url>` or `additdownloader add <name> <url>` to add an app to the registry
- - `additdownloader dwnd <name>` or `additdownloader download <name>` to download a registered app
  - - `additdownloader window_cask <name>` or `additdownloader install-window <name>` to generate a window-cask file scaffold
   
    - ## Install
   
    - From source:
   
    - ```bash
      python3 addit.py --help
      ```

      If you want an installable command, use the `pyproject.toml` entry point:

      ```bash
      python3 -m pip install .
      ```

      ## Notes

      - Registry data is stored in `registry.json` in the current working directory.
      - - `registry.json` is local runtime state and should not be committed.
        - 
