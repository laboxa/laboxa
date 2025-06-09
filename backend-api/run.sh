#!/bin/bash
docker build -t backend-api ./app && docker run -p 8000:8000 -it -v ./app:/app backend-api