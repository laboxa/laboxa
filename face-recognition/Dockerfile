FROM python:3.10

WORKDIR /face-recognition

COPY ./requirements.txt /face-recognition/

RUN apt-get -y update \
    && apt-get -y install libopencv-dev
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

# # EXPOSE 5000

CMD ["bash"]
# CMD ["python3", "test.py"]