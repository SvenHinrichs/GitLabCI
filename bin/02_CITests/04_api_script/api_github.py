import requests
import json
import argparse
import os
import sys 


class GET_API_GITHUB(object):

	def __init__(self, github_repo, working_branch):
		self.github_repo = github_repo
		self.working_branch = working_branch

	def _get_pr_number(self):
		url = f'https://api.github.com/repos/{self.github_repo}/pulls'
		payload = {}
		headers = {
			'Content-Type': 'application/json'
		}
		response = requests.request("GET", url, headers=headers, data=payload)
		pull_request_json = response.json()
		for pull in pull_request_json:
			name = pull["head"].get("ref")
			if name == self.working_branch:
				return pull["number"]

	def _get_github_username(self):
		url = "https://api.github.com/repos/" + self.GITHUB_REPOSITORY + "/branches/" + self.Working_Branch
		payload = {}
		headers = {}
		response = requests.request("GET", url, headers=headers, data=payload)
		branch = response.json()
		commit = branch["commit"]
		author = commit["author"]
		login = author["login"]
		return login

	def return_owner(self):
		owner = self.GITHUB_REPOSITORY
		owner = owner.split("/")
		print(owner[0])
		return owner[0]

class PULL_REQUEST_GITHUB(object):
	
	def __init__(self, github_repo, working_branch,  github_token):
		self.github_repo = github_repo
		self.working_branch = working_branch
		self.github_token = github_token
		self.correct_branch = f'Correct_HTML_{self.working_branch}'
	
	def _post_comment_IBBSA_merge(self, owner):
		url = f'https://api.github.com/repos/{self.github_repo}/pulls'
		payload = '{\n    \"title\": \"IBPSA Merge ' + self.working_branch + '\",\n    \"body\": \"**Following you will find the instructions for the IBPSA merge:**\\n  1. Please pull this branch IBPSA_Merge to your local repository.\\n 2. As an additional saftey check please open the AixLib library in dymola and check whether errors due to false package orders may have occurred. You do not need to translate the whole library or simulate any models. This was already done by the CI.\\n 3. If you need to fix bugs or perform changes to the models of the AixLib, push these changes using this commit message to prevent to run the automatic IBPSA merge again: **`fix errors manually`**. \\n  4. You can also output the different reference files between the IBPSA and the AixLib using the CI or perform an automatic update of the referent files which lead to problems. To do this, use one of the following commit messages \\n  **`Trigger CI - give different reference results`** \\n  **`Trigger CI - Update reference results`** \\n The CI outputs the reference files as artifacts in GitLab. To find them go to the triggered pipeline git GitLab and find the artifacts as download on the right site. \\n 5. If the tests in the CI have passed successfully, merge the branch IBPSA_Merge to development branch. **Delete** the Branch ' + self.correct_branch + '\",\n    \"head\": \"' + self.OWNER + ':' + self.correct_branch + '\",\n    \"base\": \"' + self.working_branch + '\"\n  \n}'
		headers = {
			'Authorization': 'Bearer '+self.github_token,
			'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data = payload)
		return response

	def _post_pr_correct_html(self, owner):
		url = "https://api.github.com/repos/" + self.github_repo + "/pulls"
		payload = '{\n    \"title\": \"Corrected HTML Code in branch ' + self.working_branch + '\",\n    \"body\": \"Merge the corrected HTML Code. After confirm the pull request, **pull** your branch to your local repository. **Delete** the Branch ' + self.correct_branch + '\",\n    \"head\": \"' + owner + ':' + self.correct_branch + '\",\n    \"base\": \"' + self.working_branch + '\"\n  \n}'
		headers = {
			'Authorization': 'Bearer ' + self.github_token,
			'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		print(response.text.encode('utf8'))

	def _post_comment_correct_html(self, owner):
		url = "https://api.github.com/repos/" + self.github_repo + "/pulls"
		payload = '{\n    \"title\": \"Corrected HTML Code in branch ' + self.working_branch + '\",\n    \"body\": \"Merge the corrected HTML Code. After confirm the pull request, **pull** your branch to your local repository. **Delete** the Branch ' + self.correct_branch + '\",\n    \"head\": \"' + owner + ':' + self.correct_branch + '\",\n    \"base\": \"' + self.working_branch + '\"\n  \n}'
		headers = {
			'Authorization': 'Bearer ' + self.github_token,
			'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		print(response.text.encode('utf8'))

	def _update_pr_assignees_correct_html(self, pr_number, assignees_owner):
		url = "https://api.github.com/repos/" + self.github_repo + "/issues/" + str(pr_number)
		payload = '{ \"assignees\": [\r\n    \"' + assignees_owner + '\"\r\n  ],\r\n    \"labels\": [\r\n    \"CI\", \r\n    \"Correct HTML\"\r\n    \r\n  ]\r\n}'
		headers = {
			'Authorization': 'Bearer ' + self.github_token,
			'Content-Type': 'application/json'
		}
		response = requests.request("PATCH", url, headers=headers, data=payload)
		print("User " + assignees_owner + " assignee to pull request Number " + str(pr_number))

	def _update_pr_assignees_IPBSA_Merge(self, pr_number, assignees_owner):
		url = f'https://api.github.com/repos/{self.github_repo}/issues/{str(pr_number)}'
		payload = '{ \"assignees\": [\r\n    \"'+assignees_owner+'\"\r\n  ],\r\n    \"labels\": [\r\n    \"CI\", \r\n    \"IBPSA_Merge\"\r\n    \r\n  ]\r\n}'
		headers = {
		  'Authorization': 'Bearer '+ self.github_token,
		  'Content-Type': 'application/json'
		}
		response = requests.request("PATCH", url, headers=headers, data = payload)
		print(f'User {assignees_owner} assignee to pull request Number {str(pr_number)}')


	def _post_comment_regression(self, pr_number):
		url = f'https://api.github.com/repos/{self.github_repo}/issues/{str(pr_number)}/comments'
		message = f'Errors in regression test. Compare the results on the following page\\n {page_url}'
		payload = "{\"body\":\"" + message + "\"}"
		headers = {
			'Authorization': 'Bearer ' + self.github_token,
			'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		print(response.text)
	def _post_comment_show_plots(self, pr_number):
		url = f'https://api.github.com/repos/{self.github_repo}/issues/{str(pr_number)}/comments'
		message = f'Reference results have been displayed graphically and are created under the following page {page_url}'
		payload = "{\"body\":\"" + message + "\"}"
		headers = {
			'Authorization': 'Bearer ' + self.github_token,
			'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		print(response.text)


	


if  __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Set Github Environment Variables")  # Configure the argument parser
	check_test_group = parser.add_argument_group("Arguments to set Environment Variables")
	check_test_group.add_argument("-CB", "--correct-branch", default ="${Newbranch}", help="Branch to correct your Code")
	check_test_group.add_argument("-GR", "--github-repo", default="RWTH-EBC/AixLib", help="Environment Variable owner/RepositoryName" )
	check_test_group.add_argument('-WB',"--working-branch",default="${TARGET_BRANCH}", help="Your current working Branch")
	check_test_group.add_argument('-GT',"--github-token",default="${GITHUB_API_TOKEN}", help="Your Set GITHUB Token")
	check_test_group.add_argument("--prepare-plot", help="Plot new models with new created reference files", action="store_true")
	check_test_group.add_argument("--show-plot", help="Plot new models with new created reference files",
								  action="store_true")
	check_test_group.add_argument("--post-pr-comment", help="Plot new models with new created reference files",
								  action="store_true")
	check_test_group.add_argument("--create-pr", help="Plot new models with new created reference files",
								  action="store_true")
	check_test_group.add_argument("--correct-html", help="Plot new models with new created reference files",
								  action="store_true")
	check_test_group.add_argument("--merge-request", help="Comment for a IBPSA Merge request",  action="store_true")
	check_test_group.add_argument('-GP', "--gitlab-page", default="${GITLAB_Page}", help="Set your gitlab page url")
	args = parser.parse_args()  # Parse the arguments

	from api_github import GET_API_GITHUB
	from api_github import PULL_REQUEST_GITHUB

	if args.post_pr_comment is True:
		get_api = GET_API_GITHUB(github_repo=args.github_repo, working_branch=args.working_branch)
		pr_number = get_api._get_pr_number()
		print(f'Setting pull request number: {pr_number}')
		page_url = f'{args.gitlab_page}/{args.working_branch}/plots'
		print(f'Setting gitlab page url: {page_url}')
		pull_request = PULL_REQUEST_GITHUB(github_repo=args.github_repo, working_branch=args.working_branch,
										   github_token=args.github_token)
		if args.prepare_plot is True:
			pull_request._post_comment_regression(pr_number, page_url)
		if args.show_plot is True:
			pull_request._post_comment_show_plots(pr_number, page_url)
	if args.create_pr is True:
		if args.correct_html is True:
			pull_request = PULL_REQUEST_GITHUB(github_repo=args.github_repo, working_branch=args.working_branch,
											   github_token=args.github_token)
			get_api = GET_API_GITHUB(github_repo=args.github_repo, working_branch=args.working_branch)
			owner = get_api.return_owner()
			pr_response = pull_request._post_pr_correct_html(owner)
			pr_number = pull_request._get_pr_number()
			print(f'Setting pull request number: {pr_number}')
			assignees_owner = GET_API_DATA.get_GitHub_Username()
			pull_request._update_pr_assignees_correct_html(pr_number, assignees_owner)
			exit(0)