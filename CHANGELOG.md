# v1.0.2
- Added spanish translation (Thanks to [Carlos](https://t.me/Carlitosbby))
- Added support for 301 http responses
- Fixed Attribute errors raised due to new log info message

# v1.0.1
- Updated progress bar
- Temp fix for `REPLY_MARKUP_TOO_LONG`
- Auto delete progress status message for each file when using upload all method
- Downloader improvements
    - Added support for gdrive file links
    - Handle `302` responses
- Copy message with additional info instead of forwarding and replying to reduce floodwaits
- Updated start message strings

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