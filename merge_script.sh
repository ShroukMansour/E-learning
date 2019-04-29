#!/bin/bash -e



export GIT_COMMITTER_EMAIL='shroukmansour99@gmail.com'
export GIT_COMMITTER_NAME='ShroukMansour'
export GIT_COMMITTER_PASSWORD='da75664bca798621d5a3b8398d44465a7ee2c06f'

printf '1>>>>>>>>>>>>>.\n'
git config --add remote.origin.fetch +refs/heads/*:refs/remotes/origin/* || exit
git fetch --all || exit

printf '\nb2>>>>>>>>>>>>>>'
git checkout master || exit
git merge --no-ff origin/For-testing || exit

printf '3>>>>>>>>>\n'
git push https://da75664bca798621d5a3b8398d44465a7ee2c06f@github.com/ShroukMansour/E-learning.git

printf '4>>>>>>>>>>>>n'
