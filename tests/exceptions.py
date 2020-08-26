class ConfigFileNotFoundException(Exception):
    """Required settings file can't be found."""


class MandatoryEnvironmentVariableNotDefinedException(Exception):
    """Required environment variable not provided."""
