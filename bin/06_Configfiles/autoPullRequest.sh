#!/usr/bin/env bash
set -e


echo "Create a Pull Request ${Newbranch} to ${TARGET_BRANCH}"

curl --location --request POST 'https://api.github.com/repos/SvenHinrichs/GitLabCI/pulls' \
--header 'Authorization: Bearer ${GITHUB_API_TOKEN}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "HTML Correction",
    "body": "Please pull these awesome changes in!",
    "head": "SvenHinrichs:${Newbranch}",
    "base": "${TARGET_BRANCH}"
}'