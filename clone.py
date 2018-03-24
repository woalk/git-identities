#!/usr/bin/env python3

from pathlib import Path
from auto import find_identity
from colors import Colors
import configparser
import argparse
import git

identities_file_path = str(Path.home() / '.git_identities')

parser = argparse.ArgumentParser(epilog="Clone a Git repo and automatically set the identity of the repo to the "
                                        "current context. Accepts all other arguments from `git clone'.")
parser.add_argument('url')
args = parser.parse_known_args()

name = str(args[0].url).rsplit('/', maxsplit=1)[-1]
if name[-4:] == '.git':
    name = name[:-4]
path = Path.cwd() / name

print(path)

identities = configparser.ConfigParser()
identities.read(identities_file_path)

result = find_identity(path, identities)
if result.identity_key is None:
    print(Colors.yellow + 'Warning:' + Colors.default +
          ' No identity matches the current path, so no identity will be set.')
    returned = git.clone(args[0].url, args[1])
else:
    line = 'Selected ' + Colors.bold + result.identity_key + Colors.default + ' based on '
    if result.keyword is not None:
        line += 'keyword "%s".' % result.keyword
    elif result.path is not None:
        line += 'path "%s" with weakness %s.' % (result.path, result.weakness)
    print(line)

    returned = git.clone(args[0].url, args[1] + ['--config', 'user.name=%s' % result.identity['name'],
                                                 '--config', 'user.email=%s' % result.identity['email']])

exit(returned.returncode)
