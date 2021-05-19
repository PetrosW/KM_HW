import unittest
import aiounittest
import json
import shutil


TARGET = __import__("image_reader")


class NATS:
    def __init__(self):
        self.local_data = {}
        
    async def publish(self, key, data):
        self.local_data[key] = json.loads(data)


class Testbase(aiounittest.AsyncTestCase):
    TARGET.IMAGES_FOLDER = "test_image"
    
    async def test_image_load(self):
        nc = NATS()
        
        await TARGET.scan_folder(nc)
        
        self.assertEqual(nc.local_data['test_image']['image'], "brown.bmp")
        
    async def test_image_load_unsupported_format(self):
        nc = NATS()
        
        await TARGET.scan_folder(nc)
        with self.assertRaises(KeyError):
            nc.local_data['test_image']['image']
        
    @classmethod
    def tearDownClass(self):
        shutil.move(f"{TARGET.IMAGES_FOLDER}/processing/brown.bmp", TARGET.IMAGES_FOLDER)
        
if __name__ == "__main__":
    unittest.main()
    