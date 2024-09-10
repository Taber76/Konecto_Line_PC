from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout

from .components.header import HeaderWidget
from .components.footer import FooterWidget
from .views.login import Login_View
from .views.home import Home_View
from .views.session import Session_View

from config.config import load_config
config = load_config()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('KONECTO')
        self.resize(config['screen']['width'], config['screen']['height'])
        self.setStyleSheet(
            f"background-color: {config['style']['background_color']};"
        )

        # showed info
        self.product = ""
        self.batch = ""
        self.user = {"id": None, "fullname": None, "role": None}

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Header
        self.header = HeaderWidget(self)
        layout.addWidget(self.header)
        # Body
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        # Footer
        self.footer = FooterWidget()
        layout.addWidget(self.footer)

        # Views dictionary
        self.views = {}

        # Load and show login view at start
        self.login = Login_View(self)
        self.stacked_widget.addWidget(self.login)
        self.views['login'] = self.login
        self.change_view('login')

    def change_view(self, view_name):
        if view_name not in self.views:
            if view_name == 'home':
                view = Home_View(self)
            elif view_name == 'session':
                view = Session_View(self)
            else:
                raise ValueError(f'Vista {view_name} no existe.')

            # Add view to the stacked widget and store it in the views dictionary
            self.stacked_widget.addWidget(view)
            self.views[view_name] = view

        # Change the current widget in the stacked widget
        self.stacked_widget.setCurrentWidget(self.views[view_name])

        # Update the header
        if self.header:
            self.header.update_info()

    def logout(self):
        self.user = {'id': None, 'fullname': None, 'role': None}
        self.change_view('login')
