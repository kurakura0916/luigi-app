## 環境構築

ECRへイメージをPUSH
```bash
aws ecr get-login --no-include-email --region ap-northeast-1 --profile your_profile
docker build -t luigi-app-image .
docker tag luigi-app-image:latest 1234.dkr.ecr.ap-northeast-1.amazonaws.com/luigi-app-image:latest
docker push 1234.dkr.ecr.ap-northeast-1.amazonaws.com/luigi-app-image:latest
```

CloudFormationによるAWS LambdaとBatchの環境構築

staging環境を想定するならば`stg`、production環境を想定するならば`prod`を引数に指定する。
```bash
./script/deploy.sh (stg or prod)
```


## 実行

```bash

env="stg" # 本番環境ならprod
date="YYYY-MM-DD"

aws lambda invoke \
    --function-name luigi-app-param-creator-${env} \
    --payload "{\"DATE\": \"${date}\"}"  /dev/null  \
    --profile your_profile
```
