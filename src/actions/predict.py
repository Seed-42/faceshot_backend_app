
class FaceDetector:
    def __init__(self, image_path):
        self._image_path = image_path
        self._image = self._read_image()

    @staticmethod
    def _read_image():
        return ""

    def _process_image(self):
        pass

    def detect(self):
        return [
            {
              "id": "1a2a34s5d23f4d",
              "confidence": 99.0,
              "coordinates": [12.3, 24.0, 36.5, 48.2],
            }
        ]
