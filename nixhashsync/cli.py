#!/usr/bin/env python
import os
import re
import requests


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


# Função para processar todos os plugins
def process_plugins(base_path: str):
    print("processing plugins")
    for root, dirs, files in os.walk(base_path):
        print("in the looop")
        if "default.nix" in files:
            default_nix_path = os.path.join(root, "default.nix")
            rev_file_path = os.path.join(root, "rev.nix")

            # Extrair 'author' e 'name' de default.nix
            print("opening files")
            with open(default_nix_path, "r") as nix_file:
                nix_content = nix_file.read()
                author = re.search(r'author = "(.*?)";', nix_content).group(1)
                name = re.search(r'name = "(.*?)";', nix_content).group(1)

                # Obter o hash do último commit
                try:
                    print("getting a hash")
                    latest_hash = get_latest_commit_hash(author, name)
                    print("got a hash")
                    print(f"Último hash de {author}/{name}: {latest_hash}")

                    # Atualizar o arquivo .rev
                    update_rev_file(rev_file_path, latest_hash)
                except Exception as e:
                    print(f"Erro ao processar {author}/{name}: {e}")
    print("getting the hell out")


# Caminho base para os plugins
plugins_base_path = os.path.expanduser(
    "~/nix-node-plo/modules/home-manager/blackmatter/nvim/plugins/"
)


def main():
    print("NixHashSync 15/10")
    process_plugins(plugins_base_path)
