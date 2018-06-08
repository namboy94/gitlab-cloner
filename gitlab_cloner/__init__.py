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
from gitlab_cloner.gitlab_api import clone_repo, get_projects


def clone_all(url: str, token: str, destination: str):
    """
    Clones all repositories accessible to the personal access token provided
    :param url: The gitlab URL, including https
    :param token: The personal access token to use
    :param destination: The destination in which to save the repos
    :return: None
    """
    current = os.getcwd()
    if not os.path.isdir(destination):
        os.makedirs(destination)
    os.chdir(destination)

    projects = get_projects(url, token)

    for project in projects:
        clone_repo(project, token)

    os.chdir(current)
