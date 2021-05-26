# test-python-aws-script

## Setup
  - install docker in server.
  - make .env file with own environment variables based on .env.template.
  - docker build
      `docker build -t <docker image name> .`
  - docker run `docker run [-e "CRON_TIME=<minutes>"] --env-file=<env-filename> -it <docker image name>`
     CRON_TIME is the delaying minutes to iterate this script's excuting.
     default value is 5(minutes)


## Usage
  This script is to fetch the ec2 instances list of specified regions periodictly,
  and post that list to somewhere. 
  
