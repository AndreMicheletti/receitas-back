#!/usr/bin/env bash

./stop_service.sh
docker build -t receitas_back .
docker run -d -p 7465:7465 --name receitas_back receitas_back