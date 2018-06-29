# Civic Tech - Caring Calendar API #

This project contains the back end APIs used by the Caring Calendar application.  The endpoints are
agnostic to the client interface being used (React, Angular, iOS, Android).

## Functionality: ##

* Feature 1
* Feature 2


## Project Setup ##

NPM is used to install the serverless tools whereas pip is used to install runtime Python packages.

### NPM Dependencies ###

Ensure the prerequisites are installed
```
- OPTIONAL: Node Virtual Manager (nvm)
- Node 8.11.x (for working with serverless)
```

Install the NPM dependencies
```
npm install
```

### Python Dependencies ###

Ensure the prerequisites are installed
```
- Python3.6
- pip (tool for installing Python packages)
- virtualenv (python3.6-virtualenv)
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

## Serverless Deployment ##

The application can be deployed by issuing the following commands:
```
export AWS_PROFILE=test
npm run deploy -- --stage <stage name>
```

** NOTES: **

* Replace **test** with your assume role profile name
* Please include your name to stage name if you want to create custom AWS stack for testing purposes.  For example:
> ```
> npm run deploy -- --stage hpowell
> ```

## Running project locally ##

The project can be run locally using the following command:
> ```
> npm run local -- --stage <stage name>
> ```

**NOTES**:

* This command must be run inside an activated virtual environment
* Any environment (stage name) can be used, optionally you may want to use `config/local.yaml` configuration file
* When running locally timeout, access, and file size restrictions do not behave the same as within an AWS service
