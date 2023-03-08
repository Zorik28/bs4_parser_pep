class ParserFindTagException(Exception):
    """Called when the parser cannot find the tag."""
    pass


class FindVersionsException(Exception):
    """Called when no list of Python versions found."""
    pass


class NoneResponseException(Exception):
    """Called when response is absent."""
    pass
