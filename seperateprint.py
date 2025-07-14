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


#takes an image and a limit value to separate colored pixels from gray pixels, return None if discarded
def seperate_page_color(image, limit=10, discard_empty=False):
    color_image = image.copy()
    gray_image = image.copy()

    image_data = image.load()
    color_image_data = color_image.load()
    gray_image_data = gray_image.load()
    width, height = image.size

    for pixelx in range(width): #iterate through each pixel
        for pixely in range(height):
            r,g,b = image_data[pixelx, pixely]

            if (abs(r-g) > limit) or (abs(r-b) > limit) or (abs(g-b) > limit): #remove colored pixels from gray image
                gray_image_data[pixelx, pixely] = 255,255,255
            
            else: #remove gray pixels from color image
                color_image_data[pixelx, pixely] = 255,255,255
    gray_image = gray_image.convert("L")

    if discard_empty: #discard page if blank white page
        extrema = gray_image.getextrema()
        if extrema[0] > 255 - limit:
            gray_image = None
        extrema = color_image.convert("L").getextrema()
        if extrema[0] > 255 - limit:
            color_image = None

    return gray_image, color_image


#Function to separate colored and gray pages from a PDF file
def seperate(input_path, limit=10, dpi=300, discard_empty=False):
    print("Converting PDF to images...")
    original_pages = image_to_pdf(input_path, dpi=dpi)
    color_pages = []
    gray_pages = []

    for page in original_pages:
        print("Separating colors from page. Page {} of {}...".format(original_pages.index(page) + 1, len(original_pages)))
        gray_image, color_image = seperate_page_color(page, limit=limit, discard_empty=discard_empty)
        if color_image:
            color_pages.append(color_image)
        if gray_image:
            gray_pages.append(gray_image)

    print("Saving separated pages as pdf...")
    path_cleaned = input_path.replace(".pdf", "")
    if color_pages:
        color_pages[0].save(path_cleaned + "_color.pdf", save_all=True, append_images=color_pages[1:], dpi=(dpi, dpi))
    if gray_pages:
        gray_pages[0].save(path_cleaned + "_gray.pdf", save_all=True, append_images=gray_pages[1:], dpi=(dpi, dpi))
    print("Done! Separated files saved as {}_color.pdf and {}_gray.pdf".format(path_cleaned, path_cleaned))


file = "a.pdf"
seperate(file, limit=30, discard_empty=True, dpi=300)