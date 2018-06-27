## Create Services for Environment ##

The following outlines the steps used to create the required services for a new environment.

### Prerequisites ###

* Ensure the [AWS Command Line Interface](https://aws.amazon.com/cli/) is installed

### Steps ###

* Create a copy of the **templates** folder; rename it the name of the environment (for example: test)
* Edit the files contained within the folder to replace the _{env}_ value
* From the command line enter the commands (in order):
```
./s3.py -p {profile} -e {env}
./cloudfront.py -p {profile} -e {env}
./route53.py -p {profile} -e {env}
./dynamo_tables.py -p {profile} -e {env}
```
