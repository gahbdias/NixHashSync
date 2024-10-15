#!/usr/bin/env python
import os
import requests

# Importa o Singleton Config para obter plugins
from nixhashsync.config import Config


# Função para buscar o hash do último commit de um repositório no GitHub
def get_latest_commit_hash(author: str, name: str) -> str:
    url = f"https://api.github.com/repos/{author}/{name}/commits"
    headers = {"Accept": "application/vnd.github.v3+json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commits = response.json()
        return commits[0]["sha"] if commits else None
    else:
        raise Exception(
            f"Erro ao acessar {
                author}/{name}: {response.status_code}"
        )


# Função para atualizar o arquivo .rev com o hash do commit
def update_rev_file(rev_path: str, new_hash: str):
    with open(rev_path, "w") as rev_file:
        rev_file.write(new_hash)


# Função para processar plugins do arquivo YAML
def process_plugins():
    config = Config()  # Obtém a instância Singleton
    plugins = config.get_plugins()

    for plugin in plugins:
        author = plugin.author  # Acesso direto como atributo
        name = plugin.name
        branch = plugin.branch  # Pega o branch do plugin

        print(f"Processando {author}/{name} (branch: {branch})")

        try:
            # Obter o hash do último commit
            latest_hash = get_latest_commit_hash(author, name)
            print(f"Último hash de {author}/{name}: {latest_hash}")

            # Atualizar o arquivo .rev
            rev_file_path = os.path.expanduser(
                f"~/nix-node-plo/modules/home-manager/blackmatter/nvim/plugins/{
                    author}/{name}/rev.nix"
            )
            update_rev_file(rev_file_path, latest_hash)
        except Exception as e:
            print(f"Erro ao processar {author}/{name}: {e}")


def main():
    print("NixHashSync Merge Configs")
    process_plugins()
