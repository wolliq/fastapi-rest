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

and POST a data vector of 8 elements.

Enjoy!