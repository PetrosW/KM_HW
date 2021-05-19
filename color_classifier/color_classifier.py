#!/usr/bin/env python3
"""
[summary]
"""
import asyncio
import logging
import os
import json
import shutil

from nats.aio.client import Client as NATS
import webcolors

IMAGES_FOLDER = "images"


async def add_closest_colour(requested_colour: list):
    """
    Based on euclidean distance find nearest specified WebColor and add it.

    :param requested_colour: list [R, G, B] color
    """
    logging.info("Searching for closest colour to %s", requested_colour)
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    closed = min(min_colours.keys())
    # Saving it for later use
    webcolors.CSS3_HEX_TO_NAMES[webcolors.rgb_to_hex(requested_colour)] = min_colours[closed]
    logging.info("Find and save closest colour for %s named %s", requested_colour, min_colours[closed])


async def classifier(image_data: dict):
    """
    Classify image based od mewn RGB color.

    :param image_data: dict with name and RGC color of image
    """
    try:  #try looked at base WebColors
        color_name = webcolors.rgb_to_name(image_data['color'])
    except ValueError:  # if WebColors cannot be find add closest
        logging.info("Did not find color name for %s", image_data['color'])
        await add_closest_colour(image_data['color'])
        color_name = webcolors.rgb_to_name(image_data['color'])

    logging.info("Webcolor name for %s is: %s", image_data['color'], color_name)

    if not os.path.exists(f"{IMAGES_FOLDER}/{color_name}"):
        os.makedirs(f"{IMAGES_FOLDER}/{color_name}")
    shutil.move(f"{IMAGES_FOLDER}/processing/{image_data['image']}", f"{IMAGES_FOLDER}/{color_name}")


async def message_handler(msg):
    """
    Message handle. Basically call main classifier funcsiotn

    :param msg: NATS message
    """
    subject = msg.subject
    reply = msg.reply
    data = json.loads(msg.data.decode())
    logging.info("Received a message on '%s %s': %s", subject, reply, data)
    if 'color' in data and 'image' in data:
        await classifier(data)
    else:
        logging.warning("Received data in bad format: %s", data)


async def run(loop: asyncio.AbstractEventLoop):
    """
    Main run for setting up NATS

    :param loop:  asyncio loop
    """
    nc = NATS()

    logging.info("Connecting to nats")
    await nc.connect(servers=["nats://nats-server:4222"], loop=loop)

    logging.info("Subscribe to nats 'avg_color'")
    await nc.subscribe("avg_color", cb=message_handler, is_async=True)

if __name__ == "__main__":
    logging.basicConfig(format="'%(asctime)s:%(levelname)s: %(message)s'", level=logging.INFO)
    logging.info("Starting color classifier")
    loop = asyncio.get_event_loop()
    loop.create_task(run(loop))
    loop.run_forever()
    loop.close()
