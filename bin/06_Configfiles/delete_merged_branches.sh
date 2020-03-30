#!/usr/bin/env bash

#Note: 	DELETE /projects/:id/repository/branches/:branch

set -e


curl --request DELETE 
	--header "PRIVATE-TOKEN:${GL_TOKEN}"
	https://gitlab.example.com/api/v4/projects/}${CI_PROJECT_ID}/repository/branches/${Newbranch}