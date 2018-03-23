#!/usr/bin/env python3

from pathlib import Path
from colors import Colors
import git
import configparser

identities_file_path = str(Path.home() / '.git_identities')

identities = configparser.ConfigParser()
identities.read(identities_file_path)

cwd = Path.cwd()
resultIdentity = None
resultIdentityKey = None
resultKeyword = None
resultPath = None
resultWeakness = None

try:
    for identity in identities.sections():
        identity_obj = identities[identity]
        i = 1
        while 'path' + str(i) in identity_obj:
            j = 0
            path = Path(identity_obj['path' + str(i)])
            if path == cwd:
                resultIdentity = identity_obj
                resultIdentityKey = identity[9:]
                resultPath = identity_obj['path' + str(i)]
                resultWeakness = None
                raise StopIteration
            else:
                if path in cwd.parents:
                    weakness = cwd.parents.index(path)
                    if resultWeakness is None or resultWeakness > weakness:
                        resultIdentity = identity_obj
                        resultIdentityKey = identity[9:]
                        resultPath = identity_obj['path' + str(i)]
                        resultWeakness = weakness
            i += 1
    if resultIdentity is not None:
        raise StopIteration
    for identity in identities.sections():
        identity_obj = identities[identity]
        i = 1
        while 'keyword' + str(i) in identity_obj:
            if identity_obj['keyword' + str(i)] in str(cwd):
                resultIdentity = identity_obj
                resultIdentityKey = identity[9:]
                resultKeyword = identity_obj['keyword' + str(i)]
                raise StopIteration
            i += 1
except StopIteration:
    pass

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
    print('Or you can change identity with\n   git identity apply --auto')
    exit(1)
