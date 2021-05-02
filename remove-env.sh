#!/bin/bash
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

echo
echo "------------"
echo "Removing App"
echo "------------"
echo
npm run remove -- --region $region --stage $env

echo
echo "-------------------------"
echo "Removing Helper Functions"
echo "-------------------------"
echo
pushd functions
ln -sf ../node_modules
npm run remove -- --region $region --stage $env
popd

echo
echo "-----------------------"
echo "Removing Dynamo Tables"
echo "-----------------------"
echo
pushd dynamo_tables
ln -sf ../node_modules
npm run remove -- --region $region --stage $env
popd

echo
echo "-----------------------"
echo "Removing Cognito Triggers"
echo "-----------------------"
echo
pushd cognito_triggers
ln -sf ../node_modules
npm run remove -- --region $region --stage $env
popd

echo
echo "-------------------"
echo "Removing User Pools"
echo "-------------------"
echo
pushd user_pools
ln -sf ../node_modules
npm run remove -- --region $region --stage $env
popd

echo
echo "-----------------------"
echo "Removing API Gateway"
echo "-----------------------"
echo
pushd api_gateway
ln -sf ../node_modules
npm run remove -- --region $region --stage $env
popd
