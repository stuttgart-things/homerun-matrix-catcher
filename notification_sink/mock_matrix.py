import datetime

class MockRGBMatrix:
    def __init__(self, options=None):
        self.options = options
        self.display_log = []

    def log_display(self, content):
        timestamp = datetime.datetime.now().isoformat()
        self.display_log.append((timestamp, content))
        print(f"[{timestamp}] Display: {content}")

    def clear(self):
        self.log_display("Clearing matrix")

    def draw_text(self, text, color):
        self.log_display(f"Drawing text '{text}' with color {color}")

    def draw_image(self, file_name):
        self.log_display(f"Displaying image '{file_name}'")

    def draw_gif(self, gif_name, duration, speed, display_severity, display_system):
        if display_severity and display_system:
            self.log_display(f"Displaying generated GIF with severity '{display_severity}' and system '{display_system}' for '{duration}' seconds and a speedvalue of '{speed}'")
        else:
            self.log_display(f"Displaying GIF '{gif_name}' for '{duration}' seconds and a speedvalue of '{speed}'")