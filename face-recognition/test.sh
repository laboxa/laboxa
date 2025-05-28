#!/bin/bash
docker build -t face-recognition . && docker run --rm -it -v ./:/face-recognition face-recognition