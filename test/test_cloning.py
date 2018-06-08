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
import shutil
from unittest import TestCase
from gitlab_cloner import clone_all, get_projects


class CloningTest(TestCase):
    """
    Class that tests the cloning of gitlab repositories
    """

    testdir = "repotest"
    """
    The directory in which the repos will be stored
    """

    def setUp(self):
        """
        Runs cleanup
        :return: None
        """
        self.cleanup()

    def tearDown(self):
        """
        Runs cleanup
        :return: None
        """
        self.cleanup()

    def cleanup(self):
        """
        Deletes the testing directory
        :return: None
        """
        if os.path.isdir(self.testdir):
            shutil.rmtree(self.testdir)

    def test_cloning(self):
        url = "https://gitlab.namibsun.net"
        token = ""  # Will only fetch public repos
        destination = self.testdir

        current = os.getcwd()
        clone_all(url, token, destination)
        self.assertEquals(current, os.getcwd())

        projects = get_projects(url, token)
        self.assertEquals(len(projects), len(os.listdir(self.testdir)))
