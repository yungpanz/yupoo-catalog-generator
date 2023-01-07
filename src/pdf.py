import datetime

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

class PDF:
  def __init__(self, title, image_path):
    self.title = title
    self.image_path = image_path
    self.pages = []

  def add_page(self, product_name, price, image_path):
    page = (product_name, price, image_path)
    self.pages.append(page)

  def create_title_page(self):
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    self.add_page(self.title, timestamp, self.image_path)

  def create_pdf(self, pdf_path):
    # create a new PDF with Reportlab
    pdf_canvas = Canvas(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()

    for product_name, price, image_path in self.pages:
      if product_name == self.title:
        # add the title
        title_paragraph = Paragraph(product_name, styles['Heading1'])
        title_paragraph.wrapOn(pdf_canvas, 700, 200)
        title_paragraph.drawOn(pdf_canvas, 50, 750)
        # add the timestamp
        pdf_canvas.drawString(100, 50, price)
        # add the cover image, resizing if necessary
        image_width, image_height = pdf_canvas.drawImage(image_path, x=50, y=150, width=500, height=500, preserveAspectRatio=True)
        if image_width > 500 or image_height > 500:
            pdf_canvas.drawImage(image_path, x=50, y=150, width=500, height=500)
      else:
        # add the product name
        product_paragraph = Paragraph(product_name, styles['Heading2'])
        product_paragraph.wrapOn(pdf_canvas, 500, 200)
        product_paragraph.drawOn(pdf_canvas, 100, 750)
        # add the price with a monospace font
        pdf_canvas.setFont('Courier', 14)
        pdf_canvas.drawString(100, 700, price)
        # add the image
        pdf_canvas.drawImage(image_path, x=100, y=100, width=400, height=400)
      # create a new page
      pdf_canvas.showPage()

    # save the PDF
    pdf_canvas.save()

