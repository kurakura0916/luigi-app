#!/usr/bin/env bash

env=$1

pushd `dirname $0`/.. > /dev/null


pushd lambda > /dev/null
zip build/param_creator.zip param_creator.py

popd

aws cloudformation package --template-file cloudformation/sam.yml \
    --s3-bucket hoge-package \
    --s3-prefix luigi-app \
    --output-template-file cloudformation/rendered-sam.yml \
    --profile your_profile

aws cloudformation deploy --template-file `pwd`/cloudformation/rendered-sam.yml \
    --stack-name luigi-app-${env} \
    --parameter-overrides "env=${env}" \
    --capabilities CAPABILITY_IAM \
    --profile your_profile

aws cloudformation deploy --template-file `pwd`/cloudformation/batch_infra.yml \
    --stack-name luigi-app-${env}-infra \
    --parameter-overrides "env=${env}" \
    --capabilities CAPABILITY_IAM \
    --profile your_profile

rm cloudformation/rendered-sam.yml
