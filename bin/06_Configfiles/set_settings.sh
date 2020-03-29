#!/usr/bin/env bash
set -e



echo "Set settings to your current branch and repository"




curl --location --request GET 'https://api.github.com/repos/SvenHinrichs/GitLabCI' \
--header 'PRIVATE-TOKEN: 9zTXu9p8xxRwVRJyWhrM' \
