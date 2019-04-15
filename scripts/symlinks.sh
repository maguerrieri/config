if [[ "$#" -ne 1 ]];
then
    cloud=""
else
    cloud=$1
fi

gln -s "$HOME/$cloud/tech/config/profile/bash_profile" "$HOME/.bash_profile"
gln -s "$HOME/$cloud/tech/config/profile/code.json" "$HOME/Library/Application Support/Code/User/settings.json"
gln -s "$HOME/$cloud/tech/config/profile/code_keybindings.json" "$HOME/Library/Application Support/Code/User/keybindings.json"
gln -s "$HOME/$cloud/tech/config/profile/git" "$HOME/.gitconfig"
gln -s "$HOME/$cloud/tech/config/profile/gitignore" "$HOME/.gitignore_global"
