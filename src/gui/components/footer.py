from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QHBoxLayout
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
        self.cloud_light = QWidget()
        self.cloud_light.setFixedSize(30, 30)
        self.cloud_light.setStyleSheet(f"background-color: {self.main_window.cloud_db}; border-radius: 15px;")
        cloud_label = QLabel("Online Db")
        cloud_layout = QHBoxLayout()
        cloud_layout.setAlignment(Qt.AlignCenter)
        cloud_layout.addWidget(self.cloud_light)
        cloud_layout.addWidget(cloud_label)

        # LOCAL CONECTION LIGHT ------------------------------------------------
        self.local_light = QWidget()
        self.local_light.setFixedSize(30, 30)
        self.local_light.setStyleSheet(f"background-color: {self.main_window.local_db}; border-radius: 15px;")
        local_label = QLabel("Local Db")
        local_layout = QHBoxLayout()
        local_layout.setAlignment(Qt.AlignCenter)
        local_layout.addWidget(self.local_light)
        local_layout.addWidget(local_label)

        # SECONDARY LAYOUT ------------------------------------------------------------
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setAlignment(Qt.AlignRight)
        horizontal_layout.addLayout(cloud_layout)
        horizontal_layout.addSpacerItem(QSpacerItem(30, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))  
        horizontal_layout.addLayout(local_layout)

        # MAIN LAYOUT ------------------------------------------------------------
        main_vertical_layout = QVBoxLayout()
        main_vertical_layout.setAlignment(Qt.AlignRight)
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
   
    def update_cloud_light(self, value):
        self.cloud_light.setStyleSheet(f"background-color: {value}; border-radius: 15px;")
        self.cloud_light.update()

    def update_local_light(self, value):
        self.local_light.setStyleSheet(f"background-color: {value}; border-radius: 15px;")
        self.local_light.update()