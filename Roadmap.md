# Roadmap CI Tests

## Main goals

* Return Feedback to user
  * Pipeline status (success, error)
  * extended log on page
  * log summary with forwarder
  
* Give user hints how to use pipeline

* Interactive pipeline
  * show failed plots/regression tests
  * on reviewer assigned publish to do list to PR


* Create Repo for GitHub actions (similar to gitlab templates repo)


## Triggers

* Merge-Requests (checks)
* Merge (results)
  * e.g. version, new models, ...

## CI Jobs

* pylint
  * future score (should be higher)
* fmi? (modelica lint)
* conventional-release
* coverage (modelica/python)

## Forwarders

* Merge-Request commit message
* Slack
* (Mail)
