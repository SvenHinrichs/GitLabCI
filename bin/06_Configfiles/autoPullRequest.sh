#!/usr/bin/env bash
set -e


echo "Create a Pull request ${Newbranch} to ${TARGET_BRANCH}"
echo $GITHUB_API_TOKEN

curl -X POST "https://api.github.com/repos/SvenHinrichs/GitLabCI/pulls" \
	--header "Authorization:Bearer ${GITHUB_API_TOKEN}" \
	--header "Content-Type: application/json" \
	--data "{
		\"title\": \"HTML Correction\",
		\"body\": \"Merge the Corrected HTML Code\",
		\"head\": \"SvenHinrichs:${Newbranch}\",
		\"base\": \"${TARGET_BRANCH}\"
}"

echo "Create pull request. Merge ${Newbranch} into ${TARGET_BRANCH}."
exit 0 
