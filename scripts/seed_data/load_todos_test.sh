#!/bin/bash
# call this function to write to stderr
echo_stderr ()
{
    echo "$@" >&2
}
if [ -z ${AWS_PROFILE} ]
then
   if [ ${#} -ge 1 ]
   then
      export AWS_PROFILE=${1}
   else
      echo_stderr "ERROR: AWS_PROFILE not set and no value passed in"
      echo_stderr ""
      echo_stderr "NOTE: You should set your default AWS profile before running this script"
      echo_stderr "      e.g.) export AWS_PROFILE=your-profile-name"
      echo_stderr ""
      echo_stderr "      Alternatively, just pass the profile name in as the first / only parameter."
      echo_stderr "      e.g.) ${0} your-profile-name"
      echo_stderr ""
      exit 1
   fi
fi

# Todo Table Items
aws dynamodb put-item --table-name caring-fred-test-todos --item '{"id":{"S":"todo01"},"title":{"S":"Complete Timesheet"}}'
aws dynamodb put-item --table-name caring-fred-test-todos --item '{"id":{"S":"todo02"},"title":{"S":"Civic Tech"},"description":{"S":"Prep for Serverless Session"}, "is_complete":{"BOOL":true}}'

