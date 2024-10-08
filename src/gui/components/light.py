from PySide6.QtWidgets import QWidget

class Light(QWidget):
    def __init__(self, color="red"):
        super().__init__()
        self.setFixedSize(100, 100)
        self.set_light_color(color)

    def set_light_color(self, color):
        self.setStyleSheet(f"background-color: {color}; border-radius: 50%;")
