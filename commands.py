from os.path import basename
from colors import Colors
from pathlib import Path
import git
import configparser

identities_file_path = str(Path.home() / '.git_identities')


# subparsers 'command' functions
def list_identities(args):
    identities = configparser.ConfigParser()
    identities.read(identities_file_path)
    identity_counter = 0
    for identity in identities.sections():
        if identity[:9] == 'identity.':
            identity_counter += 1
            identity_obj = identities[identity]
            line = '  '
            git_config_user = git.config_get('user', 'name')
            git_config_email = git.config_get('user', 'email')
            if identity_obj['name'] == git_config_user[0] and \
                    identity_obj['email'] == git_config_email[0]:
                line = '* '
                if git_config_user[1] or git_config_email[1]:
                    line += Colors.yellow
                else:
                    line += Colors.green
            line += identity[9:] + Colors.default
            if args.verbose:
                line += " (%s <%s>)" % (identity_obj['name'], identity_obj['email'])
            print(line)
    if identity_counter == 0:
        print(Colors.red + 'There are no saved identities.' + Colors.default)
        print('\nUse\n   %s add ...\nto add a new identity.' % basename(__file__))
    return 0


def show_identity(args):
    git_config_user = git.config_get('user', 'name')
    git_config_email = git.config_get('user', 'email')
    identities = configparser.ConfigParser()
    identities.read(identities_file_path)
    identity = args.identity
    if identity is None:
        for identity_entry in identities.sections():
            identity_entry_obj = identities[identity_entry]
            if identity_entry_obj['name'] == git_config_user[0] and \
                    identity_entry_obj['email'] == git_config_email[0]:
                identity = identity_entry[9:]
                break
    if identity is None:
        print('[?] %s <%s>' % (git_config_user[0], git_config_email[0]))
        print(Colors.red +
              'The identity in the current context is not known to %s.' % basename(__file__) +
              Colors.default)
        print('You can add the current identity with\n   %s add --current' % basename(__file__))
        return

    identity_obj = identities['identity.' + identity]
    print('[%s] %s <%s>' % (identity, identity_obj['name'], identity_obj['email']))
    if identity_obj['name'] == git_config_user[0] and \
            identity_obj['email'] == git_config_email[0]:
        line = 'This is the ' + Colors.green + 'default' + Colors.default + ' identity in the current context.'
        if git_config_user[1] or git_config_email[1]:
            line += '\nIt is set ' + Colors.yellow + 'locally' + Colors.default + ' in the current repository.'
        else:
            line += '\nIt is set globally.'
        print(line)
    return 0


def add_identity(args):
    if not args.identity.isidentifier():
        print(Colors.red + 'The specified identity ID is not a valid identifier.' + Colors.default)
        return 1

    name = None
    email = None
    if args.current:
        git_config_user = git.config_get('user', 'name')
        git_config_email = git.config_get('user', 'email')
        name = git_config_user[0]
        email = git_config_email[0]
    else:
        name = args.name
        email = args.email
        if name is None or email is None:
            print(Colors.red + 'error: the following arguments are required: name, email or -c' + Colors.default)
            return 2

    identities = configparser.ConfigParser()
    identities.read(identities_file_path)
    if not args.force and identities.has_section('identity.' + args.identity):
        print(Colors.red + 'The specified identity ID already exists.' + Colors.default)
        print('To replace the existing identity, specify --force.')
        return 3

    identities['identity.' + args.identity] = {
        'name': name,
        'email': email
    }

    with open(identities_file_path, 'w') as identities_file:
        identities.write(identities_file)
    return 0


def remove_identity(args):
    identities = configparser.ConfigParser()
    identities.read(identities_file_path)
    if not identities.has_section('identity.' + args.identity):
        print(Colors.red + "The specified identity ID doesn't exist." + Colors.default)
        return 1

    identities.remove_section('identity.' + args.identity)
    with open(identities_file_path, 'w') as identities_file:
        identities.write(identities_file)
    return 0


def apply_identity(args):
    identities = configparser.ConfigParser()
    identities.read(identities_file_path)
    if not identities.has_section('identity.' + args.identity):
        print(Colors.red + "The specified identity ID doesn't exist." + Colors.default)
        return 1

    if not args.local:
        git_config_user = git.config_get('user', 'name')
        git_config_email = git.config_get('user', 'email')
        if git_config_user[1] or git_config_email[1]:
            print(Colors.yellow + 'Warning:' + Colors.default +
                  ' the current repo has a local identity config and will not use the new value.')

    identity_obj = identities['identity.' + args.identity]
    result_n = git.config_set('user', 'name', identity_obj['name'], local=args.local)
    result_e = git.config_set('user', 'email', identity_obj['email'], local=args.local)
    if not result_e and not result_n:
        return 5
    elif not result_e:  # and resultN
        return 2
    elif not result_n:  # and resultE
        return 3
    else:  # both True
        return 0


def unset_identity(args):
    result_n = git.config_unset('user', 'name')
    result_e = git.config_unset('user', 'email')
    if not result_e and not result_n:
        return 5
    elif not result_e:  # and resultN
        return 2
    elif not result_n:  # and resultE
        return 3
    else:  # both True
        return 0