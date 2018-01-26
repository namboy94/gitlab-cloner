#!/usr/bin/env python
"""
Copyright Hermann Krumrey <hermann@krumreyh.com>, 2017

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import print_function

import os
import sys
import json
import argparse
import requests
from subprocess import Popen, PIPE


def parse_args():
    """
    Parses the Command Line Arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="The Gitlab URL")
    parser.add_argument("user", help="The Gitlab user")
    parser.add_argument("token", help="The Gitlab API Token")
    parser.add_argument("-a", "--archived", default=False, action="store_true",
                        help="Includes archived repositories")
    parser.add_argument("-d", "--destination", default=os.getcwd(),
                        help="The destination directory.")

    return parser.parse_args()


def clone_repos(projects, destination):
    """
    Clones the Repositories to the destination directory
    """

    destination = os.path.abspath(destination)

    if not os.path.exists(destination):
        os.makedirs(destination)
    if not os.path.isdir(destination):
        print("Could not create directory " + destination)
        sys.exit(1)

    cwd = os.getcwd()  # Remember the current working directory

    for project in projects:

        os.chdir(destination)
        name = project["name"]
        repo_destination = os.path.join(destination, name)

        if os.path.isdir(repo_destination):

            # If the repository has been cloned already, just fetch new changes

            print("Fetching " + name, end="... ")
            command = ["git", "fetch", "--all"]
            os.chdir(repo_destination)

        else:

            print("Cloning " + name, end="... ")
            ssh_url = project["ssh_url_to_repo"]
            command = ["git", "clone", ssh_url]

        process = Popen(command, stdout=PIPE, stderr=PIPE)
        process.communicate()

        print("Done.")

    os.chdir(cwd)  # Return to original working directory


def get_repositories(gitlab_url, user, api_key, archived):
    """
    Fetches the repository information from the gitlab API.
    Requires a valid Gitlab URL, the user's access token.

    If archived is True, also include archived repositories
    """

    if not gitlab_url.endswith("/"):
        gitlab_url += "/"

    query = gitlab_url + "api/v4/users/" + user + "/projects"
    query += "?private_token=" + api_key

    if archived:
        query += "&archived=true"

    result = requests.get(query)
    projects = []

    count = 1
    more_pages = True
    while more_pages:

        more_pages = result.headers["X-Next-Page"] != ""

        if result.status_code != 200:  # If unauthorized or other error, stop.
            print(result.text)
            sys.exit(1)
        else:
            projects += json.loads(result.text)
            count += 1
            result = requests.get(query + "&page=" + str(count))

    return projects


if __name__ == "__main__":

    args = parse_args()
    projects = get_repositories(args.url, args.user, args.token, args.archived)
    clone_repos(projects, args.destination)
