#!/usr/bin/env bash

#Usage: ./commit.sh "commit message"
# adding files needs to be done separately
#unset GIT_DIR
cd ../../raghavkhanna.github.io
git add .
git commit -m "$1"
cd ..
git add .
git commit -m "$1"
git push --recurse-submodules=on-demand