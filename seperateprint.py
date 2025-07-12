from PIL import Image
import pymupdf



#convert pdf file to image object
def image_to_pdf(file_path, dpi=300):
    zoom = dpi / 72  # zoom factor, standard: 72 dpi
    magnify = pymupdf.Matrix(zoom, zoom)
    doc = pymupdf.open(file_path)

    pages = []
    for page in doc:
        pix = page.get_pixmap(matrix=magnify)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pages.append(img)

    return pages


#takes an image and a limit value to separate colored pixels from gray pixels.
def seperate_page_color(image, limit=10):
    color_image = image.copy()
    gray_image = image.copy()

    image_data = image.load()
    color_image_data = color_image.load()
    gray_image_data = gray_image.load()
    height,width = image.size

    #iterate through each pixel
    for pixely in range(height):
        for pixelx in range(width):
            r,g,b = image_data[pixely, pixelx]

            #remove colored pixels from gray image
            if (abs(r-g) >limit) or (abs(r-b) > limit) or (abs(g-b) > limit):
                gray_image_data[pixely, pixelx] = 255,255,255
            
            #remove gray pixels from color image
            else:
                color_image_data[pixely, pixelx] = 255,255,255
    gray_image = gray_image.convert("L")
    return gray_image, color_image


#Function to separate colored and gray pages from a PDF file
def seperate(input_path, limit=10, dpi=300):
    original_pages = image_to_pdf(input_path, dpi=dpi)
    color_pages = []
    gray_pages = []
    for page in original_pages:
        gray_image, color_image = seperate_page_color(page, limit=limit)
        color_pages.append(color_image)
        gray_pages.append(gray_image)

    color_pages[0].save(input_path.replace(".pdf", "_color.pdf"), save_all=True, append_images=color_pages[1:], dpi=(dpi, dpi))
    gray_pages[0].save(input_path.replace(".pdf", "_gray.pdf"), save_all=True, append_images=gray_pages[1:], dpi=(dpi, dpi))



seperate("aaa.pdf", limit=10)