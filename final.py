from PIL import Image, ImageDraw, ImageFont


## ---------------------------------------------------- Image Crop ---------------------------------------------------

def crop_image(image, crop_mode):
    # Open the input image
    im = image

    # Determine the dimensions of the input image
    width, height = im.size

    if crop_mode == "portrait":
        target_size = (1080,1350)
        # Crop to a portrait aspect ratio (e.g., 4:5)
        new_width = min(width, height * 4 // 5)
        left = (width - new_width) // 2
        top = 0
        right = left + new_width
        bottom = height
    elif crop_mode == "square":
        target_size = (1080,1080)
        # Crop to a square aspect ratio
        new_size = min(width, height)
        left = (width - new_size) // 2
        top = (height - new_size) // 2
        right = left + new_size
        bottom = top + new_size
    elif crop_mode == "story":
        # Crop to a story aspect ratio (9:16) for a typical mobile screen
        target_size = (1080,1920)
        width, height = im.size
        target_height = height
        target_width = int(target_height * 9 / 16)
        left = (width - target_width) // 2
        top = (height - target_height) // 2
        right = left + target_width
        bottom = top + target_height
    else:
        raise ValueError("Invalid crop mode. Supported modes: portrait, square, story")

    # Perform the crop
    cropped_im = im.crop((left, top, right, bottom))
    
    cropped_im.thumbnail(target_size, Image.Resampling.LANCZOS)
    return cropped_im


## ---------------------------------------------------- shadow gradient --------------------------------------------------


def gradient_from_bottom_to_top(image, gradient_magnitude=1.):
    im = image
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    
    width, height = im.size
    
    gradient = Image.new('L', (1, height), color=0xFF)
    
    for y in range(height):
        # Reverse the gradient by changing the calculation here
        gradient.putpixel((0, y), int(255 * (1 - gradient_magnitude * float(height - y) / height)))
    
    alpha = gradient.resize(im.size)
    
    black_im = Image.new('RGBA', (width, height), color=0) # i.e. black
    black_im.putalpha(alpha)
    
    gradient_im = Image.alpha_composite(im, black_im)
    # gradient_im.save('out.png', 'PNG')
    return gradient_im


### --------------------------------------------------  text wrap -------------------------------------------------- 
def text_wrap(text, max_width, font):

    lines = []
    # If the text width is smaller than the max_width, then no need to split, just return it
    if font.getlength(text) <= max_width:
        return text
    
    # Split the line by spaces to get words
    words = text.split(' ')
    i = 0
    wrapped_text = ''
    
    while i < len(words):
        line = ''
        while i < len(words) and font.getlength(line + words[i])  <= max_width:
            line = line + words[i] + " "
            i += 1
        if not line:
            line = words[i]
            i += 1
        lines.append(line)
    
    # Join the lines with newline characters
    wrapped_text = '\n'.join(lines)

    return wrapped_text


### ------------------------- reduce font size for wrapped text ------------------------------------

def fontSize_reduce(wrapped_text,max_height,font,font_size,font_path):
    draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))

    bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    while text_height > max_height:
        font_size -= 1
        # print("font size", font_size)
        font = ImageFont.truetype(font_path, font_size)
        bbox = draw.textbbox((0, 0), wrapped_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    
    return font


def add_logo(input_image, logo_image_path, max_width, max_height, position=(10,10)):

    # Open the logo image
    logo = Image.open(logo_image_path)

    # Get the current dimensions of the logo
    width, height = logo.size
    aspect_ratio = width / height

    # Calculate the new dimensions while maintaining the aspect ratio
    if width > max_width or height > max_height:
        if width > max_width:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
    else:
        # Enlarge the size while maintaining the aspect ratio
        if aspect_ratio > max_width / max_height:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)

    # Resize the image while maintaining the aspect ratio
    resized_logo = logo.resize((new_width, new_height))
    paste_position = position

    # Paste the logo onto the main image
    input_image.paste(resized_logo, paste_position,resized_logo)


