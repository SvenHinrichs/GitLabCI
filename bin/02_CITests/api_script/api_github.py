import requests
import json
import argparse
import os
import sys


class GET_API_GITHUB(object):

    def __init__(self, Correct_Branch, GITHUB_REPOSITORY, Working_Branch):
        self.GITHUB_REPOSITORY = GITHUB_REPOSITORY
        self.Correct_Branch = Correct_Branch
        self.Working_Branch = Working_Branch

    def _jprint(self):  # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)

    def _get_github_username(self):
        url = f'https://api.github.com/repos/{self.GITHUB_REPOSITORY}/branches/{self.Working_Branch}'
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        branch = response.json()
        commit = branch["commit"]
        author = commit["author"]
        login = author["login"]
        return login

    def _return_owner(self):
        owner = self.GITHUB_REPOSITORY
        owner = owner.split("/")
        print(owner[0])
        return owner[0]


class PULL_REQUEST_GITHUB(object):

    def __init__(self, Correct_Branch, GITHUB_REPOSITORY, Working_Branch, OWNER, GITHUB_TOKEN):
        self.GITHUB_REPOSITORY = GITHUB_REPOSITORY
        self.Correct_Branch = Correct_Branch
        self.Working_Branch = Working_Branch
        self.GITHUB_TOKEN = GITHUB_TOKEN
        self.OWNER = OWNER

    def _post_pull_request(self):
        url = "https://api.github.com/repos/" + self.GITHUB_REPOSITORY + "/pulls"
        payload = '{\n    \"title\": \"Corrected HTML Code in branch ' + self.Working_Branch + '\",\n    \"body\": \"Merge the corrected HTML Code. After confirm the pull request, **pull** your branch to your local repository. **Delete** the Branch ' + self.Correct_Branch + '\",\n    \"head\": \"' + self.OWNER + ':' + self.Correct_Branch + '\",\n    \"base\": \"' + self.Working_Branch + '\"\n  \n}'
        headers = {
            'Authorization': 'Bearer ' + self.GITHUB_TOKEN,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text.encode('utf8'))
        return response

    def _get_pull_request_number(self, pull_request_response):  # returns the number of the pull request from your working branch
        pull_request_number = pull_request_response.json()
        pull_request_number = pull_request_number["number"]
        print(f' Pull request number: {pull_request_number}')
        return pull_request_number

    def _update_pull_request_assignees(self, pull_request_number, assignees_owner):
        url = f'https://api.github.com/repos/{self.GITHUB_REPOSITORY }/issues/{str(pull_request_number)}'
        payload = '{ \"assignees\": [\r\n    \"' + assignees_owner + '\"\r\n  ],\r\n    \"labels\": [\r\n    \"CI\", \r\n    \"Correct HTML\"\r\n    \r\n  ]\r\n}'
        headers = {
            'Authorization': 'Bearer ' + self.GITHUB_TOKEN,
            'Content-Type': 'application/json'
        }
        response = requests.request("PATCH", url, headers=headers, data=payload)
        print(f'User {assignees_owner} assignee to pull request Number {str(pull_request_number)}')


if __name__ == '__main__':
    # python api.py --GITHUB-REPOSITORY SvenHinrichs/GitLabCI --Working-Branch master
    parser = argparse.ArgumentParser(description="Set Github Environment Variables")  # Configure the argument parser
    check_test_group = parser.add_argument_group("Arguments to set Environment Variables")
    check_test_group.add_argument("-CB", "--Correct-Branch", default="${Newbranch}", help="Branch to correct your Code")
    check_test_group.add_argument("-GR", "--GITHUB-REPOSITORY", default="RWTH-EBC/AixLib",
                                  help="Environment Variable owner/RepositoryName")
    check_test_group.add_argument('-WB', "--Working-Branch", default="${TARGET_BRANCH}",
                                  help="Your current working Branch")
    check_test_group.add_argument('-GT', "--GITHUB-TOKEN", default="${GITHUB_API_TOKEN}", help="Your Set GITHUB Token")
    check_test_group.add_argument("--show-ref",
                                 help='Plot only model',
                                 action="store_true")
    args = parser.parse_args()  # Parse the arguments

    GET_API_DATA = GET_API_GITHUB(GITHUB_REPOSITORY=args.GITHUB_REPOSITORY, Correct_Branch=args.Correct_Branch,
                                  Working_Branch=args.Working_Branch)
    owner = GET_API_DATA._return_owner()
    PULL_REQUEST = PULL_REQUEST_GITHUB(GITHUB_REPOSITORY=args.GITHUB_REPOSITORY, Correct_Branch=args.Correct_Branch,
                                       Working_Branch=args.Working_Branch, GITHUB_TOKEN=args.GITHUB_TOKEN, OWNER=owner)
    pull_request_response = PULL_REQUEST.post_pull_request()
    pull_request_number = PULL_REQUEST.get_pull_request_number(pull_request_response)
    assignees_owner = GET_API_DATA._get_github_username()
    PULL_REQUEST.update_pull_request_assignees(pull_request_number, assignees_owner)
    exit(0)
