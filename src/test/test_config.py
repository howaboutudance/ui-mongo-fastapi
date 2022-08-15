import pytest
from ui_mongo import config


def test_config_var():
  assert config.settings.test_var == "test variable"