from PIL import Image, ImageDraw, ImageFont


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
        
        # Adjust dimensions if the cropped image is smaller than the target size
        if new_width < target_size[0]:
            left = max(0, left - (target_size[0] - new_width) // 2)
            right = left + target_size[0]

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
    
    # cropped_im.thumbnail(target_size, Image.Resampling.LANCZOS) # maintain its aspect ratio
    cropped_im = cropped_im.resize(target_size)

    return cropped_im


def gradient_bottom_to_top(image,darkness = 0.8, gradient_magnitude=1., gradient_color = (0, 0, 0)):
    im = image
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    
    width, height = im.size
    
    gradient = Image.new('L', (1, height), color=0xFF)
    
    for y in range(height):
        # Reverse the gradient by changing the calculation here
        gradient.putpixel((0, y), int(255 * (darkness - gradient_magnitude * float(height - y) / height)))
    
    alpha = gradient.resize(im.size)
    
    black_im = Image.new('RGBA', (width, height), color=gradient_color) # i.e. black
    black_im.putalpha(alpha)
    
    gradient_im = Image.alpha_composite(im, black_im)
    # gradient_im.save('out.png', 'PNG')
    return gradient_im


def gradient_left_to_right(image, gradient_magnitude=1.):
    im = image
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    
    width, height = im.size
    
    gradient = Image.new('L', (width, 1), color=0xFF)
    
    for x in range(width):
        # Create a left-to-right gradient
        gradient.putpixel((x, 0), int(255 * (0.6 - gradient_magnitude * float(x) / width)))
    
    alpha = gradient.resize(im.size)
    
    black_im = Image.new('RGBA', (width, height), color=0)  # i.e. black
    black_im.putalpha(alpha)
    
    gradient_im = Image.alpha_composite(im, black_im)
    
    return gradient_im


def gradient_top_left_to_bottom_right(image, gradient_magnitude=1.):
    im = image
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    
    width, height = im.size
    
    gradient = Image.new('L', (width, height))
    
    for x in range(width):
        for y in range(height):
            # Create a gradient from top left to bottom right
            alpha_value = int(255 * (0.8 - gradient_magnitude * (x + y) / (width + height)))
            gradient.putpixel((x, y), alpha_value)
    
    black_im = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))  # Fully transparent background
    black_im.putalpha(gradient)
    
    gradient_im = Image.alpha_composite(im, black_im)
    
    return gradient_im


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
