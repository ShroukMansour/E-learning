#!/bin/bash -e



export GIT_COMMITTER_EMAIL='shroukmansour99@gmail.com'
export GIT_COMMITTER_NAME='ShroukMansour'

printf '1>>>>>>>>>>>>>.\n'
git config --add remote.origin.fetch +refs/heads/*:refs/remotes/origin/* || exit
git fetch --all || exit

printf '\nb2>>>>>>>>>>>>>>'
git checkout For-testing || exit
git merge --no-ff "travis commit" || exit

printf '3>>>>>>>>>\n'
git push @github.com/">https://b535aecee130bd3bac42ea289baa5b3453f88c00@github.com/ShroukMansour/E-learning.git"

printf '4>>>>>>>>>>>>n'
