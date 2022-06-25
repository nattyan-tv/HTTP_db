class HTTP_db_Exception(Exception):
    """Base exception class for HTTP_db"""
    pass


class DatabaseKeyError(HTTP_db_Exception):
    """Raised when a key is not found in the database"""
    pass


class DatabaseReadError(HTTP_db_Exception):
    """Raised when an error occurs while reading from the database"""
    pass


class DatabaseWriteError(HTTP_db_Exception):
    """Raised when an error occurs while writing to the database"""
    pass


class DatabaseDeleteError(HTTP_db_Exception):
    """Raised when an error occurs while deleting from the database"""
    pass


class UnknownDatabaseError(HTTP_db_Exception):
    """Raised when an unknown database error occurs"""
    pass


class DatabaseIOError(HTTP_db_Exception):
    """Raised when a database file cannot be read."""
    pass

class DatabaseAuthenticationError(HTTP_db_Exception):
    """Raisede when a database authentication error has occrred."""
