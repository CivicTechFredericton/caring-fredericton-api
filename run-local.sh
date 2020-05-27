#!/bin/bash
set -e
cd $(dirname $0)

if [ -z "$1" ]
  then
    echo "Please supply an environment stage name"
    exit 1
fi

if [ -z $AWS_REGION ] ; then
  export AWS_REGION='ca-central-1'
fi

region=$AWS_REGION
env=$1

npm run local -- --region $region --stage $env
