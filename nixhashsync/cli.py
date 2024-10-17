#!/usr/bin/env python
import os
import time
import requests

# Import Singleton Config to retrieve plugins
from nixhashsync.config import Config


# Function to fetch the latest commit hash from a GitHub repository
def get_latest_commit_hash(author: str, name: str) -> str:
    url = f"https://api.github.com/repos/{author}/{name}/commits"
    headers = {"Accept": "application/vnd.github.v3+json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        commits = response.json()
        return commits[0]["sha"] if commits else None
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error accessing {author}/{name}: {e}")


# Function to update the .rev file with the commit hash, now adding quotes
def update_rev_file(rev_file: str, new_hash: str):
    with open(os.path.expanduser(rev_file), "w") as rev_file_handle:
        rev_file_handle.write(f'"{new_hash}"')


# Function to process plugins from the YAML configuration file
def process_plugins():
    config = Config()  # Get Singleton instance
    file_path = config.get_file_path()  # Get the base path for files
    plugins = config.get_plugins()

    for plugin in plugins:
        author = plugin.author
        name = plugin.name
        branch = plugin.branch
        rev_file_path = os.path.join(
            file_path, f"{author}/{name}/rev.nix"
        )  # Use the file_path from the config

        print(f"Processing {author}/{name} (branch: {branch})")

        try:
            # Fetch the latest commit hash
            latest_hash = get_latest_commit_hash(author, name)
            print(f"Latest hash for {author}/{name}: {latest_hash}")

            # Update the .rev file with the quoted commit hash
            update_rev_file(rev_file_path, latest_hash)
        except Exception as e:
            print(f"Error processing {author}/{name}: {e}")
            print("Waiting 60 seconds before retrying...")
            time.sleep(60)
            process_plugins()  # Retry after 60 seconds


def main():
    print("NixHashSync with quotes")
    process_plugins()
