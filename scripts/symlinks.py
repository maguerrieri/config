#!/usr/bin/env python3

from typing import List, Tuple, Union

import sys
import os
import argparse

from pathlib import PureWindowsPath

parser = argparse.ArgumentParser("Set up your symlinks")
parser.add_argument("--cloud")
parser.add_argument("--shortcloud")

args = parser.parse_args()
cloud = args.cloud or "icloud"
shortcloud = args.shortcloud or cloud

class UnsupportedPlatformException(Exception):
    pass

is_wsl = len(os.popen("which cmd.exe").readline().strip()) > 0

def home_path() -> str:
    posix_path = os.path.expandvars("$HOME")
    if os.path.exists(posix_path) and not is_wsl:
        return posix_path

    wsl_path = os.popen("wslpath $(cmd.exe /C \"echo %USERPROFILE%\")").readline().strip()
    if os.path.exists(wsl_path):
        return wsl_path
    
    raise UnsupportedPlatformException()
home_path = home_path()
print(f"Home directory: {home_path}")

def cloud_path() -> str:
    macos_path = "$HOME/Library/Mobile Documents/com~apple~CloudDocs"
    if os.path.exists(macos_path):
        return macos_path

    wsl_path = os.path.join(home_path, cloud)
    if os.path.exists(wsl_path):
        return wsl_path
    
    raise FileNotFoundError(f"Can't find cloud directory named {cloud}")
cloud_path = cloud_path()
print(f"Cloud path: {cloud_path}")

wsl_root_path = "/mnt/c"
def root_relative_wsl_path(path: str):
    if path.startswith(wsl_root_path):
        return path[len(wsl_root_path):]
    else:
        return path

def code_settings_path() -> str:
    macos_path = os.path.join(home_path, "Library", "Application Support", "Code", "User")
    if os.path.exists(macos_path):
        return macos_path
    
    wsl_path = os.path.join(home_path, "AppData", "Roaming", "Code", "User")
    if os.path.exists(wsl_path):
        return wsl_path

    raise FileNotFoundError("Can't find Visual Studio Code settings")
code_settings_path = code_settings_path()
print(f"Visual Studio Code settings: {code_settings_path}")

def make_symlink(target: str, source: str, use_mklink=False):
    if use_mklink:
        cmd_path = os.popen("which cmd.exe").readline().strip()
        if len(cmd_path) > 0:
            win_source = "C:" / PureWindowsPath(root_relative_wsl_path(source))
            win_target = "C:" / PureWindowsPath(root_relative_wsl_path(target))

            os.system(f"cmd.exe /C \"mklink {win_source} {win_target}\"")
            return
    
    os.symlink(target, source)

links: List[Tuple[str, str, List[str], bool]] = [
    (f"{cloud_path}", f"$HOME/{shortcloud}", None, False),
    (f"{cloud_path}/tech", "$HOME/tech", None, False),
    (f"{cloud_path}/tech/config/profile/bash_profile", "$HOME/.bash_profile", None, False),
    (f"{cloud_path}/tech/config/profile/zshrc", "$HOME/.zshrc", None, False),
    (f"{cloud_path}/tech/config/profile/code.json", f"{code_settings_path}/settings.json", None, True),
    (f"{cloud_path}/tech/config/profile/code_keybindings.json", f"{code_settings_path}/keybindings.json", None, True),
    (f"{cloud_path}/tech/config/profile/git", "$HOME/.gitconfig", None, False),
    (f"{cloud_path}/tech/config/profile/gitignore", "$HOME/.gitignore_global", None, False),
    (
        f"{cloud_path}/tech/config/profile/windows-terminal.json",
        f"{home_path}/AppData/Local/Packages/Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/settings.json",
        ['wsl'], 
        True
    ),
]

for (target, name, platforms, mklink_if_wsl) in links:
    if not (platforms is None
            or sys.platform in platforms and not is_wsl
            or "wsl" in platforms and is_wsl):
        continue

    expanded_target = os.path.expandvars(target).format(**locals())
    expanded_name = os.path.expandvars(name).format(**locals())

    if os.path.islink(expanded_name):
        print(f"Deleting existing symlink `{expanded_name}`.")
        os.unlink(expanded_name)
    elif os.path.exists(expanded_name):
        backup = os.path.join(os.path.dirname(expanded_name), f"_{os.path.basename(expanded_name)}")
        print(f"Moving existing `{expanded_name}` to `{backup}`.")
        if not os.path.exists(backup):
            os.rename(expanded_name, backup)
        else:
            print(f"`{backup}` also exists; aborting.")
            sys.exit()
    
    print(f"Linking `{expanded_name}` -> `{expanded_target}`.")
    make_symlink(expanded_target, expanded_name, mklink_if_wsl)
