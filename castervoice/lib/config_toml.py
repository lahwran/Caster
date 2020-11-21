from castervoice.lib import utilities

class BaseConfig(object):
    def __init__(self):
        self._config = {}

    def get(self, key):
        return None if key not in self._config else self._config[key]

    def put(self, key, value):
        self._config[key] = value


class TomlConfig(BaseConfig):

    def __init__(self, config_path):
        super(TomlConfig, self)
        self._config_path = config_path

    def save(self):
        utilities.save_toml_file(self._config, self._config_path)

    def load(self):
        self._config = utilities.load_toml_file(self._config_path)
