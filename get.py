from google.cloud import vision
from google.cloud.vision import types
import os
import io

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'KEY.json'

pics = ['https://i.imgur.com/2EUmDJO.jpg', 'https://i.imgur.com/FPMomNl.png',
        'https://images.everydayhealth.com/images/diet-nutrition/how-many-calories-are-in-a-banana-1440x810.jpg']


class Identify():
    def __init__(self, pics):
        self._pics = pics

    def pics(self):
        return self._pics

    def run(self):
        client = vision.ImageAnnotatorClient()
        image = types.Image()

        for pic in self._pics:
            image.source.image_uri = pic
            resp = client.label_detection(image=image)

            labels = resp.label_annotations

            print("Labels")
            for label in labels:
                print(label.description)

            print('=' * 79)


items = Identify(pics)
items.run()
