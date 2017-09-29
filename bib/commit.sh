#!/usr/bin/env bash

#Usage: ./commit.sh "commit message"
# adding files needs to be done separately
#unset GIT_DIR
cd ../../raghavkhanna.github.io
git status
#git commit -am $1
cd ..
git status
#git status
#git commit -am $1
#git push --recurse-submodules=on-demand