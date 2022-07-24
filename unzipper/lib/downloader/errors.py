# Exceptions raised by the Downloader class

class InvalidUrl(Exception):
    def __init__(self) -> None:
        super().__init__("The provided string isn't an url!")


class InvalidContentType(Exception):
    def __init__(self) -> None:
        super().__init__("The provided url doesn't contain any archive!")


class HttpStatusError(Exception):
    def __init__(self) -> None:
        super().__init__("Received HTTP status code isn't 200")


class FileTooLarge(Exception):
    def __init__(self) -> None:
        super().__init__("Archive is too large to download!")
