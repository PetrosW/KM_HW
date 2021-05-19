#!/usr/bin/env python3
"""
[summary]
"""
import asyncio
import json
import logging
import os
import shutil
import time

from nats.aio.client import Client as NATS

# just support most common files
SUPPORTED_IMAGE_FILES = {".bmp", ".jpg", ".png"}

IMAGES_FOLDER = "images"


async def scan_folder(nc: NATS):
    """
    Scan folder for supported images and publish them

    :param nc: NATS client
    """
    logging.info("Scanning for images")
    with os.scandir(f"{IMAGES_FOLDER}") as entries:
        for entry in entries:
            if entry.is_file():
                _, file_ext = os.path.splitext(entry.name)
                if file_ext in SUPPORTED_IMAGE_FILES:
                    shutil.move(f"{IMAGES_FOLDER}/{entry.name}", f"{IMAGES_FOLDER}/processing")
                    logging.info("Publishing image to system %s", entry.name)
                    await nc.publish(IMAGES_FOLDER, json.dumps({"image": entry.name}).encode())


async def run(loop: asyncio.AbstractEventLoop):
    """
    Main funcion, check folder every 10 second and sending supported picture format to system.

    :param loop: asyncio loop
    """
    nc = NATS()

    logging.info("Connecting to nats")
    await nc.connect(servers=["nats://nats-server:4222"], loop=loop)

    logging.info("Starting loop")
    while True:
        try:
            await scan_folder(nc)
            # re-scan folder every 10 seconds
            await asyncio.sleep(10)
        except Exception as ex:  # we dont want shut down whole program
            logging.error(ex)
            pass

if __name__ == "__main__":
    logging.basicConfig(format="'%(asctime)s:%(levelname)s: %(message)s'", level=logging.INFO)
    logging.info("Starting image reader")

    if not os.path.exists(IMAGES_FOLDER):
        os.makedirs(IMAGES_FOLDER)
    if not os.path.exists(f"{IMAGES_FOLDER}/processing"):
        os.makedirs(f"{IMAGES_FOLDER}/processing")
    time.sleep(2)  # wait for others to start
    loop = asyncio.get_event_loop()
    loop.create_task(run(loop))
    loop.run_forever()
    loop.close()
