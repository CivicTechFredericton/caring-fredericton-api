# Civic Tech - Caring Calendar API #

This project contains the back end APIs used by the Caring Calendar application.  The endpoints are
agnostic to the client interface being used (React, Angular, iOS, Android).

## SSM Parameter Store Configuration (Prior to deployment) ##
The SSM Parameter Store service will be leveraged to store environment and account specific configuration details.
These values are set manually via aws console and get set as lambda environment variables at deploy time.  
If you want to change defaults then set the value in ssm and redeploy.

| Key | Description | Default |
| :--- | :--- | :--- |
| default-domain-name | REQUIRED! The default domain name for use in the deployed environments | None |
| default-email-sender | REQUIRED! The default email address where emails come from | None |
| default-org-verification-email-recipient | REQUIRED! The default email address used to verify new organization requests | None |
| caring-fred-{{stage}}-api-domain-name | OPTIONAL Custom API domain name used for the environment | None |
| caring-fred-{{stage}}-ui_domain_name | OPTIONAL Custom web site URL | None |
| caring-fred-{{stage}}-email-sender | OPTIONAL Overridden value for who should emails come from | None |
| caring-fred-{{stage}}-org-verification-email-recipient | OPTIONAL Overridden value for the email address used to verfiy new organization requests | None |
## Functionality: ##

* Organization Management (Registration, Verification, Updates)
* Scheduling Events

## Project Setup ##

NPM is used to install the serverless tools whereas pip is used to install runtime Python packages.

### NPM Dependencies ###

Ensure the prerequisites are installed
```
- Node LTS 12.x (for working with serverless)
    - nvm (Node Version Manager) is highly recommended 
```

Install the NPM dependencies
```
npm install
```

### Python Dependencies ###

Ensure the prerequisites are installed
```
- Python3.8
- pip (tool for installing Python packages)
```

Create virtual env for python3.8 inside project directory:
```
python3.8 -m venv venv 
```

Activate newly created environment
```
. venv/bin/activate
```

Install the required python packages
```
pip install -r requirements.txt
```

OPTIONAL: Exit the virtual environment using the following command
```
deactivate
```

## Project Deployment ##

The application can be deployed by issuing the following commands:
```
export AWS_PROFILE=test
export AWS_REGION=ca-central-1
./deploy-env.sh <stage_name>
```

Once the application has been deplolyed create a user account to be used for working with the APIs
```
cd scripts
./user_sign_up.py <username> <password> -p <profile name> - s <stage_name>
```

** NOTES: **

* Replace **test** with your assume role profile name
* Please include your name to stage name if you want to create a custom AWS stack for testing purposes
* This command must be run inside an activated virtual environment

## Running project locally ##

The project can be run locally using the following command:
```
export AWS_PROFILE=tech
export AWS_REGION=ca-central-1
./run-local.sh <stage_name>
```

**NOTES**:

* This command must be run inside an activated virtual environment
* Any environment (stage name) can be used provided there is an existing deployment available
* When running locally timeout, access, and file size restrictions do not behave the same as within an AWS service
* This command must be run inside an activated virtual environment

## Remove Application ##

The application can be removed by issuing the following commands:
```
export AWS_PROFILE=test
export AWS_REGION=ca-central-1
./remove-env.sh <stage_name>
```

** NOTES: **

* Replace **test** with your assume role profile name
* Any environment (stage name) can be used provided there is an existing deployment available
* This command must be run inside an activated virtual environment
