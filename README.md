# Average Color Classifier

Simple python3 3-module Average Color Classifier with comunication via NATS. This project was made as Homework for Konica Minolta

## Architecture

Classifier is made from 3 modules or microservices which communicate with help of [Nats](https://nats.io/). This microservices are runnig in Docker

First module only load up images from folder (this folder is specified with `IMAGES_FOLDER` const in `image_reader.py`). Put all images into processing folder and then send message into NATS about this event. It scan folder every 10 second and on start.

Second module get message from NATS that image is need to be processed. Module load up image and compute images avg color witch help of opencv (load image) and numpy (compute average color). Then send message to NATS with average color.

Third module get this average color and based on that will find WebColor name. If color is not found, module will find closest name with help of euclidean RGB distance. Then put image from processing folder into folder with WebColor name.

Every module have few python unittest. If you want try it you need go to module folder and run `python3 test.py`

## Instructions for running

Firstly you need to build docker images. Run `docker-compose build`.

Then you can run `docker-compose up --force-recreate` to run it.

In repositary are few base images. If you add more images into `IMAGES_FOLDER` (if you did nor change it, it is "images") then Classifier will pick it up. It run scan every 10 second.