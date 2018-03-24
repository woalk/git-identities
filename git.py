from subprocess import run, PIPE, DEVNULL


# Returns a tuple (value, BOOL) whereas BOOL==True means that the config was fetched from the local .git/config
def config_get(section, key):
    value = run(['git', 'config', '--get', '%s.%s' % (section, key)],
                stdout=PIPE, stderr=None, encoding='utf_8', universal_newlines=True).stdout[:-1]
    local_result = run(['git', 'config', '--local', '--get', '%s.%s' % (section, key)], stdout=DEVNULL, stderr=None)

    return value, local_result.returncode == 0


def config_set(section, key, value, local=True):
    if local:
        result = run(['git', 'config', '--local', '%s.%s' % (section, key), value], stdout=None, stderr=None)
    else:
        result = run(['git', 'config', '--global', '%s.%s' % (section, key), value], stdout=None, stderr=None)
    return result.returncode == 0


def config_unset(section, key, local=True):
    if local:
        result = run(['git', 'config', '--local', '--unset', '%s.%s' % (section, key)], stdout=None, stderr=None)
    else:
        result = run(['git', 'config', '--global', '--unset', '%s.%s' % (section, key)], stdout=None, stderr=None)
    return result.returncode == 0


def clone(url, args):
    print(['git', 'clone'] + args + ['--', url])
    return run(['git', 'clone'] + args + ['--', url])
