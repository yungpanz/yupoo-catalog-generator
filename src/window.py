import sys
import re
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QLabel, QPushButton, QFileDialog, QComboBox, QGraphicsView, QGraphicsScene
)
from PyQt5.QtGui import QPixmap, QDoubleValidator
from PyQt5.QtCore import Qt
from pdf import PDF
from webpage import WebPage
from scraper import Scraper
from image_downloader import ImageDownloader
from currency_converter import CurrencyConverter
        
class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    
        self.setWindowTitle('Yupoo catalog generator')
        
        # Create a label and text box for the Catalog title
        title_label = QLabel('Catalog title:', self)
        title_label.move(20, 20)
        self.title_text_box = QLineEdit(self)
        self.title_text_box.move(20, 50)
        self.title_text_box.resize(200, 32)
        
        # Create a label and text box for the Yupoo catalog URL
        url_label = QLabel('Yupoo catalog URL:', self)
        url_label.move(20, 90)
        self.url_text_box = QLineEdit(self)
        self.url_text_box.move(20, 120)
        self.url_text_box.resize(200, 32)
        
        # Create a label for the price multiplier text box
        price_multiplier_label = QLabel('Price multiplier:', self)
        price_multiplier_label.move(230, 90)

        # Create a text box to accept only numbers
        self.price_multiplier_text_box = QLineEdit(self)
        self.price_multiplier_text_box.move(230, 120)
        self.price_multiplier_text_box.resize(200, 32)
        self.price_multiplier_text_box.setValidator(QDoubleValidator())
        
        # Create a text box to accept only floats
        self.price_multiplier_text_box = QLineEdit(self)
        self.price_multiplier_text_box.move(230, 120)
        self.price_multiplier_text_box.resize(200, 32)

        # Create an float validator
        float_validator = QDoubleValidator()

        # Set the float validator for the text box
        self.price_multiplier_text_box.setValidator(float_validator)
        
        # Create a label and text box to display the selected image file path
        image_label = QLabel('Cover image file:', self)
        image_label.move(20, 200)
        self.image_text_box = QLineEdit(self)
        self.image_text_box.move(20, 230)
        self.image_text_box.resize(200, 32)
        self.image_text_box.setReadOnly(True)  # Make the text box read-only
        
        # Create a button to select an image file
        image_button = QPushButton('Select image', self)
        image_button.move(230, 230)
        
        # Create a graphics view and scene to display the image preview
        self.preview_view = QGraphicsView(self)
        self.preview_view.move(350, 230)
        self.preview_view.resize(200, 200)
        self.preview_scene = QGraphicsScene(self.preview_view)
        self.preview_view.setScene(self.preview_scene)
        
        # Define a function to be called when the image button is clicked
        def on_image_button_clicked():
            # Show a file selection dialog
            file_name, _ = QFileDialog.getOpenFileName(self, 'Select image', '/', 'Images (*.png *.xpm *.jpg *.bmp)')
            if file_name:  # If a file was selected
                self.image_text_box.setText(file_name)  # Set the text of the text box to the file path
                # Load the image file and display it in the preview scene
                pixmap = QPixmap(file_name)
                scaled_pixmap = pixmap.scaled(self.preview_view.size(), Qt.KeepAspectRatio)  # Scale the pixmap to fit the view
                self.preview_scene.clear()  # Clear the scene
                self.preview_scene.addPixmap(scaled_pixmap)  # Add the pixmap to the scene
            else:  # If no file was selected
                self.image_text_box.setText('')  # Clear the text box
                self.preview_scene.clear()  # Clear the scene
           
        # Create the currency combo box
        output_label = QLabel('Select currency:', self)
        output_label.move(20, 270)
        self.currency_combo_box = QComboBox(self)
        self.currency_combo_box.move(20, 300)
        self.currency_combo_box.addItem("¥ - Chinese Yen")
        self.currency_combo_box.addItem("€ - Euro")
        self.currency_combo_box.addItem("$ - US Dollar")
             
        # Create a drop-down list to select the output format
        output_label = QLabel('Output format:', self)
        output_label.move(200, 270)
        self.output_combo_box = QComboBox(self)
        self.output_combo_box.move(200, 300)
        self.output_combo_box.addItem('PDF')  # Add an item to the list
        
        # Create a button to generate the catalog
        generate_button = QPushButton('Generate catalog', self)
        generate_button.move(20, 360)
        
        # Define a function to be called when the generate button is clicked
        def on_generate_button_clicked():
            # Get the values from the input widgets
            self.pdf_title = self.title_text_box.text()
            self.url = self.url_text_box.text()
            self.image_file = self.image_text_box.text()
            self.price_multiplier = float(self.price_multiplier_text_box.text())
            self.output_format = self.output_combo_box.currentText()  # Get the currently selected item
            
            # Get the selected currency
            currency_index = self.currency_combo_box.currentIndex()
            if currency_index == 0:
                # Chinese Yen
                self.currency_symbol = "¥"
                self.currency_code = "CNY"
            elif currency_index == 1:
                # Euro
                self.currency_symbol = "€"
                self.currency_code = "EUR"
            elif currency_index == 2:
                # US Dollar
                self.currency_symbol = "$"
                self.currency_code = "USD"
            else:
                # Unknown currency
                self.currency_symbol = "?"
            
            # Create an instance of the WebPage class
            web_page = WebPage(self.url)

            # Get the content of the page
            page_content = web_page.get_page_content()
            
            # Create an instance of the Scraper class
            scraper = Scraper(page_content)
            
            # Extract the products from the HTML page
            self.products = scraper.extract_products()
            
            if self.output_format == "PDF":
                self.generate_pdf()

        # Connect the buttons' clicked signals to the functions
        image_button.clicked.connect(on_image_button_clicked)
        generate_button.clicked.connect(on_generate_button_clicked)
        
    def generate_pdf(self): 
        # Create an instance of the CurrencyConverter class
        converter = CurrencyConverter()
        
        # Create an instance of the ImageDownloader class
        image_downloader = ImageDownloader()
    
        # Create an instance of the PDF class
        pdf = PDF(self.pdf_title, self.image_file)
        
        #Create the title page
        pdf.create_title_page()
        
        # Add pages to the PDF
        for i, product in enumerate(self.products):
            # Convert the prices to the selected currency
            product_price = converter.convert(float(product["price"]), "CNY", self.currency_code)
            # Use the selected currency to format the price
            product_price = "{}{:.2f}".format(self.currency_symbol, float(product_price) * self.price_multiplier)
            # Remove all emoji characters from the string
            product_name = re.sub(r'[^\x00-\x7F]', '', product['name'])
            pdf.add_page(product_name, product_price, image_downloader.download(image_url=product['image_url'], ref_url=self.url))
             
        # Show the "Save File" dialog
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)", options=options)
        
        if file_name:
            # Save the PDF file at the selected path
            pdf.create_pdf(file_name)
        
        

