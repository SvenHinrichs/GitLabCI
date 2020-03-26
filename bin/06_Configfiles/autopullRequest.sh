curl --location --request POST 'https://api.github.com/repos/SvenHinrichs/GitLabCI/pulls' \
--header 'Authorization: Bearer 5378e2d460f76f2dbc6bd01dac6e64dc559fe6f5' \
--header 'Content-Type: text/plain' \
--data-raw '{
  "title": "Amazing new feature",
  "body": "Please pull these awesome changes in!",
  "head": "SvenHinrichs:test-branch",
  "base": "master"
}'

Create a new Branch

curl --location --request POST 'https://api.github.com/repos/SvenHinrichs/GitLabCI/git/refs' \
--header 'Authorization: Bearer 5378e2d460f76f2dbc6bd01dac6e64dc559fe6f5' \
--header 'Content-Type: application/json' \
--data-raw '{
    "ref": "refs/heads/api-branch",
    "sha": "15af51cae721478010bd60d76ebc5d4082ebcdd7"
}'


https://api.github.com/repos/SvenHinrichs/GitLabCI/git/refs/heads/api-branch
{
    "ref": "refs/heads/api-branch",
    "node_id": "MDM6UmVmMTYyNDE1ODU3OmFwaS1icmFuY2g=",
    "url": "https://api.github.com/repos/SvenHinrichs/GitLabCI/git/refs/heads/api-branch",
    "object": {
        "sha": "15af51cae721478010bd60d76ebc5d4082ebcdd7",
        "type": "commit",
        "url": "https://api.github.com/repos/SvenHinrichs/GitLabCI/git/commits/15af51cae721478010bd60d76ebc5d4082ebcdd7"
    }
}

DELETE Branch

curl --location --request DELETE 'https://api.github.com/repos/SvenHinrichs/GitLabCI/git/refs/heads/api-branch' \
--header 'Authorization: Bearer 5378e2d460f76f2dbc6bd01dac6e64dc559fe6f5' \
--header 'Content-Type: application/json' \
--data-raw '{
    "ref": "refs/heads/api-branch",
    "sha": "15af51cae721478010bd60d76ebc5d4082ebcdd7"
}'

[
    {
        "name": "issue802_CleanCI_Infrastructure",
        "commit": {
            "sha": "15af51cae721478010bd60d76ebc5d4082ebcdd7",
            "url": "https://api.github.com/repos/SvenHinrichs/GitLabCI/commits/15af51cae721478010bd60d76ebc5d4082ebcdd7"
        },
        "protected": false,
        "protection": {
            "enabled": false,
            "required_status_checks": {
                "enforcement_level": "off",
                "contexts": []
            }
        },
        "protection_url": "https://api.github.com/repos/SvenHinrichs/GitLabCI/branches/issue802_CleanCI_Infrastructure/protection"
    },
    {
        "name": "master",
        "commit": {
            "sha": "843f09694430e63f333b04b9b562296142f679f4",
            "url": "https://api.github.com/repos/SvenHinrichs/GitLabCI/commits/843f09694430e63f333b04b9b562296142f679f4"
        },
        "protected": false,
        "protection": {
            "enabled": false,
            "required_status_checks": {
                "enforcement_level": "off",
                "contexts": []
            }
        },
        "protection_url": "https://api.github.com/repos/SvenHinrichs/GitLabCI/branches/master/protection"
    },
    {
        "name": "test-branch",
        "commit": {
            "sha": "54aaf3c88731a665a2e6abab8f5d93b70f75bc43",
            "url": "https://api.github.com/repos/SvenHinrichs/GitLabCI/commits/54aaf3c88731a665a2e6abab8f5d93b70f75bc43"
        },
        "protected": false,
        "protection": {
            "enabled": false,
            "required_status_checks": {
                "enforcement_level": "off",
                "contexts": []
            }
        },
        "protection_url": "https://api.github.com/repos/SvenHinrichs/GitLabCI/branches/test-branch/protection"
    }
]