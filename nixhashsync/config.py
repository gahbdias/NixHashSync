import yaml
import os
from pydantic import BaseModel, ValidationError, Field
from typing import List
from deepmerge import Merger


# Definição do formato esperado para o arquivo YAML usando Pydantic
class Plugin(BaseModel):
    author: str
    name: str
    branch: str = Field(default="main")


class ConfigModel(BaseModel):
    plugins: List[Plugin]


class Config:
    _instance = None
    CONFIG_LOCATIONS = [
        "/etc/nixhashsync/config.yml",
        os.path.expanduser("~/.config/nixhashsync/config.yml"),
        ".config/nixhashsync/config.yml",
    ]

    # Definir como mesclar dicionários (configurações)
    merger = Merger([(list, ["append"]), (dict, ["merge"])],
                    ["override"], ["override"])

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        merged_config = {}

        found_files = 0
        for config_file in self.CONFIG_LOCATIONS:
            if os.path.exists(config_file):
                found_files += 1
        if found_files == 0:
            raise ValidationError("could not find a configuration in any path")

        for config_file in self.CONFIG_LOCATIONS:
            if os.path.exists(config_file):
                with open(config_file, "r") as file:
                    config_data = yaml.safe_load(file)
                    # Mescla o arquivo de configuração na estrutura principal
                    if config_data:
                        self.merger.merge(merged_config, config_data)

        # Validação usando Pydantic
        try:
            self.config = ConfigModel(**merged_config)
        except ValidationError as e:
            print(f"Erro de validação no arquivo de configuração: {e}")
            raise

    def get_plugins(self):
        return self.config.plugins


# Exemplo de uso:
if __name__ == "__main__":
    try:
        config = Config()
        plugins = config.get_plugins()
        for plugin in plugins:
            print(
                f"Author: {plugin.author}, Name: {
                    plugin.name}, Branch: {plugin.branch}"
            )
    except Exception as e:
        print(f"Erro ao carregar a configuração: {e}")
