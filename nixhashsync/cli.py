#!/usr/bin/env python
import requests


def get_latest_commit_hash(owner: str, repo: str) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {"Accept": "application/vnd.github.v3+json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commits = response.json()
        if commits:
            # Pega o hash (sha) do commit mais recente
            return commits[0]["sha"]
        else:
            raise Exception(
                f"Nenhum commit encontrado no repositório {owner}/{repo}.")
    else:
        raise Exception(
            f"Erro ao acessar o repositório {
                owner}/{repo}: {response.status_code}"
        )


def main():
    print("we are the worst!")
    owner = "nixos"  # Exemplo de dono do repositório
    repo = "nixpkgs"  # Exemplo de repositório
    print("trying stuff")
    try:
        latest_hash = get_latest_commit_hash(owner, repo)
        print(f"Último hash do repositório {owner}/{repo}: {latest_hash}")
    except Exception as e:
        print(str(e))
