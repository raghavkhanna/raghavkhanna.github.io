#!/usr/bin/env bash

#Usage: ./commit.sh "commit message"
# adding files needs to be done separately
cd ../raghavkhanna.github.io
git commit -am $1
cd ..
git commit -am $1
git push --recurse-submodules=on-demand