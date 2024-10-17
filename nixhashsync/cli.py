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

    response = requests.get(url, headers=headers)
    if response.status_code in [200]:
        commits = response.json()
        return commits[0]["sha"] if commits else None
    elif response.status_code in [403, 402, 404]:
        raise requests.exceptions.RequestException(
            f"Error accessing {author}/{name}: HTTP {response.status_code}"
        )
    else:
        response.raise_for_status()


# Function to update the .rev file with the commit hash, now adding quotes
def update_rev_file(rev_file: str, new_hash: str):
    with open(os.path.expanduser(rev_file), "w") as rev_file_handle:
        rev_file_handle.write(f'"{new_hash}"')


# Function to show countdown timer
def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timeformat = f"{mins:02d}:{secs:02d}"
        print(f"Retrying in: {timeformat}", end="\r")
        time.sleep(1)
        seconds -= 1
    print("Retrying now...            ")


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
        except requests.exceptions.RequestException as e:
            print(f"Error processing {author}/{name}: {e}")
            print("Waiting 60 seconds before retrying...")
            countdown_timer(60)  # Show countdown before retrying
            process_plugins()  # Retry after the countdown
        except Exception as e:
            print(f"An unexpected error occurred: {e}")  # Catch non-API errors


def main():
    print("NixHashSync | Waiting when request returns error")
    process_plugins()
