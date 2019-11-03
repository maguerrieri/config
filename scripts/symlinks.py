#!/usr/bin/env python3

import sys
import os

links = {
    "$HOME/tech/config/profile/bash_profile": "$HOME/.bash_profile",
    "$HOME/tech/config/profile/zshrc": "$HOME/.zshrc",
    "$HOME/tech/config/profile/code.json" :"$HOME/Library/Application Support/Code/User/settings.json",
    "$HOME/tech/config/profile/code_keybindings.json": "$HOME/Library/Application Support/Code/User/keybindings.json",
    "$HOME/tech/config/profile/git": "$HOME/.gitconfig",
    "$HOME/tech/config/profile/gitignore": "$HOME/.gitignore_global",
}
for (target, name) in links.items():
    expanded_target = os.path.expandvars(target)
    expanded_name = os.path.expandvars(name)

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
    
    os.symlink(expanded_target, expanded_name)
    print(f"Linking `{expanded_name}` -> `{expanded_target}`.")
