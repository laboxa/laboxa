#!/bin/bash
docker build -t face-recognition . && docker run -it --privileged --device=/dev/video0 -v ./:/face-recognition face-recognition