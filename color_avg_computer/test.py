import unittest
import aiounittest
import json
import shutil


TARGET = __import__("color_avg_computer")


class Testbase(aiounittest.AsyncTestCase):
    TARGET.IMAGES_FOLDER = "test_image"
    
    async def test_compute_avg_color(self):
        avg_color = await TARGET.compute_avg_color("mismas.bmp")
        self.assertEqual(avg_color, [190, 171, 144])
        
        
if __name__ == "__main__":
    unittest.main()
    