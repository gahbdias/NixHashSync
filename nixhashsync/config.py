import yaml
import os


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        config_file = os.path.join(os.path.dirname(__file__), "config.yaml")
        with open(config_file, "r") as file:
            self.config = yaml.safe_load(file)

    def get_plugins(self):
        return self.config.get("plugins", [])


# Exemplo de uso:
if __name__ == "__main__":
    config = Config()
    plugins = config.get_plugins()
    for plugin in plugins:
        print(
            f"Author: {plugin['author']}, Name: {
                plugin['name']}, Branch: {plugin['branch']}"
        )