def sample_template(text,input_img_path,output_img_path,crop_mode):

    original_image = Image.open(input_img_path)
    
    ## crop image for given crop mode
    # crop_mode = "square"
    cropped_image = crop_image(original_image, crop_mode)

    # adding gradient
    gradient_image = gradient_from_bottom_to_top(cropped_image, gradient_magnitude=2.)

    # adding Text

    # Take 10% to the left for min and 90% to the left for max
    x_min = (gradient_image.size[0] * 10) // 100
    x_max = (gradient_image.size[0] * 90) // 100
    max_width = x_max - x_min

    y_min = (gradient_image.size[1] * 75) // 100   # 75% from the top
    y_max = (gradient_image.size[1] * 85) //100   # 85% to the bottom

    max_height = (gradient_image.size[1] * 80) // 100   

    
    text = "This is a long multiline text that will be added to the image.It can have multiple lines.This is a long multiline text that will be added to the image.It can have multiple lines.This is a long multiline text that will be added to the image.It can have multiple lines.This is a long multiline text that will be added to the image.It can have multiple lines."
    font_path = r'C:\Windows\Fonts\MAGNETOB'
    font_size = (gradient_image.size[0] * 4) // 100
    font = ImageFont.truetype(font_path, font_size)

    wrapped_text= text_wrap(text, max_width, font)

    reduced_font = fontSize_reduce(wrapped_text,max_height,font,font_size,font_path)

    final_wrapped_text= text_wrap(text, max_width, reduced_font) 

    color = 'rgb(255,0,0)'
    draw = ImageDraw.Draw(gradient_image)
    draw.text((x_min,y_max), text=final_wrapped_text, font=reduced_font, anchor="ld", align='left')

    ### logo 
    logo_x = x_min
    logo_y = (gradient_image.size[1] * 90) //100

    logo_width = (gradient_image.size[0] * 10) // 100
    logo_height = ((gradient_image.size[1] * 98) // 100) - y_max
    logo_size= min(logo_width,logo_height)
    logo_image_path = r"images\image.png"
    add_logo(gradient_image, logo_image_path, logo_size, logo_size, position=(logo_x,logo_y))

    gradient_image.save(output_img_path)


def second_template(text,input_img_path,output_img_path,crop_mode):

    original_image = Image.open(input_img_path)
    
    ## crop image for given crop mode
    # crop_mode = "square"
    cropped_image = crop_image(original_image, crop_mode)

    # adding gradient
    gradient_image = gradient_from_bottom_to_top(cropped_image, gradient_magnitude=2.)

    # adding Text

    # Take 10% to the left for min and 90% to the left for max
    x_min = (gradient_image.size[0] * 10) // 100
    x_max = (gradient_image.size[0] * 90) // 100
    max_width = x_max - x_min

    # y_min = (gradient_image.size[1] * 75) // 100   # 75% from the top
    y_max = (gradient_image.size[1] * 85) //100   # 85% to the bottom

    max_height = (gradient_image.size[1] * 80) // 100   

    font_path = r'C:\Windows\Fonts\MAGNETOB'
    # font_size = (gradient_image.size[0] * 4) // 100
    font_size = 70
    font = ImageFont.truetype(font_path, font_size)

    wrapped_text= text_wrap(text, max_width, font)
    print(type(wrapped_text))
    reduced_font = fontSize_reduce(wrapped_text,max_height,font,font_size,font_path)

    final_wrapped_text= text_wrap(text, max_width, reduced_font) 

    color = 'rgb(255,0,0)'
    draw = ImageDraw.Draw(gradient_image)
    x = (gradient_image.size[0] * 50) // 100
    # draw.text((x,y_max), text=final_wrapped_text, font=reduced_font, anchor="md", align='center')
    draw.multiline_text((x,y_max), text=final_wrapped_text, font=reduced_font, anchor="md", spacing=30, align='center', stroke_width=0, embedded_color=False)
    
    
    ### logo 

    logo_width = (gradient_image.size[1] * 10) // 100
    logo_height = logo_width
    logo_image_path = r"images\image.png"

    logo_x = ((gradient_image.size[0] * 50) //100) - (logo_width // 2)
    logo_y = (gradient_image.size[1] * 90) //100
    
    add_logo(gradient_image, logo_image_path, logo_width, logo_height, position=(logo_x,logo_y))

    logo_width = (gradient_image.size[1] * 3) // 100
    logo_height = logo_width
    arrow_x = (gradient_image.size[0] * 93) //100
    arrow_y = (gradient_image.size[1] * 45) //100
    arrow_image_path = r'images\whiteArrow.png'
    add_logo(gradient_image, arrow_image_path, logo_width, logo_height, position=(arrow_x,arrow_y))
    
    gradient_image.save(output_img_path)


def logo_template(text,input_img_path,output_img_path,crop_mode):

    original_image = Image.open(input_img_path)
    
    ## crop image for given crop mode
    cropped_image = crop_image(original_image, crop_mode)

    gradient_image = cropped_image

    ### logo 

    logo_width = (gradient_image.size[1] * 15) // 100
    logo_height = logo_width
    logo_image_path = r"images\image.png"

    px = ((gradient_image.size[0] * 2) //100)
    py = ((gradient_image.size[1] * 2) //100)
    # logo_x = ((gradient_image.size[0] * 50) //100) - (logo_width // 2)
    # logo_y = (gradient_image.size[1] * 90) //100
    
    logo_x = gradient_image.size[0] - px - logo_width
    logo_y = py
    print(f'x= {logo_x} & y= {logo_y}')
    add_logo(gradient_image, logo_image_path, logo_width, logo_height, position=(logo_x,logo_y))


    gradient_image.save(output_img_path)



if __name__ == "__main__":
    input_img_path =r"images\wall-e.jpg"
    output_img_path = r"output_images\wall-e_logo.png"
    
    # input_img_path =r"images\minions.jpg"
    # output_img_path = r"output_images\minions_edit.png"

    text = "Blossoming with vibrant colors and delicate petals."
    crop_mode = "story"
    
    logo_template(text, input_img_path,output_img_path,crop_mode)