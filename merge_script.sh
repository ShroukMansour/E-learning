#!/bin/bash -e


export GIT_COMMITTER_EMAIL='travis@travis'
export GIT_COMMITTER_NAME='Travis CI'

printf 'Removing staging branch as it has been handled already\n'
printf 'git push %s :staging >/dev/null 2>&1\n' "ShroukMansour/E-learning"
push_uri="https://b535aecee130bd3bac42ea289baa5b3453f88c00@github.com/ShroukMansour/E-learning"
git push "$push_uri" :staging >/dev/null 2>&1

# Preparing for merge
git checkout staging
git config user.email "shroukmansour99@gmail.com"
git config user.name "ShroukMansour"

printf 'Pulling develop\n' >&2
git fetch origin +develop:develop
git merge develop --no-edit