#!/usr/bin/env bash
#POST /repos/:owner/:repo/pulls
#{
#  "title": "Amazing new feature",
#  "body": "Please pull these awesome changes in!",
#  "head": "username:branch",
#  "base": "TARGET_BRANCH"
#}
set -e


echo "Create a Pull request ${Newbranch} to ${TARGET_BRANCH}"


curl -X POST "https://api.github.com/repos/${Github_Repository}/pulls" \
	--header "Authorization:Bearer ${GITHUB_API_TOKEN}" \
	--header "Content-Type: application/json" \
	--data "{
		\"title\": \"Merge the corrected HTML Code in branch ${TARGET_BRANCH}\",
		\"body\": \"Merge the corrected HTML Code. After confirm the pull request, **pull** your branch to your local repository.\",
		\"head\": \"${GITLAB_USER_NAME}:${Newbranch}\",
		\"base\": \"${TARGET_BRANCH}\"
}"

echo "Create pull request. Merge ${Newbranch} into ${TARGET_BRANCH}. "
exit 0 
