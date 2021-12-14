import requests
import time
from datetime import datetime
from datetime import date

def get_date(url,branch): # date of last commit
    branch_url = url + "/" + branch
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", branch_url, headers=headers, data=payload)
    text = response.json()
    commit = text["commit"]
    commit = commit["commit"]
    commit = commit["committer"]
    return commit

def get_branches(url,token): # get a list of branches in repo
    try:
        payload={}
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        text = response.json()
        branch_list = []
        for dic in text:
            branch_list.append(dic["name"])
        return branch_list
    except requests.ConnectionError as e:
        print(e)

def local_time():
    l_time = date.today()
    return l_time

def get_time(commit):
    date = commit["date"]
    date = date[:date.find("T")]
    time = datetime.strptime(date, '%Y-%m-%d').date()
    return time

def get_name(commit):
    name = commit["name"]
    return name

def get_name_mail(commit):
    email = commit["email"]
    return email


if __name__ == '__main__':
    # python bin/02_CITests/06_deploy/api_branch_timeout.py
    repo = "SvenHinrichs/GitLabCI"
    url = "https://api.github.com/repos/" + repo + "/branches"
   
    CRED = '\033[91m'
    CEND = '\033[0m'
    green = "\033[0;32m"
    time_list = []
    l_time = local_time()
    list = get_branches(url, token)
    w_message = []
    e_message = []
    for branch in list:

        commit = get_date(url, branch)
        name = get_name(commit)
        email = get_name_mail(commit)
        print(f'Name: {name}')
        print(f'Email: {email}')
        time = get_time(commit)
        previous_date = str(l_time - time)
        if previous_date.find("days") > -1:
            time_dif = int(previous_date[:previous_date.find("days")])
            if time_dif > 180:
                print(f'Branch {branch}{CRED} is inactiv for more than 180 days {CEND}. Inactive for {time_dif} days.')
                e_message.append(branch)
            elif time_dif > 90:
                print(f'Branch {branch}{CRED} is inactiv for more than 90 days {CEND}. Inactive for {time_dif} days.')
                w_message.append(branch)
            else:
                print(f'Branch {branch} is since {time_dif} days inactive')

