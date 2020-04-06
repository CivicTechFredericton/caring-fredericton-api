echo
echo "-----------------------"
echo "Deploying Dynamo Tables"
echo "-----------------------"
echo
pushd dynamo_tables
ln -sf ../node_modules
npm run deploy -- --region $region --stage $env
popd

echo
echo "-------------------------"
echo "Deploying API Application"
echo "-------------------------"
echo
npm run deploy -- --region $region --stage $env