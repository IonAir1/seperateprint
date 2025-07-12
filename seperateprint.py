from PIL import Image, ImageDraw, ImageFont
import pymupdf


def image_to_pdf(file_path, output_path, dpi=300):
    zoom = dpi / 72  # zoom factor, standard: 72 dpi
    magnify = pymupdf.Matrix(zoom, zoom)
    doc = pymupdf.open(file_path)
    for page in doc:
        pix = page.get_pixmap(matrix=magnify)
        pix.save(output_path)

image_to_pdf('input.pdf', 'temp.png')