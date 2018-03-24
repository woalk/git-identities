#!/usr/bin/env python3

import argparse
import commands

parser = argparse.ArgumentParser(epilog='Manage identities for Git commits.')
subparsers = parser.add_subparsers(metavar='command',
                                   title='command',
                                   description='the command to be executed.',
                                   dest='command')
subparsers.required = True
parser_list = subparsers.add_parser('list',
                                    help='list all known identities',
                                    aliases=['ls'])
parser_list.set_defaults(func=commands.list_identities)
parser_list.add_argument('-v', '--verbose',
                         action='store_true',
                         help='print all details about every identity')

parser_show = subparsers.add_parser('show',
                                    help='show details about the given identity')
parser_show.set_defaults(func=commands.show_identity)
parser_show.add_argument('identity', nargs='?', help='the identity to show details about', default=None)

parser_add = subparsers.add_parser('add',
                                   help='add a new identity')
parser_add.set_defaults(func=commands.add_identity)
parser_add.add_argument('-c', '--current',
                        action='store_true',
                        help="add the identity of the current context, either from the current repo's .git/config or "
                             "the global gitconfig")
parser_add.add_argument('identity', help='a unique ID for the new identity')
parser_add.add_argument('name',
                        help='the full user name, to use for git-config user.name; required if not specifying -c',
                        nargs='?',
                        default=None)
parser_add.add_argument('email',
                        help='the email address, to use for git-config user.name; required if not specifying -c',
                        nargs='?',
                        default=None)
parser_add.add_argument('-f', '--force',
                        action='store_true',
                        help="overwrite any already existing identity with the given ID")

parser_remove = subparsers.add_parser('remove',
                                      help='remove a known identity')
parser_remove.set_defaults(func=commands.remove_identity)
parser_remove.add_argument('identity', help='the unique ID of the identity to remove')

parser_update = subparsers.add_parser('update',
                                      help='change the settings of a known identity')
parser_update.set_defaults(func=commands.update_identity)
parser_update.add_argument('identity', help='the unique ID of the identity to update')
parser_update.add_argument('--name',
                           help='change the full name of this identity',
                           default=None)
parser_update.add_argument('--email',
                           help='change the email address of this identity',
                           default=None)
parser_update.add_argument('-k', '--keywords',
                           nargs='*',
                           help='change the keywords used to choose this identity; can be multiple, '
                                'supply no keywords after this command to clear keywords',
                           default=None)
parser_update.add_argument('-p', '--paths',
                           nargs='*',
                           help='change the paths used to choose this identity; can be multiple, '
                                'supply no paths after this command to clear paths',
                           default=None)

parser_apply = subparsers.add_parser('apply',
                                     help='set the config to use the specified known identity')
parser_apply.set_defaults(func=commands.apply_identity)
parser_apply.add_argument('identity',
                          nargs='?',
                          help='the unique ID of the identity to apply',
                          default=None)
parser_apply.add_argument('--global',
                          dest='local',
                          action='store_false',
                          help="apply the identity globally for all non-configured projects")
parser_apply.add_argument('--local',
                          dest='local',
                          action='store_true',
                          required=False,
                          help="apply the identity locally for the current repo (default)")
parser_apply.add_argument('-a', '--auto',
                          action='store_true',
                          help="apply the identity matching based on current context's keywords or path")

parser_use_global = subparsers.add_parser('use-global',
                                          help='remove any local identity config to reset to the global identity')
parser_use_global.set_defaults(func=commands.unset_identity)

args = parser.parse_args()
result = args.func(args)

exit(result)
