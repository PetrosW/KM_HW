import unittest
import aiounittest
import json
import webcolors
import os
import shutil


TARGET = __import__("color_classifier")


class Message:
    def __init__(self, subject, reply, data):
        self.subject = subject
        self.reply = reply
        self.data = json.dumps(data).encode()

class Testbase(aiounittest.AsyncTestCase):
    TARGET.IMAGES_FOLDER = "test_image"
    
    async def test_add_closest_colour(self):
        rgb_color = (254,0,0)
        
        await TARGET.add_closest_colour(rgb_color)
        
        self.assertEqual(webcolors.CSS3_HEX_TO_NAMES["#fe0000"], "red")
        
    async def test_classifier(self):
        image_data = {
            'color': (254,0,0),
            'image': "red.bmp",
        }
        
        await TARGET.classifier(image_data)
        
        self.assertTrue(os.path.exists(f"{TARGET.IMAGES_FOLDER}/red/red.bmp"))
        
        shutil.move(f"{TARGET.IMAGES_FOLDER}/red/red.bmp", f"{TARGET.IMAGES_FOLDER}/processing")
        
    async def test_message_handler(self):
        data = Message(
            "test", 
            "test_reply", 
            {
                'color': (254,0,0),
                'image': "red.bmp",
            }
        )
        await TARGET.message_handler(data)
        
        self.assertTrue(os.path.exists(f"{TARGET.IMAGES_FOLDER}/red/red.bmp"))
        
        shutil.move(f"{TARGET.IMAGES_FOLDER}/red/red.bmp", f"{TARGET.IMAGES_FOLDER}/processing")
        
        
if __name__ == "__main__":
    unittest.main()
    