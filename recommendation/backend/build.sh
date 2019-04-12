#!/bin/bash

docker build -t gcr.io/silver-osprey-217701/matching .
docker push gcr.io/silver-osprey-217701/matching:latest
