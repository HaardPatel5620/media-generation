from PIL import Image, ImageDraw, ImageFont


def crop_image(image, crop_mode):
    # Open the input image
    im = image

    # Determine the dimensions of the input image
    width, height = im.size

    if crop_mode == "portrait":
        target_size = (1080,1350)
        # Crop to a portrait aspect ratio (e.g., 4:5)
        new_height = height
        new_width = int(height * 4 // 5)
        
        if new_width > width:
            new_width = width
            new_height = int(new_width * 5 // 4)

        left = (width - new_width) // 2
        right = left + new_width
        top = (height - new_height) // 2
        bottom = top + new_height

    elif crop_mode == "square":
        target_size = (1080,1080)
        # Crop to a square aspect ratio
        new_size = min(width, height)
        left = (width - new_size) // 2
        right = left + new_size
        top = (height - new_size) // 2
        bottom = top + new_size

    elif crop_mode == "story":
        # Crop to a story aspect ratio (9:16) for a typical mobile screen
        target_size = (1080,1920)
        target_height = height
        target_width = int(target_height * 9 / 16)
        left = (width - target_width) // 2
        right = left + target_width
        top = (height - target_height) // 2
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
    logo = logo.convert("RGBA")
    
    # Get the current dimensions of the logo
    width, height = logo.size
    aspect_ratio = width / height
    print("###########",aspect_ratio)
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
    # print(logo_mask.size, logo_mask.mode)
    resized_logo = logo.resize((new_width, new_height))
    paste_position = position
    print(resized_logo.size, resized_logo.mode)

    # Paste the logo onto the main image
    input_image.paste(resized_logo, paste_position,resized_logo)


def draw_gradient_line(image, start, end, line_color, max_opacity=255, steps=1000, thickness=5):
    # Create a new image for the gradient line with RGBA mode
    image = image.convert("RGBA")
    
    gradient_line = Image.new("RGBA", image.size)
    draw = ImageDraw.Draw(gradient_line)

    print(gradient_line.size, gradient_line.mode)
    # Calculate the step size for x, y, and opacity
    delta_x = (end[0] - start[0]) / steps
    delta_y = (end[1] - start[1]) / steps
    delta_opacity = max_opacity / steps

    for i in range(steps):
        opacity = int(max_opacity - delta_opacity * i)
        x = start[0] + delta_x * i
        y = start[1] + delta_y * i

        # Draw a line with a smooth gradient effect on the gradient_line image
        draw.line([(x - thickness / 2, y), (x + thickness / 2, y)], fill=line_color + (opacity,), width=thickness)

    # Paste the gradient_line onto the original image
    image = Image.alpha_composite(image, gradient_line)

    return image