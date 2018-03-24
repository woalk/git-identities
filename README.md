# Git-Identities
**User identity management for git**

This program is meant to be used by people who work on multiple projects
with different Git identities, e.g. students or home-office workers.

Git-Identities allows you to change your Git config's `user.name` and `user.email`
easily and quickly from a database of known identities,
and provides automatic setters and checks to assure you're never committing with the wrong config again.

**This requires Git version `2.10+` to work correctly.**

## Usage

### Basics

Every command in this program has a help function by calling it with `-h` or `--help`.

The main command is `git identities`.
It allows managing your identities and applying it to different contexts.

With `git identities list`, you can list all known identities.

With `git identities add <id> <name> <email>`, you can add a new identity.
As `<id>`, use an identifier that can be used to reference your identity later,
it has to be alphanumeric with underscores, not starting with a number.

With `git identities apply <id>`, the identity is set as the local config's `user.name` and `user.email`.
You can reset a local choice with `git identities use-global`.

### "current context"

By "current context", the program means the configuration as it would be used by Git in the current directory.
This is either the local config in `.git/config` or a submodule config directory, that has overriden other settings,
the global config, or the system-wide config, whatever comes first in this order.

### Verifying

The main purpose of the Git-Identities program is to ensure that you're using the right identity.

To accomplish this, you can use
```bash
git identities update <id> --paths /path/to/projects1 /path/to/projects2 ...
```

to set one or more paths, whose subdirectories will honor the given identity.
If the program is installed correctly,
it will not let you commit
if you would commit with a different identity than the one that should be used in the current context.

(You can override this for one time by calling `git commit --no-verify`, if you need to.)

It will also warn you (but not stop you to commit)
if the current context does not match to any identity known to Git-Identities.

#### Keywords

Git-Identities also supports keywords.
They can be set with
```bash
git identities update <id> --keywords keyword1 keyword2 ...
```

An identity with a keyword matches whenever the path contains the keyword, anywhere.
Paths are always prioritized, and keywords are prioritized by the order they were specified in the `update` command.

Paths are recommended and keywords discouraged, as they can prove a bit unpredictable.
They have their advantages for verifying, though, sometimes.

#### Example

Assume we have used
```bash
git identities add private "Woalk" "woalk@example.com"
git identities add work "Name Surname" "surname@example.com"
```
to add two identities.

Assume further that we have a directory structure of
`/home/woalk/git` for private projects,
with a subdirectory `work` for work projects.

So, we use
```bash
git identities update private --paths /home/woalk/git
git identities update work --paths /home/woalk/git/work
```
to set up our identity checks.

If we now want to commit something in our project
`/home/woalk/git/privateproject1`,
Git-Identities will ensure it is done with the `private` identity,
which means using `Woalk` as `user.name` and `woalk@example.com` as `user.email`.

If we now want to commit something in our project
`/home/woalk/git/work/topsecretproject1`,
Git-Identities will ensure it is done with the `work` identity,
which means using `Name Surname` as `user.name` and `surname@example.com` as `user.email`.

### Auto-applying

Git-Identities can automatically set the correct config from the settings.

This can either be done manually, by calling
```bash
git identities apply --auto
``` 
in the respective repository, or by calling
```bash
git id-clone <url> ...
```
instead of `git clone` when cloning a repository.
It will check the destination directory for the applying identity
and set it via directly when cloning.

It supports every argument that `git clone` supports, except `[<directory>]`.
See `man git clone` for details.

## Installation

### Script

Use the `install.sh` script from this directory.

It is a careful script that will tell you everything it will do
and provide you with a chance to review the changes before committing them.

After installation, Git-Identities is available via `git identities`,
assuming the main binary installation place chosen in the installation script was in your `PATH`.

### Installation place

It will ask you to move the checked-out repo into a system-wide directory before running the script.

On Linux systems, you can use, for example, `/opt`.
On macOS systems, you can use `/usr/local`, or `/usr/local/opt` if you have `brew` installed.

On Linux, you should `chown` the repo to `root:root` for security reasons.
On macOS, you can `chown` it to `root:wheel`, assuming you're ok with that if you have `brew` installed.

### Optional configuration

You can create additional Git alias commands for better access to Git-Identities, e.g.
```bash
git config alias.id identities
git config alias.ic id-clone
```
to access the commands via `git id` and `git ic`.

## Author & License

```
Copyright (C) 2018 Alexander Köster
https://woalk.com
```

```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use these files except in compliance with the License.
You may obtain a copy of the License in the file LICENSE in this
project or at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

If you build something better with it, I would love to know and get a PR, but it isn't mandatory. 
