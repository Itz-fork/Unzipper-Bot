# Exceptions raised by the Extractor class

class ExtractionFailed(Exception):
    def __init__(self) -> None:
        super().__init__("Extraction failed due to an unknown error! Please make sure that your archive isn't corrupted")