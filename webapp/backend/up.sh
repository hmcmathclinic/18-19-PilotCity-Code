#!/bin/bash

sh build.sh

kubectl create -f "matchmaking.yaml"
kubectl create -f "matchmaking-service.yaml"