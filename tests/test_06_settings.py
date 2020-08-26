import os
import tempfile

import pytest
from pydantic import BaseSettings


@pytest.fixture(scope="session")
def tmp_settings_dir():
    yield tempfile.mkdtemp()


@pytest.fixture
def tmp_settings_file(tmp_settings_dir):
    file_path = os.path.join(tmp_settings_dir, 'dummy.env')
    with open(file_path, "w") as f:
        f.write("DUMMY_VALUE = 1\n")
    yield file_path


# https://pydantic-docs.helpmanual.io/usage/settings/
class Settings(BaseSettings):
    dummy_value: int = 0

    class Config:
        env_file_encoding = "utf-8"


class ConfigFileNotFoundException(Exception):
    """Required settings file can't be found."""


class MandatoryEnvironmentVariableNotDefinedException(Exception):
    """Required environment variable not provided."""


def load_settings_from_file(settings_file: str) -> Settings:
    if not os.path.exists(settings_file):
        raise ConfigFileNotFoundException(
            f"The settings file {settings_file} could not be found."
        )
    return Settings(_env_file=settings_file)


def get_mandatory_environment_variable(environment_variable_name: str) -> str:
    """None is not considered a valid value."""
    value = os.getenv(environment_variable_name)
    if value is None:
        raise MandatoryEnvironmentVariableNotDefinedException(
            f"The {environment_variable_name} environment variable is mandatory."
        )
    return value


def test_load_settings_from_file_successfully(tmp_settings_file: str):
    settings = load_settings_from_file(tmp_settings_file)
    assert settings.dummy_value == 1


def test_load_settings_from_nonexistent_file_raises_exception():
    with pytest.raises(ConfigFileNotFoundException):
        load_settings_from_file('nonexistent.env')


def test_get_missing_mandatory_environment_variable_raises_exception():
    with pytest.raises(MandatoryEnvironmentVariableNotDefinedException):
        get_mandatory_environment_variable("A_MISSING_VARIABLE")


def test_get_valid_mandatory_environment_variable_successfully():
    an_environment_var = "A_DUMMY_VAR"
    assert os.environ.get(an_environment_var) is None  # Checks the pre-test state is safe.

    an_override_value = "value"
    os.environ[an_environment_var] = an_override_value
    try:
        assert (
            get_mandatory_environment_variable(an_environment_var)
            == an_override_value
        )
    finally:
        del os.environ[an_environment_var]
