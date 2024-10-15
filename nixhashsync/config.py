import yaml
import os
from pydantic import BaseModel, ValidationError, Field
from typing import List


# Definição do formato esperado para o arquivo YAML usando Pydantic
class Plugin(BaseModel):
    author: str
    name: str
    branch: str = Field(default="main")


class ConfigModel(BaseModel):
    plugins: List[Plugin]


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
            config_data = yaml.safe_load(file)

        # Validação usando Pydantic
        try:
            self.config = ConfigModel(**config_data)
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
