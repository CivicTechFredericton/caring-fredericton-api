#!/bin/bash
cd $(dirname $0)

if [ -z $AWS_REGION ] ; then
  echo 'Please set the environment variable AWS_REGION before running this script'
  exit 1
fi

region=$AWS_REGION
env=$1

echo
echo "----------------------------"
echo "Removing Base Infrastructure"
echo "----------------------------"
echo
npm run remove -- --region $region --stage $env

echo
echo "-----------------------"
echo "Removing Dynamo Tables"
echo "-----------------------"
echo
pushd dynamo_tables
npm run remove -- --region $region --stage $env
popd

echo
echo "-----------------------"
echo "Removing API Gateway"
echo "-----------------------"
echo
pushd api_gateway
npm run remove -- --region $region --stage $env
popd
