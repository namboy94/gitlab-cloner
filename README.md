# Gitlab Cloner

[![build status](https://gitlab.namibsun.net/namibsun/python/gitlab-cloner/badges/master/build.svg)](https://gitlab.namibsun.net/namibsun/python/gitlab-cloner/commits/master)

![Logo](resources/logo/logo-readme.png "Logo")

This is a small script that clones all git repositories of a user from a
Gitlab server.

This requires the user's API access token.

## Usage

Use the Gitlab Server's URL as the first positional argument, the second 
one should be the API key.

You can also specify a destination directory for the repositories
with the ```-d``` argument.

To include any archived repositories, use the ```-a``` option

## Further Information

* [Changelog](CHANGELOG)
* [License (GPLv3)](LICENSE)
* [Gitlab](https://gitlab.namibsun.net/namibsun/python/gitlab-cloner)
* [Github](https://github.com/namboy94/gitlab-cloner)
* [Progstats](https://progstats.namibsun.net/projects/gitlab-cloner)
* [PyPi](https://pypi.org/project/gitlab-cloner)
