## To deploy cloud functions:
```shell
cd cloudFunctions
gcloud functions deploy llm --runtime python38 --trigger-http --allow-unauthenticated --env-vars-file ../.env.yaml
```