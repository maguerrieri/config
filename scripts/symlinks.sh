if [[ "$#" -ne 1 ]];
then
    cloud="db"
else
    cloud=$1
fi

ln -s "/Users/marioguerrieri/$cloud/tech/config/profile/bash_profile" "/Users/marioguerrieri/.bash_profile"
ln -s "/Users/marioguerrieri/$cloud/tech/config/profile/code.json" "/Users/marioguerrieri/Library/Application Support/Code/User/settings.json"
ln -s "/Users/marioguerrieri/$cloud/tech/config/profile/code_keybindings.json" "/Users/marioguerrieri/Library/Application Support/Code/User/keybindings.json"
ln -s "/Users/marioguerrieri/$cloud/tech/config/profile/git" "/Users/marioguerrieri/.gitconfig"
