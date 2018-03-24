#!/usr/bin/env python3

from pathlib import Path
from colors import Colors
from auto import find_identity
import git
import configparser

identities_file_path = str(Path.home() / '.git_identities')

identities = configparser.ConfigParser()
identities.read(identities_file_path)

cwd = Path.cwd()
result = find_identity(cwd, identities)

resultIdentity = result.identity
resultIdentityKey = result.identity_key
resultKeyword = result.keyword
resultPath = result.path
resultWeakness = result.weakness

git_config_user = git.config_get('user', 'name')
git_config_email = git.config_get('user', 'email')

if resultIdentity is None:
    if git_config_user[1] or git_config_email[1]:
        print(Colors.yellow + 'Warning:' + Colors.default +
              ' No identity matches the current path, but a local identity config is set.')
elif resultIdentity['name'] != git_config_user[0] or resultIdentity['email'] != git_config_email[0]:
    print(Colors.red + 'Warning:' + Colors.default +
          ' You are committing with an identity that does not match your preferences for this context.')
    line = '\nReason: found expected identity ' + Colors.bold + resultIdentityKey + Colors.default
    if resultKeyword is not None:
        line += ' by keyword "%s"' % resultKeyword
    elif resultPath is not None:
        line += ' by path "%s" with weakness %s' % (resultPath, resultWeakness)
    else:
        line += 'unknown'
    print(line)
    print('       Expected: %s <%s>' % (resultIdentity['name'], resultIdentity['email']))
    print('Committing with: %s <%s>' % (git_config_user[0], git_config_email[0]))
    print('\nIf you still want to commit, use\n   git commit --no-verify')
    print('Or you can change identity with\n   git identities apply --auto')
    exit(1)
