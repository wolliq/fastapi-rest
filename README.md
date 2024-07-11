# Fast API scorer

Simple Fast API example to load a PyTorch model and score an input tensor (vector of 8 values).

# How to run
- Install just lib
- launch
```
just build
```
to build the image locally

- Docker launch
```
just run
```
to run the docker image locally.

- Kubernetes launch (Docker Desktop)
```
kubectl apply -f service.yaml
kubectl apply -f deployment.yaml
```

Then you can check pods:
```
kubectl get pods
```

to see
```
NAME                            READY   STATUS    RESTARTS   AGE
fastapi-rest-7c4787b5fd-wpffj   1/1     Running   0          4s
```

The exec a port forward
```
kubectl port-forward fastapi-rest-7c4787b5fd-bdpzb 8080:8000
```

Then hit
```
http://0.0.0.0:8080/docs
```

and POST a data vector of 8 elements as follow
```
{
  "data": [
    0.1,0.2,0.3,0.4,0.1,0.2,0.3,0.4
  ]
}
```

You should see a prediction showing up
```
{
  "predictions": [
    0.09620699286460876
  ]
}
```

You can also directlyy target the endpoint using a curl command:
```
curl -X 'POST' \
  'http://0.0.0.0:8000/score' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": [
    0.1,0.2,0.3,0.4,0.1,0.2,0.3,0.4
  ]
}'
```
which will reply
```
{"predictions":[0.09620698541402817]}
```

# Retraining
You can also retrain the model using different parameters in the trainer.py file.

Enjoy!