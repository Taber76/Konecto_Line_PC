from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout
from matplotlib import style

from gui.components.header import HeaderWidget
from gui.components.footer import FooterWidget
from gui.views.login import Login_View
from gui.views.home import Home_View
from gui.views.session import Session_View
from db.batches.dao import get_all_batches

from config.config import load_config, load_styles
from db.conection import DbConnection
config = load_config()
style = load_styles()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('KONECTO')
        self.resize(config['screen']['width'], config['screen']['height'])
        self.setStyleSheet(
            f"background-color: {style['background_color']};"
        )

        # info
        self.product = ""
        self.batch = ""
        self.batch_id = None
        self.bacth_list = get_all_batches()
        self.user = {"id": None, "fullname": None, "role": None}
        self.cloud_db = "red"
        self.local_db = "red"

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
        self.footer = FooterWidget(self)
        layout.addWidget(self.footer)

        # Views dictionary
        self.views = {}

        # Load and show login view at start
        self.login = Login_View(self)
        self.stacked_widget.addWidget(self.login)
        self.views['login'] = self.login
        self.change_view('login')

        # Check database connection
        self.check_db_connection()

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
        if view_name == 'home':
            self.bacth_list = get_all_batches()
        self.stacked_widget.setCurrentWidget(self.views[view_name])

        # Update the header
        if self.header:
            self.header.update_info()

    def logout(self):
        self.user = {'id': None, 'fullname': None, 'role': None}
        self.change_view('login')

    def check_db_connection(self):
        DbConnection("cloud").connect()
        DbConnection("local").connect()
        if DbConnection("cloud").is_connected():
            self.cloud_db = 'green'
            self.footer.update_cloud_light("green")
        if DbConnection("local").is_connected():
            self.local_db = 'green'
            self.footer.update_local_light("green")
