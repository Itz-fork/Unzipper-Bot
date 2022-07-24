# Unzipper
This is where the main stuff happens.

# TOC
- [Directory structure](#directory-structure)
- [Folders](#folders)

## Directory structure
Directory tree structure of [unzipper](/unzipper) folder.

```
├── client
│   ├── caching.py
│   ├── __init__.py
│   ├── patcher.py
│   └── pyro_client.py
├── database
│   ├── cloud.py
│   ├── __init__.py
│   ├── language.py
│   ├── split_arc.py
│   ├── thumbnail.py
│   ├── upload_mode.py
│   └── users.py
├── helpers_nexa
│   ├── buttons.py
│   ├── checks.py
│   ├── __init__.py
│   └── utils.py
├── __init__.py
├── lib
│   ├── backup_tool
│   │   └── __init__.py
│   ├── downloader
│   │   ├── errors.py
│   │   └── __init__.py
│   ├── extractor
│   │   ├── errors.py
│   │   └── __init__.py
│   └── __init__.py
├── localization
│   ├── defaults
│   │   └── buttons.json
│   ├── en
│   │   ├── messages.json
│   │   └── README.md
│   ├── languages.json
│   ├── README.md
│   ├── si
│   │   ├── messages.json
│   │   └── README.md
│   └── templates
│       └── messages-template.json
├── __main__.py
├── modules
│   ├── admin.py
│   ├── callbacks.py
│   ├── extract.py
│   ├── __init__.py
│   ├── settings.py
│   └── user_utils.py
└── README.md
```


## Folders
- [client](client) - Contains the custom client (inherited from `pyrogram.Client` class)
- [database](database) - Contains functions to handle database queries
- [modules](modules) - Contains pyrogram modules
- [lib](lib) - Contains modules (downloader, extractor)
- [helpers_nexa](helpers_nexa) - Contains helper functions, classes
- [localization](localization) - Contains language files and templates