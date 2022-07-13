# v1.0 - Beta

- Refactored the code
- Rewrote most of the modules
- Better error handling
- Better logging
- Multi-language support
- Changed thumbnail database to [telegra.ph](https://telegra.ph/)
- Added progress bar for direct link downloads
- Added support for multi-part 7z archives (archives ends with file extensions like `.001`, `.002`, etc.)
- Fixed various bugs
    - Fixed RPCErrors:
        - `REPLY_MARKUP_TOO_LONG`
        - `ENTITY_BOUNDS_INVALID`
    - Fixed `RuntimeWarning: coroutine 'x' was never awaited` caused due to calling async function synchronously