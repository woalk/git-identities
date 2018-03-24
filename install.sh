#!/usr/bin/env bash

echo "git-identities Install script"
echo "(C) 2018 woalk"

if [ ! -z "$1" ] && [ "$1" != "--no-sudo" ]; then
    echo -e "\e[0;31mInvalid arguments.\e[0;39m" >&2
    exit 2
fi

echo
echo "Before running this, you should move this repository to a location that is available system-wide."
echo "It will allow you to update git-identities via Git without reinstalling."
echo "Press [ENTER] to continue or ^C at any time to cancel."
read

NO_SUDO=`if [ "$1" == "--no-sudo" ]; then echo 1; else echo 0; fi`
DO_SUDO=0

if [ "`id -u`" -ne "0" ] && [ ${NO_SUDO} -eq 0 ]; then
    DO_SUDO=1
    echo "Info: You are not root."
    echo "If you don't have \`sudo', you may need to run this script as root, or supply \`--no-sudo'."
    echo
fi

if [ ! -e "./git_identities.py" ]; then
    echo -e "\e[0;31mPlease run this script from the directory with the \`git-identities' files.\e[0;39m" >&2
    exit 1
fi

INSTALL_DIR="/usr/local/bin"

echo -e "We will symlink the main binary into \e[1m${INSTALL_DIR}/\e[0mgit-identities\e[0m"
echo "Enter another directory path (in your PATH), or press [ENTER] to use the displayed path: "

read INSTALL_DIR_OVERRIDE
echo
if [ ! -z ${INSTALL_DIR_OVERRIDE} ]; then
    INSTALL_DIR=${INSTALL_DIR_OVERRIDE}
fi

GIT_CONFIG_SCOPE="system-wide"
GIT_CONFIG_COMMAND_SCOPE="--system"
if [ ${NO_SUDO} -eq 1 ]; then
    GIT_CONFIG_SCOPE="user-global"
    GIT_CONFIG_COMMAND_SCOPE="--global"
fi

CURRENT_HOOK_DIR=`git config ${GIT_CONFIG_COMMAND_SCOPE} --get core.hooksDir`
if [ ! -z "${CURRENT_HOOK_DIR}" ]; then
    echo -e "\e[0;33mWarning:\e[0;39m You already have a ${GIT_CONFIG_SCOPE} Git config core.hooksDir."
    echo "Please remove it with"
    echo "   git config ${GIT_CONFIG_COMMAND_SCOPE} --unset core.hooksDir"
    echo "if you don't use it before proceeding."
    echo "If you do use it, either add"
    echo -e "   python3 \"`pwd`/hooks/checks.py\"\n   IDENTITY_RETURN=\$?\n   if [ \$IDENTITY_RETURN -ne 0 ]; then\n    exit \$IDENTITY_RETURN\n   fi"
    echo "to your existing \`pre-commit' hook with proper return code, or symlink"
    echo "   ln -s \"`pwd`/hooks/checks.py\" \"${CURRENT_HOOK_DIR}/pre-commit\""
    echo "if you don't use a pre-commit hook yet."
    echo "Press [ENTER] to continue or ^C to cancel."
    read
else
    echo -e "We will set the ${GIT_CONFIG_SCOPE} Git config to have a \e[1mhooksDir\e[0m to \e[1m`pwd`/hooks\e[0m"
fi

PREFIX_CMD="sudo "
if [ ${DO_SUDO} -eq 0 ]; then
    PREFIX_CMD=""
fi

echo
echo "By pressing [ENTER], you agree with the mentioned changes to your system."
read

${PREFIX_CMD}ln -s "`pwd`/git_identities.py" "${INSTALL_DIR}/git-identities"
if [ $? -ne 0 ]; then
    echo -e "\e[0;31mError:\e[0;39m Couldn't create symlink."
    exit 3
fi

if [ -z "${CURRENT_HOOK_DIR}" ]; then
    ${PREFIX_CMD}git config ${GIT_CONFIG_COMMAND_SCOPE} core.hooksDir "`pwd`/hooks"
    if [ $? -ne 0 ]; then
        echo -e "\e[0;31mError:\e[0;39m Couldn't change Git config."
        exit 4
    fi
fi

echo "Install successful."
echo "Try it out now by calling \`git identities list'."
exit 0
