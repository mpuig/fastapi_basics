import os

import pytest

from tests.exceptions import ConfigFileNotFoundException, MandatoryEnvironmentVariableNotDefinedException
from tests.settings import load_settings_from_file, get_mandatory_environment_variable, load_settings_from_environment


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


def test_load_settings_from_environment_variable_successfully(tmp_settings_dir, dummy_env):
    settings = load_settings_from_environment("DUMMY_ENV_FOR_TEST", tmp_settings_dir)
    assert settings.dummy_value == 99


def test_load_settings_from_nonexistent_environment_variable_raises_exception():
    with pytest.raises(MandatoryEnvironmentVariableNotDefinedException):
        load_settings_from_environment("NONEXISTENT_ENV")
