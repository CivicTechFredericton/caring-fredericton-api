#!/bin/bash
set -e
cd $(dirname $0)

if [ -z $AWS_REGION ] ; then
  echo 'Please set the environment variable AWS_REGION before running this script'
  exit 1
fi

if [ -z "$1" ]
  then
    echo 'Please supply an environment stage name'
    exit 1
fi

region=$AWS_REGION
env=$1

echo "------------------------------"
echo "Installing NPM Dependencies"
echo "------------------------------"
echo
npm install

echo "------------------------------"
echo "Installing Python Dependencies"
echo "------------------------------"
echo
pip install -r requirements.txt

echo
echo "---------------------"
echo "Deploying API Gateway"
echo "---------------------"
echo
pushd api_gateway
ln -sf ../node_modules
npm run deploy -- --region $region --stage $env
popd

echo
echo "-----------------------------"
echo "Deploying Base Infrastructure"
echo "-----------------------------"
echo
npm run deploy -- --region $region --stage $env

echo
echo "--------------------------"
echo "Deploying Helper Functions"
echo "--------------------------"
echo
pushd functions
ln -sf ../node_modules
npm run deploy -- --region $region --stage $env
popd

echo
echo "--------------------------"
echo "Deploying Cognito Triggers"
echo "--------------------------"
echo
pushd cognito_triggers
ln -sf ../node_modules
npm run deploy -- --region $region --stage $env
popd

echo
echo "-----------------------"
echo "Deploying Dynamo Tables"
echo "-----------------------"
echo
pushd dynamo_tables
ln -sf ../node_modules
npm run deploy -- --region $region --stage $env
popd
