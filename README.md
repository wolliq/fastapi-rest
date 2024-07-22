# FastAPI - Sentence API

Welcome to the Sentence API for SMG.
It contains a simple REST API

# How to run locally

- Set GCloud account in your .env file
```
# Development settings
PROJECT_ID="YOUR_PROJECT_ID"
DATASET_ID="YOUR_DATASET_ID"
TABLE_ID="YOUR_TABLE_ID"

GOOGLE_APPLICATION_CREDENTIALS="PATH_TO_GCLOUD_JSON_FILE"
```

- Launch
```
$ fastapi dev app/main.py
```
and you should see
```
 ╭────────── FastAPI CLI - Development mode ───────────╮                                                                                                                                 
 │                                                     │                                                                                                                                 
 │  Serving at: http://127.0.0.1:8000                  │                                                                                                                                 
 │                                                     │                                                                                                                                 
 │  API docs: http://127.0.0.1:8000/docs               │                                                                                                                                 
 │                                                     │                                                                                                                                 
 │  Running in development mode, for production use:   │                                                                                                                                 
 │                                                     │                                                                                                                                 
 │  fastapi run                                        │                                                                                                                                 
 │                                                     │                                                                                                                                 
 ╰─────────────────────────────────────────────────────╯ 
```
- Connect to http://127.0.0.1:8000/docs to access the Swagger UI

# How to test locally
Supposing you have filled a BigQuery table, schema as in the test dataset.
You can directly target the endpoint using a curl command:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/sentences/10' \
  -H 'accept: application/json'
```
which will reply something like
```
{
  "id": 10,
  "text": "super movie title",
  "cyphered_text": "fhcre zbivr gvgyr"
}
```

# How to deploy
## Docker
- Install Docker (https://docs.docker.com/engine/install/)
- Install just (https://github.com/casey/just)
- Then, launch
```
$ just build
```
to build the image locally

- Docker launch
```
$ just run
```
to run the docker image locally.

## Kubernetes
- Kubernetes launch (Docker Desktop)
```
$ kubectl apply -f service.yaml
$ kubectl apply -f deployment.yaml
```

Then you can check pods:
```
$ kubectl get pods
```

to see
```
NAME                            READY   STATUS    RESTARTS   AGE
fastapi-rest-7c4787b5fd-wpffj   1/1     Running   0          4s
```

The exec a port forward
```
$ kubectl port-forward fastapi-rest-7c4787b5fd-bdpzb 8080:8000
```

Then hit
```
http://0.0.0.0:8080/docs
```

and play with the Swagger UI.
