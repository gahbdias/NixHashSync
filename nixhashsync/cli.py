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


# Função para extrair o autor e nome do plugin de um arquivo default.nix
def extract_author_and_name(nix_content: str):
    # Tentativa 1: Padrão com author e name em variáveis separadas
    author_match = re.search(r'author = "(.*?)";', nix_content)
    name_match = re.search(r'name = "(.*?)";', nix_content)

    if author_match and name_match:
        return author_match.group(1), name_match.group(1)

    # Tentativa 2: Padrão com author e name inline
    inline_match = re.search(
        r"config\.blackmatter\.programs\.nvim\.plugins\.(.*?)\.(.*?)\.enable",
        nix_content,
    )
    if inline_match:
        return inline_match.group(1), inline_match.group(2)

    # Se nenhum padrão for encontrado
    raise ValueError("Formato desconhecido em default.nix")


# Função para processar todos os plugins
def process_plugins(base_path: str):
    print("processing plugins")
    for root, dirs, files in os.walk(base_path):
        print("on loop")
        if "default.nix" in files:
            default_nix_path = os.path.join(root, "default.nix")
            rev_file_path = os.path.join(root, "rev.nix")

            # Ler o conteúdo de default.nix
            with open(default_nix_path, "r") as nix_file:
                nix_content = nix_file.read()

                # Extrair 'author' e 'name' usando os diferentes formatos
                try:
                    author, name = extract_author_and_name(nix_content)

                    # Obter o hash do último commit
                    print("getting hash")
                    latest_hash = get_latest_commit_hash(author, name)
                    print(f"Último hash de {author}/{name}: {latest_hash}")

                    # Atualizar o arquivo .rev
                    update_rev_file(rev_file_path, latest_hash)
                except Exception as e:
                    print(f"Erro ao processar {default_nix_path}: {e}")


# Caminho base para os plugins
plugins_base_path = os.path.expanduser(
    "~/nix-node-plo/modules/home-manager/blackmatter/nvim/plugins/EtiamNullam/relative-source.nvim"
)


def main():
    print("NixHashSync sem config")
    process_plugins(plugins_base_path)
