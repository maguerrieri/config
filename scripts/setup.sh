#!/bin/bash

sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

./symlinks.py

chflags hidden $HOME/Dropbox*
chflags -h hidden $HOME/icloud
