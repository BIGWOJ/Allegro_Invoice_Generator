import file_operations
import invoice_creation
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QInputDialog, QMessageBox, QFileDialog, QLabel, QApplication
from PyQt5.QtGui import QPixmap
import sys

class GUI_buttons(QWidget):

    def __init__(self):
        super().__init__()
        self.buttons()

    def buttons(self):

        self.import_csv_button = QPushButton("Import .csv file", self)
        self.import_csv_button.clicked.connect(self.import_csv)

        self.exit_app_button = QPushButton("Exit application", self)
        self.exit_app_button.clicked.connect(self.exit_app)

        self.image = QLabel(self)
        self.load_image()

        layout = QVBoxLayout(self)
        layout.addWidget(self.image)
        layout.addWidget(self.import_csv_button)
        layout.addWidget(self.exit_app_button)

        self.setLayout(layout)
        self.resize(500, 500)
        self.setWindowTitle("AIG v1.0")

    #Importing .csv file and extracting orders from it
    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Load .csv file", "", "Text Files (*.csv);;All Files (*)")
        if not file_path:
            return

        QMessageBox.information(None, " ", "File .csv loaded successfully")
        orders = file_operations.read_csv(file_path)
        invoice_creation.generate_invoices(orders)

    #Loading logo image
    def load_image(self):
        pixmap = QPixmap("logo.png")
        self.image.setPixmap(pixmap)
        self.image.setScaledContents(True)

    def exit_app(self):
        exit(0)

standard_font_size = 16
#Filling prices for orders with various sets bought
def price_incomplete_order(product, customer, date):
    window = QWidget()
    window_layout = QVBoxLayout(window)
    window.setStyleSheet(f'font: {standard_font_size}px')

    price, _ = QInputDialog.getDouble(window, " ",f"\nEnter the price of:\n{product}\nbought by {customer}\non day {date} ",decimals=2)
    return price

def invoices_finished():
    QMessageBox.information(QWidget(), " ", "All invoices have been generated")

def app_exec():
    app = QApplication(sys.argv)
    #Manually checked the RGB color of logo background
    logo_background_color = (37,37,37)

    #QPushButton like "OK" "Cancel"
    #GUI_buttons QPushButton - import file and exit app
    app.setStyleSheet(f"""
        QWidget {{
            color: lightgray;
            background-color: rgb({logo_background_color[0]}, {logo_background_color[1]}, {logo_background_color[2]})
        }}
    
        QMessageBox {{
            font: {standard_font_size}px;
            color: lightgray;
            background-color: rgb({logo_background_color[0]}, {logo_background_color[1]}, {logo_background_color[2]})
        }}
        
        QPushButton {{
            font: {standard_font_size}px;
            color: black;
            background-color: lightgray
        }}
        
        GUI_buttons QPushButton {{
            font: bold 22px;
            color: rgb({logo_background_color[0]}, {logo_background_color[1]}, {logo_background_color[2]});
            border-width: 2px;
            border-style: solid;
            border-color: black;
            background-color: lightgray
        }}
        """)

    main_window = GUI_buttons()
    main_window.show()
    app.exec_()
