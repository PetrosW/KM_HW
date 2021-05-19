#!/usr/bin/env python3
"""
[summary]
"""
import asyncio
import logging
import json

import cv2
import numpy as np
from nats.aio.client import Client as NATS


IMAGES_FOLDER = "images"
NC = NATS()


async def compute_avg_color(image_name: str) -> list:
    """
    Compute avg color for a given image. Using OpenCv for loading and Numpy for computing.

    :param image_name: name of image
    :return: list [R, G, B] color
    """
    processing_image = cv2.cvtColor(cv2.imread(f"{IMAGES_FOLDER}/processing/{image_name}"), cv2.COLOR_BGR2RGB)
    avg_color = np.mean(processing_image, axis=(0, 1), dtype=int).tolist()
    return avg_color


async def message_handler(msg):
    """
    Handler for NATS.
    Call compute avg. color and then send it to NATS system.

    :param msg: [description]
    """
    subject = msg.subject
    reply = msg.reply
    data = json.loads(msg.data.decode())
    logging.info("Received a message on '%s %s': %s", subject, reply, data)
    
    if 'image' in data:
        avg_color = await compute_avg_color(data['image'])
        
        logging.info("Publishing message %s", avg_color)
        await NC.publish(
            "avg_color",
            json.dumps(
                {
                    "image": data['image'],
                    "color": avg_color,
                }
            ).encode()
        )
    else:
        logging.warning("Received data in bad format: %s", data)


async def run(loop: asyncio.AbstractEventLoop):
    """
    Main run for setting up NATS

    :param loop:  asyncio loop
    """
    logging.info("Connecting to nats")
    await NC.connect(servers=["nats://nats-server:4222"], loop=loop)

    logging.info("Subscribe to nats 'images")
    await NC.subscribe("images", cb=message_handler, is_async=True)


if __name__ == "__main__":
    logging.basicConfig(format="'%(asctime)s:%(levelname)s: %(message)s'", level=logging.INFO)
    logging.info("Starting color average computer")
    loop = asyncio.get_event_loop()
    loop.create_task(run(loop))
    loop.run_forever()
    loop.close()
