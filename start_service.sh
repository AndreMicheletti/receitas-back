#!/usr/bin/env bash

docker kill receitas_back
docker rm receitas_back
docker build -t receitas_back .
docker run -d -p 7465:7465 --name receitas_back receitas_back