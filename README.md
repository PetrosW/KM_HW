# Average Color Classifier

Simple python3 3-module Average Color Classifier with communication via NATS. This project was made as an interview assignment for Konica Minolta.

## Architecture

Classifier consists of 3 modules or microservices which communicate with the help of [Nats](https://nats.io/). This microservices are runnig in Docker.

First module only loads up images from folder (this folder is specified by `IMAGES_FOLDER` constant in `image_reader.py`). Put all images into processing folder and then send message into NATS about this event. It scan folder every 10 second and on start.

Second module gets message from NATS that there is image to be processed. This module loads image and the average color of the image with the help of opencv (load image) and numpy (compute average color). Then it sends message to NATS with average color.

TThird module uses the average color to find its WebColor name. If color is not found, module will find closest name with help of euclidean RGB distance. The processed image is transferred from the processing folder to folder specified by the WebColor name.

Every module has several python unittestwhich can be run in the module folder typing `python3 test.py`

## Instructions for running

First, you need to build docker images. To do so, run `docker-compose build`.

Then you can run `docker-compose up --force-recreate` to run it.

Repository has few sample images. If you add more images into `IMAGES_FOLDER` (specified by the default folder name "images") the classifier automatically process them. It runs scan every 10 second.
