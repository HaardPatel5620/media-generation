from PIL import Image, ImageDraw, ImageFont


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


def fontSize_reduce(wrapped_text,max_height,font,font_size,font_path,spacing):
    draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))

    bbox = draw.textbbox((0, 0), wrapped_text, font=font, spacing = spacing)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    while text_height > max_height:
        font_size -= 1
        spacing -= 1 
        # print("font size", font_size)
        font = ImageFont.truetype(font_path, font_size)
        bbox = draw.textbbox((0, 0), wrapped_text, font=font, spacing = spacing)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    
    return font
