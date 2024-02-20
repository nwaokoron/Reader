# Reader
Reader Chrome Extension Is an accessibility app to read online content.

To run locally
```
flask --app main run
```


To run in docker

After updating app src code, build docker image for the cantainer use the following command. 

```
docker build -t reader .
```


To run the container use the following command
```
docker run -dp 127.0.0.1:8080:8080 reader
```

Run reader in a google cloud authenicate docker container via GOOGLE_APPLICATION_CREDENTIALS
"""
docker run -dp 127.0.0.1:8080:8080 -w /app --mount type=bind,src="$(pwd)"/secrets,target=/app/secrets/ reader

Check that container has been started by 

```
docker ps
```

If container is not running check for errors
```
docker logs <container_id>
```

To open the container's command line run:
```
docker exec -it <container> bash
```

`testing`


depeloyed on google cloud run
https://console.cloud.google.com/run?hl=en&project=reader-400005

how to deploy
https://cloud.google.com/run/docs/deploying-source-code