## What is it?
The folder contains the following templates:

	- check_model.gitlab-ci.yml: Check models 
	- check_simulate.gitlab-ci.yml: simulate models 
	- regression_test.gitlab-ci.yml Regression test 
	- html_check.gitlab-ci.yml: html check and correct the html code
	- style_check.gitlab-ci.yml: check style of modelica models

## What is implemented? 
Add the following lines to your gitlab.ci.yml:
 

	#!/bin/bash
	image: registry.git.rwth-aachen.de/ebc/ebc_intern/dymola-docker:miniconda-latest

	stages:
		- build
		- HTMLCheck
		- openMR
		- deploy
		- StyleCheck
		- Check
		- Simulate
		- RegressionTest

	include:
		- project: 'EBC/EBC_all/gitlab_ci/templates'
		- file: 'bin/05_Templates/check_model.gitlab-ci.yml'
		- project: 'EBC/EBC_all/gitlab_ci/templates'
		- file: 'bin/05_Templates/check_simulate.gitlab-ci.yml'
		- project: 'EBC/EBC_all/gitlab_ci/templates'
		- file: 'bin/05_Templates/regression_test.gitlab-ci.yml'
		- project: 'EBC/EBC_all/gitlab_ci/templates'
		- file: 'bin/05_Templates/html_check.gitlab-ci.yml'
		- project: 'EBC/EBC_all/gitlab_ci/templates'
		- file: 'bin/05_Templates/style_check.gitlab-ci.yml'

## What is done?
- Simulate and check models
- Regressiontest
- Check and correct the html code
- Check the style of the models in AixLib
