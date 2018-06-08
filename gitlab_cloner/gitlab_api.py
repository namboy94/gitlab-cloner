"""LICENSE
Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of gitlab-cloner.

gitlab-cloner is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

gitlab-cloner is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with gitlab-cloner.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""


import os
import json
import shutil
import requests
from typing import List, Dict, Any
from subprocess import check_output
from colorama import Fore, Style


def get_projects(gitlab_url: str, private_token: str) \
        -> List[Dict[str, Any]]:
    """
    Retrieves a list of repositories that the provided private token
    grants access to.
    :param gitlab_url: The URL of the gitlab instance, including https etc.
    :param private_token: The private token to use
    :return: A list of gitlab projects
    """

    url = gitlab_url + "/api/v4/projects?private_token=" + private_token
    response = requests.get(url)

    projects = json.loads(response.text)

    while response.headers["X-Next-Page"]:
        next_page = response.headers["X-Next-Page"]
        response = requests.get(url + "&page=" + next_page)
        projects += json.loads(response.text)

    return projects


def clone_repo(repo: Dict[str, Any], private_token: str):
    """
    Clones a git repository. If the repository already exists,
    the user will be prompted to delete the old repository.
    If the user refuses, the repository will not be cloned.
    :param repo: The repository to clone
    :param private_token: The private token to use when cloning
    :return: None
    """

    if os.path.isdir(repo["name"]):
        resp = input("Repository " + repo["name"] + "exists. Delete? (y|n)")
        if resp == "y":
            shutil.rmtree(repo["name"])
        else:
            return

    oauth = "oauth2:" + private_token + "@"
    url = repo["http_url_to_repo"]\
        .replace("http://", "http://" + oauth)\
        .replace("https://", "https://" + oauth)

    command = ["git", "clone", url]
    print(Fore.CYAN + " ".join(command) + Style.RESET_ALL)
    output = check_output(command)
    print(Fore.MAGENTA + output.decode() + Style.RESET_ALL)
