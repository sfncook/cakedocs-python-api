## Run Flask locally for testing:
```shell
python app.py 
```

## To deploy cloud functions:
```shell
cd cloudFunctions
gcloud functions deploy llm --runtime python38 --trigger-http --allow-unauthenticated
```

## To load environment variables from yaml file: (doesn't work with .env)
```shell
cd cloudFunctions
gcloud functions deploy llm --runtime python38 --trigger-http --allow-unauthenticated --env-vars-file ./.env.yaml
```

