#!/bin/bash

docker build . -t python:ase
docker run -itd --name python -w /workdir -v .:/workdir -p 50021:50021 python:ase