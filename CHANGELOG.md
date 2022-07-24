# v1.0

- Refactored the code
- Rewrote most of the modules
- Better logging
- Better error handling
- Multi-language support
- Cache data to reduce database reads
- Added progress bar for direct link downloads
- Added support for multi-part 7z archives (archives ends with file extensions like `.001`, `.002`, etc.)
- Changed thumbnail database to [telegra.ph](https://telegra.ph/)
- Fixed various bugs
    - Fixed RPCErrors:
        - `REPLY_MARKUP_TOO_LONG`
        - `ENTITY_BOUNDS_INVALID`
    - Fixed `RuntimeWarning: coroutine 'x' was never awaited` caused due to calling async function synchronously
    - Fixed saving upload mode in banned users database collection