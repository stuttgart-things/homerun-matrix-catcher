import asyncio
from unittest.mock import MagicMock
from display_on_matrix.image_gif.image import display_image

# WIP
def run_mock_test():
    class MockMatrix:
        def __init__(self):
            self.width = 64
            self.height = 32

        def CreateFrameCanvas(self):
            return MagicMock()

        def SetImage(self, image, x, y):
            pass

        def Clear(self):
            pass

    class MockSelf:
        def __init__(self):
            self.matrix = MockMatrix()
            self.flag_infinity = False

    mock_self = MockSelf()
    args = {
        "image": "http://example.com/image.png",
        "duration": 5,
        "size": "full"
    }

    asyncio.run(display_image(mock_self, args))