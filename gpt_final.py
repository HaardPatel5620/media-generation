from PIL import Image, ImageDraw, ImageFont

# Image Editing Functions

def crop_image(image, crop_mode):
    # Determine the dimensions of the input image
    width, height = image.size

    if crop_mode == "portrait":
        # Crop to a portrait aspect ratio (e.g., 4:5)
        new_width = min(width, height * 4 // 5)
        left = (width - new_width) // 2
        top = 0
        right = left + new_width
        bottom = height
    elif crop_mode == "square":
        # Crop to a square aspect ratio
        new_size = min(width, height)
        left = (width - new_size) // 2
        top = (height - new_size) // 2
        right = left + new_size
        bottom = top + new_size
    elif crop_mode == "story":
        # Crop to a story aspect ratio (9:16) for a typical mobile screen
        target_width = int(height * 9 / 16)
        left = (width - target_width) // 2
        top = (height - height) // 2
        right = left + target_width
        bottom = top + height
    else:
        raise ValueError("Invalid crop mode. Supported modes: portrait, square, story")

    # Perform the crop
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image

def gradient_from_bottom_to_top(image, gradient_magnitude=1.):
    # Add a gradient from bottom to top of the image
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    width, height = image.size
    gradient = Image.new('L', (1, height), color=0xFF)
    
    for y in range(height):
        # Reverse the gradient by changing the calculation here
        gradient.putpixel((0, y), int(255 * (1 - gradient_magnitude * float(height - y) / height)))
    
    alpha = gradient.resize(image.size)
    black_image = Image.new('RGBA', (width, height), color=0)
    black_image.putalpha(alpha)
    gradient_image = Image.alpha_composite(image, black_image)
    return gradient_image

# Text Functions

def text_wrap(text, max_width, font):
    # Wrap text to fit within the specified max_width
    lines = []
    if font.getlength(text) <= max_width:
        return text
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
    
    wrapped_text = '\n'.join(lines)
    return wrapped_text

def fontSize_reduce(wrapped_text, max_height, font, font_size, font_path):
    draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    while text_height > max_height:
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        bbox = draw.textbbox((0, 0), wrapped_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    
    return font

# Image Editing and Composition

def add_logo(input_image, logo_image_path, max_width, max_height, position=(10, 10)):
    logo = Image.open(logo_image_path)
    width, height = logo.size
    aspect_ratio = width / height

    if width > max_width or height > max_height:
        if width > max_width:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
    else:
        if aspect_ratio > max_width / max_height:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)

    resized_logo = logo.resize((new_width, new_height))
    paste_position = position
    input_image.paste(resized_logo, paste_position, resized_logo)

# Templates

def sample_template(text, input_img_path, output_img_path, crop_mode):
    original_image = Image.open(input_img_path)
    cropped_image = crop_image(original_image, crop_mode)
    gradient_image = gradient_from_bottom_to_top(cropped_image, gradient_magnitude=2.)

    x_min = (gradient_image.size[0] * 10) // 100
    x_max = (gradient_image.size[0] * 90) // 100
    max_width = x_max - x_min
    y_max = (gradient_image.size[1] * 85) // 100
    max_height = (gradient_image.size[1] * 80) // 100

    font_path = r'C:\Windows\Fonts\MAGNETOB'
    font_size = (gradient_image.size[0] * 4) // 100
    font = ImageFont.truetype(font_path, font_size)
    
    wrapped_text = text_wrap(text, max_width, font)
    reduced_font = fontSize_reduce(wrapped_text, max_height, font, font_size, font_path)
    final_wrapped_text = text_wrap(text, max_width, reduced_font)

    draw = ImageDraw.Draw(gradient_image)
    x = (gradient_image.size[0] * 50) // 100
    # draw.multiline_text((x, y_max), text=final_wrapped_text, font=reduced_font, anchor="md", spacing=30, align='center', stroke_width=0, embedded_color=False)
    
    # highlight_offset = 3
    # highlight_color = "rgb(255, 255, 0)"
    # # x, y = (x, y_max)
    # x += highlight_offset
    # draw.text((x, y_max), final_wrapped_text, font=reduced_font, anchor="md", spacing=30, fill=highlight_color,)
    # x -= highlight_offset
    # draw.text((x, y_max), final_wrapped_text, font=reduced_font, anchor="md", spacing=30)




    # Create a bounding box for the highlighted background
    highlight_color = "rgb(255, 255, 0)"
    text_bbox = draw.textbbox((x, y_max), final_wrapped_text, font=reduced_font)
    padding = 10  # Adjust the padding as needed
    highlight_bbox = (text_bbox[0] - padding, text_bbox[1] - padding, text_bbox[2] + padding, text_bbox[3] + padding)
    
    # Draw the highlighted background
    draw.rectangle(highlight_bbox, fill=highlight_color)
    
    # Draw the main text on top of the highlight
    draw.text((x, y_max), text=final_wrapped_text, font=reduced_font, anchor="md")




    logo_width = (gradient_image.size[1] * 10) // 100
    logo_height = logo_width
    logo_image_path = r"images\image.png"
    logo_x = ((gradient_image.size[0] * 50) // 100) - (logo_width // 2)
    logo_y = (gradient_image.size[1] * 90) // 100
    add_logo(gradient_image, logo_image_path, logo_width, logo_height, position=(logo_x, logo_y))

    logo_width = (gradient_image.size[1] * 3) // 100
    logo_height = logo_width
    arrow_x = (gradient_image.size[0] * 93) // 100
    arrow_y = (gradient_image.size[1] * 45) // 100
    arrow_image_path = r'images\whiteArrow.png'
    add_logo(gradient_image, arrow_image_path, logo_width, logo_height, position=(arrow_x, arrow_y))
    print("befor save")
    gradient_image.save(output_img_path)

if __name__ == "__main__":
    input_img_path = r"images\wall-e.jpg"
    output_img_path = r"output_images\wall-e_edit_hl1.png"
    text = "Blossoming with vibrant colors and delicate petals.Blossoming with vibrant colors and delicate petals"
    crop_mode = "square"
    sample_template(text, input_img_path, output_img_path, crop_mode)
