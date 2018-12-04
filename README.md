# snaplyzer
AcloudGuru beginner python - aws snapshot + boto3

## About
use boto3 to manage AWS EC2

## Configuration
1. run these in pipenv
2. install boto3 on pipenv
3. configure aws cli 'adding profile'.
4. test script with ipython in pipenv

## Running

pipenv run python snaplyzer/snaplyzer.py <command> <subcommand> <--project=PROJECT>

*command* instances, volumes, snapshots
*subcommand* - pipenv run python snaplyzer/snaplyzer.py <command> --help
*project* optional.  It will filter out the tag from AWS