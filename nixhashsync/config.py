import yaml
import os
from pydantic import BaseModel, ValidationError, Field
from typing import List, Optional


# Definição do formato esperado para o arquivo YAML usando Pydantic
class PluginConfig(BaseModel):
    path: str  # Caminho dos plugins


class Plugin(BaseModel):
    author: str
    name: str
    branch: str = Field(default="main")


class ConfigModel(BaseModel):
    plugin: PluginConfig  # Configurações gerais do plugin, incluindo o caminho
    plugins: Optional[List[Plugin]] = Field(default_factory=list)


class Config:
    _instance = None
    CONFIG_LOCATIONS = [
        "/etc/nixhashsync/config.yml",
        os.path.expanduser("~/.config/nixhashsync/config.yml"),
        ".config/nixhashsync/config.yml",  # Caminho relativo na raiz do projeto
    ]

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        merged_config = {}
        found_file = False  # Flag para verificar se algum arquivo foi encontrado

        # Verificar se algum dos arquivos de configuração existe
        for config_file in self.CONFIG_LOCATIONS:
            print(
                f"Tentando carregar: {config_file}"
            )  # Depuração para verificar os caminhos
            if os.path.exists(config_file):
                found_file = True  # Encontrou ao menos um arquivo
                with open(config_file, "r") as file:
                    config_data = yaml.safe_load(file)
                    # Mescla o arquivo de configuração na estrutura principal
                    if config_data:
                        merged_config.update(config_data)

        # Se nenhum arquivo de configuração foi encontrado, lança um erro
        if not found_file:
            raise FileNotFoundError(
                "Não foi possível encontrar arquivo de configuração"
            )

        # Validação usando Pydantic
        try:
            self.config = ConfigModel(**merged_config)
        except ValidationError as e:
            print(f"Erro de validação no arquivo de configuração: {e}")
            raise

    # Função para obter o caminho base dos plugins
    def get_file_path(self):
        return self.config.plugin.path

    def get_plugins(self):
        return self.config.plugins


# Exemplo de uso:
if __name__ == "__main__":
    try:
        config = Config()
        file_path = config.get_file_path()
        print(f"Plugin path: {file_path}")

        plugins = config.get_plugins()
        for plugin in plugins:
            print(
                f"Author: {plugin.author}, Name: {
                    plugin.name}, Branch: {plugin.branch}"
            )
    except Exception as e:
        print(f"Erro ao carregar a configuração: {e}")
