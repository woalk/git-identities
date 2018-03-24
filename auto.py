from argparse import Namespace
from pathlib import Path

# --- general commands


# @param cwd:        a pathlib.Path to use
# @param identities: a configparser.ConfigParser() pointing to the .git_identities file
# @return: an argparse.Namespace
#          with (identity_key, identity, keyword, path, weakness)
def find_identity(cwd, identities):
    result_identity_key = None
    result_identity = None
    result_keyword = None
    result_path = None
    result_weakness = None

    try:
        for identity in identities.sections():
            identity_obj = identities[identity]
            i = 1
            while 'path' + str(i) in identity_obj:
                j = 0
                path = Path(identity_obj['path' + str(i)])
                if path == cwd:
                    result_identity = identity_obj
                    result_identity_key = identity[9:]
                    result_path = identity_obj['path' + str(i)]
                    result_weakness = None
                    raise StopIteration
                else:
                    if path in cwd.parents:
                        weakness = cwd.parents.index(path)
                        if result_weakness is None or result_weakness > weakness:
                            result_identity = identity_obj
                            result_identity_key = identity[9:]
                            result_path = identity_obj['path' + str(i)]
                            result_weakness = weakness
                i += 1
        if result_identity is not None:
            raise StopIteration
        for identity in identities.sections():
            identity_obj = identities[identity]
            i = 1
            while 'keyword' + str(i) in identity_obj:
                if identity_obj['keyword' + str(i)] in str(cwd):
                    result_identity = identity_obj
                    result_identity_key = identity[9:]
                    result_keyword = identity_obj['keyword' + str(i)]
                    raise StopIteration
                i += 1
    except StopIteration:
        pass
    return Namespace(identity_key=result_identity_key, identity=result_identity, keyword=result_keyword,
                     path=result_path, weakness=result_weakness)
