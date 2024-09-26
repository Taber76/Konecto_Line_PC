from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

from config.config import load_config, load_styles
config = load_config()
style = load_styles()

class FooterWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):

        # CLOUD CONECTION LIGHT ------------------------------------------------
        

        # MAIN LAYOUT ------------------------------------------------------------
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setAlignment(Qt.AlignCenter)

        # Main layout
        main_vertical_layout = QVBoxLayout()
        main_vertical_layout.setAlignment(Qt.AlignCenter)
        main_vertical_layout.addLayout(horizontal_layout)
        self.setLayout(main_vertical_layout)
        self.setStyleSheet(
            f"background-color: {style['header']['background_color']};"
            f"font-family: {style['header']['font']};"
            f"font-weight: {style['header']['font-weight']};"
            f"color: {style['header']['text_color']};"
        )
        self.setFixedWidth(config['screen']['width'])
        self.setFixedHeight(int(config['screen']['height'] * 0.08))
   
