import asyncio
from unittest.mock import MagicMock
from display_on_matrix.image_gif.gif import display_gif

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

        def SwapOnVSync(self, canvas):
            pass

        def Clear(self):
            pass

    class MockSelf:
        def __init__(self):
            self.matrix = MockMatrix()
            self.flag_infinity = False

    mock_self = MockSelf()
    args = {
        "image": "http://example.com/image.gif",
        "duration": 5,
        "speed": "2",
        "size": "full"
    }

    asyncio.run(display_gif(mock_self, args))