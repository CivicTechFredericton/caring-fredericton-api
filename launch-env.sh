#!/bin/bash
set -e

region=$1
env=$2

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
npm run deploy -- --stage $env
popd

echo
echo "-----------------------"
echo "Deploying Dynamo Tables"
echo "-----------------------"
echo
pushd dynamo_tables
ln -sf ../node_modules
npm run deploy -- --stage $env
popd

echo
echo "-------------------------"
echo "Deploying API Application"
echo "-------------------------"
echo
npm run deploy -- --stage $env
