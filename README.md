# Fast API scorer

Simple Fast API example to load a PyTorch model and score an input tensor (vector of 8 values).

# How to run
- Install just lib
- launch
```
just build
```
to build the image locally

- launch
```
just run
```
to run the docker image locally.

Then hit
```
http://0.0.0.0:8000/docs
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

- You can also retrain the model using different parameters in the trainer.py file.

Enjoy!