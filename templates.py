from PIL import Image, ImageDraw, ImageFont
from text_mods import text_wrap, fontSize_reduce
from img_mods import crop_image, add_logo, gradient_bottom_to_top, gradient_top_left_to_bottom_right
from decouple import config


font_path = config("FONT_PATH")
arrow_image_path = config("ARROW_IMG_PATH")
reverse_arrow_white_path = config("REVERSE_ARROWS_WHITE")
logo_image_path = config("LOGO_IMG_PATH")
white_quote_image_path = config("WHITE_QUOTE_IMG_PATH")
quote_image_path = config("QUOTE_IMG_PATH")
reverse_quote_image_path = config("REVERSE_QUOTE_IMG_PATH")
location_image_path = config("LOCATION_IMG_PATH")
down_arrow_image_path = config("DOWN_ARROW_IMG_PATH")
faded_arrow_path = config("FADED_ARROW_IMG_PATH")
web_story_2_img_path = config("WEB_STORY_IMG_PATH")
underline_img_path = config("CURL_UNDERLLINE_IMG_PATH")
underline_long_img_path = config("CURL_UNDERLLINE_LONG_IMG_PATH")
faded_line_path = config("FADED_LINE_IMG_PATH")
story2_img_path = config("STORY2_IMG_PATH")


def highlighted_text(draw, final_wrapped_text, highlight_text, x_min, y_text,  reduced_font, highlight_background_color, highlight_color, color):

    lines = final_wrapped_text.split("\n")
    hl_words = highlight_text.split()
    line_index = 0
    while line_index < len(lines):
        hl_index = 0
        single_line_words = ""
        while hl_words:
            if hl_words[hl_index] in lines[line_index]:
                single_line_words += hl_words[hl_index] + " "
                del hl_words[hl_index]
            else:
                break

        # if single_line_words:
        text_to_hl = single_line_words.strip()
        line_parts = lines[line_index].split(text_to_hl) if text_to_hl and text_to_hl in lines[line_index] else None
        if line_parts:
            x_text = x_min 
            for part in line_parts[:-1]:
                draw.text((x_text, y_text), part, font=reduced_font, fill=color, anchor="la")
                x_text += draw.textlength(part, font=reduced_font)

                # Draw a yellow background rectangle behind the highlighted part
                hl_width = draw.textlength(text_to_hl, font=reduced_font)
                left, top, right, bottom = reduced_font.getbbox("AAA AAA")
                hl_height = bottom - top
                
                rectangle_coords = (x_text , y_text + 5, x_text + hl_width , y_text + hl_height + (hl_height*60)//100)
                draw.rectangle(rectangle_coords, fill=highlight_background_color)

                draw.text((x_text, y_text), text_to_hl, font=reduced_font, fill=highlight_color, anchor="la")
                x_text += draw.textlength(text_to_hl, font=reduced_font)
            draw.text((x_text, y_text), line_parts[-1], font=reduced_font, fill=color, anchor="la")
        else:
            draw.text((x_min, y_text), lines[line_index], font=reduced_font, fill=color, anchor="la")
        
        left, top, right, bottom = reduced_font.getbbox(lines[line_index])
        text_width = right - left
        text_height = bottom - top
        y_text += text_height + 20
        line_index += 1


def template_preprocess(
    text, input_img_path, crop_mode, font_path, font_size_perc, x_mn_prc, x_mx_prc, y_mn_prc, y_mx_prc, mx_height_perc):
     
        original_image = Image.open(input_img_path)
        cropped_image = crop_image(original_image, crop_mode)
        gradient_image = cropped_image

        x_min = (gradient_image.size[0] * x_mn_prc) // 100
        x_max = (gradient_image.size[0] * x_mx_prc) // 100
        max_width = x_max - x_min

        y_min = (gradient_image.size[1] * y_mn_prc) // 100
        y_max = (gradient_image.size[1] * y_mx_prc) // 100
        max_height = (gradient_image.size[1] * mx_height_perc) // 100

        font_size = (gradient_image.size[0] * font_size_perc) // 100
        font = ImageFont.truetype(font_path, font_size)
        spacing = 25

        wrapped_text = text_wrap(text, max_width, font)

        reduced_font = fontSize_reduce(
            wrapped_text, max_height, font, font_size, font_path,spacing
        )

        final_wrapped_text = text_wrap(text, max_width, reduced_font)
        return gradient_image, x_min, x_max, y_min, y_max, reduced_font, final_wrapped_text
    

def feed_basic(text, input_img_path, output_img_path, crop_mode, arrow):
     
    gradient_image, x_min, x_max, y_min, y_max, reduced_font, final_wrapped_text = template_preprocess(text, input_img_path, crop_mode, font_path, font_size_perc = 7, x_mn_prc=10, x_mx_prc=90, y_mn_prc=75, y_mx_prc=85, mx_height_perc=70)
    gradient_image = gradient_bottom_to_top(gradient_image, gradient_magnitude=2.)
    
    color = "rgb(255,0,0)"
    draw = ImageDraw.Draw(gradient_image)
    draw.text(
        (x_min, y_max),
        text=final_wrapped_text,
        font=reduced_font,
        anchor="ld",
        spacing = 25,
        align="left",
    )

    ### logo
    logo_width = (gradient_image.size[0] * 12) // 100
    logo_height = logo_width
    logo_x = x_min
    logo_y = (gradient_image.size[1] * 90) // 100 - logo_height//3

    add_logo(
        gradient_image, logo_image_path, logo_width, logo_height, position=(logo_x, logo_y)
    )

    ## arrow
    if arrow == "show":
        bbox = draw.multiline_textbbox((x_min, y_max), final_wrapped_text, font=reduced_font, anchor="ld",spacing=25)
        text_height = bbox[3] - bbox[1]

        arrow_width = (gradient_image.size[0] * 6) // 100
        arrow_height = logo_width
        arrow_x = x_max
        arrow_y = max(min((y_max- text_height - logo_height), gradient_image.size[1]//2), 30)
        add_logo(
            gradient_image,
            arrow_image_path,
            arrow_width,
            arrow_height,
            position=(arrow_x, arrow_y),
        )
    
    gradient_image.save(output_img_path,'PNG')
    

def feed_swipe(text, input_img_path, output_img_path, crop_mode, arrow):
     
    gradient_image, x_min, x_max, y_min, y_max, reduced_font, final_wrapped_text = template_preprocess(text, input_img_path, crop_mode, font_path, font_size_perc = 7, x_mn_prc=10, x_mx_prc=90, y_mn_prc=75, y_mx_prc=85, mx_height_perc=80)
    gradient_image = gradient_bottom_to_top(gradient_image, gradient_magnitude=2.)

    draw = ImageDraw.Draw(gradient_image)
    x = (gradient_image.size[0] * 50) // 100
    
    draw.multiline_text(
        (x, y_max),
        text=final_wrapped_text,
        font=reduced_font,
        anchor="md",
        spacing=25,
        align="center",
        embedded_color=False,
    )

    ### logo
    logo_width = (gradient_image.size[0] * 12) // 100
    logo_height = logo_width
    
    logo_x = ((gradient_image.size[0] * 50) // 100) - (logo_width // 2)
    logo_y = y_max + reduced_font.size//2

    add_logo(
        gradient_image,
        logo_image_path,
        logo_width,
        logo_height,
        position=(logo_x, logo_y),
    )

    ## arrow
    if arrow == "show":
        arrow_width = (gradient_image.size[0] * 6) // 100
        arrow_height = arrow_width
        arrow_x = x_max
        arrow_y = (gradient_image.size[1] * 50) // 100 - arrow_height//2
        add_logo(
            gradient_image,
            arrow_image_path,
            arrow_width,
            arrow_height,
            position=(arrow_x, arrow_y),
        )

    gradient_image.save(output_img_path,'PNG')


def highlight_template(text, input_img_path, output_img_path, crop_mode, arrow, text_to_hl=None):
     
    gradient_image, x_min, x_max, _, y_max, reduced_font, final_wrapped_text = template_preprocess(
        text, input_img_path, crop_mode, font_path, font_size_perc = 7, x_mn_prc=10, x_mx_prc=90, y_mn_prc=75, y_mx_prc=85, mx_height_perc=80
    )
    gradient_image = gradient_bottom_to_top(gradient_image, gradient_magnitude=2.)

    color = "rgb(255,255,255)"
    highlight_color = "rgb(0, 0, 0)"
    highlight_background_color = "rgb(255, 255, 0)"
    draw = ImageDraw.Draw(gradient_image)
    
    ## logo 
    logo_width = (gradient_image.size[0] * 12) // 100
    logo_height = logo_width
    logo_x = x_min
    logo_y = (gradient_image.size[1] * 90) // 100 - logo_height//3
    add_logo(gradient_image, logo_image_path, logo_width, logo_height, position=(logo_x, logo_y))

    left, top, right, bottom = draw.multiline_textbbox((x_max,y_max),final_wrapped_text,font=reduced_font,anchor= "ld", spacing=20)
    y_text = top
    
    highlighted_text(draw, final_wrapped_text, text_to_hl, x_min, y_text, reduced_font, highlight_background_color, highlight_color, color)


    ## arrow
    if arrow == "show":
        bbox = draw.multiline_textbbox((x_min, y_max), final_wrapped_text, font=reduced_font, anchor="ld",spacing=25)
        text_height = bbox[3] - bbox[1]

        arrow_width = (gradient_image.size[0] * 6) // 100
        arrow_height = logo_width
        arrow_x = x_max
        arrow_y = max(min((y_max- text_height - logo_height), gradient_image.size[1]//2), 30)
        add_logo(
            gradient_image,
            arrow_image_path,
            arrow_width,
            arrow_height,
            position=(arrow_x, arrow_y),
        )

    gradient_image.save(output_img_path,'PNG')


def logo_only(input_img_path, output_img_path, crop_mode, logo_position):
     
    original_image = Image.open(input_img_path)
    
    ## crop image for given crop mode
    cropped_image = crop_image(original_image, crop_mode)
    gradient_image = cropped_image

    ### logo 
    logo_width = (gradient_image.size[0] * 12) // 100
    logo_height = logo_width

    px = ((gradient_image.size[0] * 4) //100)
    py = ((gradient_image.size[1] * 2) //100)

    position_dict = {
        1: (px, py),
        2: ((gradient_image.size[0] // 2) - (logo_width // 2), py),
        3: (gradient_image.size[0] - px - logo_width, py),
        4: (px, gradient_image.size[1] - py - logo_height),
        5: ((gradient_image.size[0] // 2) - (logo_width // 2), gradient_image.size[1] - py - logo_height),
        6: (gradient_image.size[0] - px - logo_width, gradient_image.size[1] - py - logo_height),
    }

    # Use the dictionary to set logo_x and logo_y based on logo_position
    if logo_position in position_dict:
        logo_x, logo_y = position_dict[logo_position]
        add_logo(gradient_image, logo_image_path, logo_width, logo_height, position=(logo_x,logo_y))

    elif logo_position == 7:
        # logo_width = (gradient_image.size[0] * 20) // 100
        # logo_height = (gradient_image.size[1] * 20) // 100
        logo_width = 324
        logo_height = 272
        
        logo_x,logo_y = ((gradient_image.size[0] // 2) - (logo_width // 2), (gradient_image.size[1] // 2))
        logo = Image.open(logo_image_path)
        resized_logo = logo.resize((324, 272))

        img = resized_logo.convert("RGBA")
        
        datas = img.getdata()
        newData = []
    
        for item in datas:
            if item[0] != 0 and item[1] != 0 and item[2] != 0:
                newData.append((item[0], item[1], item[2], 70))
            else:
                newData.append(item)
        img.putdata(newData)

        # # Define the paste position
        paste_position = (logo_x,logo_y - logo_width//2) # Adjust the position where you want to paste the logo

        # # Paste the resized and transparent logo onto the input image
        gradient_image.paste(img, paste_position, img)

    gradient_image.save(output_img_path,'PNG')
    

def web_news(text, sub_text, text_to_hl, input_img_path, output_img_path,crop_mode, arrow):
    
    gradient_image, x_min, x_max, _, _, reduced_font, final_wrapped_text = template_preprocess(text, input_img_path, crop_mode, font_path, font_size_perc = 7, x_mn_prc=15, x_mx_prc=90, y_mn_prc=75, y_mx_prc=85, mx_height_perc=65)
    gradient_image = gradient_bottom_to_top(gradient_image, gradient_magnitude=1.)
    
    y = (gradient_image.size[1] * 80) //100
    y_temp = (gradient_image.size[1] * 5) //100
    
    color = "rgb(255,255,255)"
    highlight_color = "rgb(0, 0, 0)"
    highlight_background_color = "rgb(255, 255, 0)"
    draw = ImageDraw.Draw(gradient_image)

    # sub_text
    _, x_min_sub, _, _, _, sub_font, final_wrapped_sub_text = template_preprocess(sub_text, input_img_path, crop_mode, font_path, font_size_perc = 4, x_mn_prc=15, x_mx_prc=70, y_mn_prc=75, y_mx_prc=85, mx_height_perc=80)
    
    y_sub = (gradient_image.size[1] * 90) //100
    color_sub = 'rgb(255,255,0)'
    draw.text((x_min_sub,y_sub), text=final_wrapped_sub_text, fill = color_sub, font=sub_font, anchor="ld", spacing=5, align='left', stroke_width=0, embedded_color=False)

    bbox = draw.multiline_textbbox((x_min,y), final_wrapped_text, font=reduced_font, anchor="ld",spacing=20)
    text_height_init = bbox[3] - bbox[1]
    y_text = max((y - text_height_init - reduced_font.size), y_temp)

    ## text with highlight
    highlighted_text(draw, final_wrapped_text, text_to_hl, x_min, y_text, reduced_font, highlight_background_color, highlight_color, color)
    
    ### logo 
    logo_width = (gradient_image.size[0] * 12) // 100
    logo_height = logo_width
    
    logo_x = x_max - logo_width
    logo_y = y_sub - logo_height//2   ## it's temp solution, use logo_height only do not devide by 2 
    
    add_logo(gradient_image, logo_image_path, logo_width, logo_height, position=(logo_x,logo_y))

    ## line
    line_x = (gradient_image.size[0] * 5) // 100
    line_color =  (255, 255, 0)  # RGB color, here it's yellow
    line_width = 3  # Line width in pixels
    
    start_point = (x_min - line_x, y_sub)
    end_point = (x_min - line_x, max((y - text_height_init -reduced_font.size),y_temp))
    draw.line([start_point, end_point], fill=line_color, width=line_width)
    
    point_color =  (255, 255, 0)  # RGB color, here it's yellow
    point_size = 7  # Point size in pixels
    point_end = start_point
    draw.ellipse((point_end[0] - point_size, point_end[1] - point_size, point_end[0] + point_size, point_end[1] + point_size), fill=point_color)

    ## arrow 
    if arrow == "show":
        arrow_width = (gradient_image.size[0] * 6) // 100
        arrow_height = arrow_width
        arrow_x = x_max
        arrow_y = max((bbox[1] - 2*reduced_font.size - arrow_height//2), 30)
        add_logo(
            gradient_image,
            arrow_image_path,
            arrow_width,
            arrow_height,
            position=(arrow_x, arrow_y),
        )


    gradient_image.save(output_img_path,'PNG')    


def citim(text, sub_text, input_img_path,output_img_path,crop_mode):
    

    gradient_image, x_min, x_max, _, _, reduced_font, final_wrapped_text = template_preprocess(
        text, input_img_path, crop_mode, font_path, font_size_perc = 7, 
        x_mn_prc=10, x_mx_prc=90, 
        y_mn_prc=85, y_mx_prc=85, mx_height_perc=50)
    
    gradient_image = gradient_bottom_to_top(gradient_image, darkness=1, gradient_magnitude=2.)

    draw = ImageDraw.Draw(gradient_image)
    y = (gradient_image.size[1] * 80) //100
    draw.multiline_text((x_min,y), text=final_wrapped_text, font=reduced_font, anchor="ld", spacing=25, align='left')
    
    ## sub text
    _, x_min_sub, _, _, y_max_sub, sub_font, final_wrapped_sub_text = template_preprocess(sub_text, input_img_path, crop_mode, font_path, font_size_perc = 3, x_mn_prc=15, x_mx_prc=70, y_mn_prc=75, y_mx_prc=90, mx_height_perc=80)
    color = 'rgb(255,255,0)'
    draw.text((x_min,y_max_sub), text=final_wrapped_sub_text, font=sub_font, anchor="ld", spacing=5, align='left')
    
    # Define the curly brace underline position
    left, top, right, bottom = draw.multiline_textbbox((x_min,y_max_sub), final_wrapped_sub_text, font=sub_font, anchor="ld",spacing=5)
    text_width = right - left
    # Open the underline_img image
    underline_img = Image.open(underline_img_path)
    # Get the current dimensions of the underline_img
    width, height = underline_img.size

    # if width < text_width:
    underline_long_img = Image.open(underline_img_path)
    _, height = underline_long_img.size

    w_var = max(text_width, 30)
    h_var = max(int(height//2), 10)

    resized_curl = underline_long_img.resize((w_var, h_var))
    height = resized_curl.size[1]
    paste_position = (left, bottom + height//3)
    # else:
    #     # height = int(height * text_width / width) *10
    #     original_width, original_height = width, height
    #     w = text_width
    #     # Calculate the new height while maintaining the aspect ratio
    #     h = original_height * w / original_width

    #     # Calculate how much to crop from both sides
    #     crop_amount = (original_width - w) / 2

    #     # Define the cropping coordinates
    #     l = crop_amount
    #     r = original_width - crop_amount
    #     t = 0
    #     b = original_height
    #     # Crop the image
    #     resized_curl = underline_img.crop((l, t, r, b))
    #     # h_var = max(text_width//8, 10)
    #     h_var = max(int(h - text_width//15), 10)

    #     # Resize the cropped image to the desired (w, h) size
    #     resized_curl = resized_curl.resize((w, int(h//1.5)))
    #     height = resized_curl.size[1]
    #     paste_position = (left, bottom + int(height//3))
        

    # Paste the underline_img onto the main image
    gradient_image.paste(resized_curl, paste_position,resized_curl)

    ### logo 
    logo_width = (gradient_image.size[0] * 12) // 100
    logo_height = logo_width
    logo_x = x_max - logo_width
    logo_y = y_max_sub - logo_height//2  
    
    add_logo(gradient_image, logo_image_path, logo_width, logo_height, position=(logo_x,logo_y))

    ## quote 
    bbox = draw.multiline_textbbox((x_min,y), final_wrapped_text, font=reduced_font, anchor="ld",spacing=25)
    line_height = bbox[3] - bbox[1]

    quote_width = (gradient_image.size[1] * 12) // 100
    quote_height = quote_width
    quote_x = x_min
    quote_y = y - line_height - quote_height
    add_logo(gradient_image, white_quote_image_path, quote_width, quote_height, position=(quote_x,quote_y))
    
    gradient_image.save(output_img_path,'PNG')


def iconic_location(text, input_img_path, output_img_path, crop_mode):
     
    gradient_image, x_min, x_max, y_min, y_max, reduced_font, final_wrapped_text = template_preprocess(text, input_img_path, crop_mode, font_path, font_size_perc = 4, x_mn_prc=50, x_mx_prc=95, y_mn_prc=75, y_mx_prc=95, mx_height_perc=80)
    gradient_image = gradient_bottom_to_top(gradient_image, gradient_magnitude=2.)

    color = "rgb(255,0,0)"
    draw = ImageDraw.Draw(gradient_image)
    
    if len(text) != 0:
        draw.text(
            (x_max, y_max),
            text=final_wrapped_text,
            font=reduced_font,
            anchor="rd",
            spacing = 15,
            align="left",
        )
        
        # location logo
        bbox = draw.multiline_textbbox((x_max, y_max), final_wrapped_text, font=reduced_font, anchor="rd",spacing=15)
        line_width = int(bbox[2] - bbox[0])

        left, top, right, bottom = reduced_font.getbbox("A")
        Atext_height = bottom - top
        Atext_width = right - left
        
        location_height = Atext_width + Atext_width//3
        location_x = (x_max - int(1.5*Atext_width) - line_width)
        location_y = bbox[1] - location_height//7   ## //5 if bottom to match 
        add_logo(
            gradient_image,
            location_image_path,
            location_height,
            location_height,
            position=(location_x, location_y),
        )
    
    ### logo
    logo_x = (gradient_image.size[0] * 5) // 100
    logo_y = (gradient_image.size[1] * 5) // 100

    logo_width = (gradient_image.size[0] * 12) // 100
    logo_height = logo_width
    
    add_logo(
        gradient_image, logo_image_path, logo_height, logo_height, position=(logo_x, logo_y)
    )

    
    # hashed text 
    draw.text(
        (logo_x, y_max),
        text="#iconicalbania",
        font=reduced_font,
        anchor="ld",
        spacing = 5,
        align="left",
    )

    gradient_image.save(output_img_path,'PNG')


def feed_location(text, input_img_path, output_img_path, crop_mode, location, arrow):
    
    gradient_image, x_min, x_max, y_min, y_max, reduced_font, final_wrapped_text = template_preprocess(text, input_img_path, crop_mode, font_path, font_size_perc = 7, x_mn_prc=15, x_mx_prc=95, y_mn_prc=75, y_mx_prc=95, mx_height_perc=70)
    gradient_image = gradient_bottom_to_top(gradient_image, gradient_magnitude=2.)

    draw = ImageDraw.Draw(gradient_image)
    draw.text(
        (x_max, y_max),
        text=final_wrapped_text,
        font=reduced_font,
        anchor="rd",
        spacing = 25,
        align="right",
    )
    
    ### logo
    bbox = draw.multiline_textbbox((x_max, y_max), final_wrapped_text, font=reduced_font, anchor="rd",spacing=25)
    text_height = bbox[3] - bbox[1]

    logo_width = (gradient_image.size[0] * 12) // 100
    logo_height = logo_width
    logo_x = x_max - logo_width
    logo_y = y_max- text_height - logo_height

    add_logo(
        gradient_image, logo_image_path, logo_width, logo_height, position=(logo_x, logo_y)
    )

    ## location
    _ , x_min_location, x_max_location, y_min_location, y_max_location, reduced_font_location, final_wrapped_location = template_preprocess(location, input_img_path, crop_mode, font_path, font_size_perc = 5, x_mn_prc=50, x_mx_prc=95, y_mn_prc=75, y_mx_prc=95, mx_height_perc=80)

    y = (gradient_image.size[1] * 5) // 100
    lcoation_text_x = logo_x - reduced_font_location.size//2
    lcoation_text_y = logo_y + logo_height//1.5 

    bbox = draw.multiline_textbbox((lcoation_text_x, lcoation_text_y), final_wrapped_location, font=reduced_font_location, anchor="rd",spacing=5)
    line_height = bbox[3] - bbox[1]
    line_width = int(bbox[2] - bbox[0])

    left, top, right, bottom = reduced_font_location.getbbox("A")
    Atext_height = bottom - top
    Atext_width = right - left
    
    location_height = Atext_width + Atext_width//2
    location_x = (lcoation_text_x - 2*Atext_width - line_width)
    location_y = int(bbox[3] - int(1.5*Atext_height))

    if location:
        ## location text
        draw.text(
            (lcoation_text_x, lcoation_text_y),
            text=final_wrapped_location,
            font=reduced_font_location,
            anchor="rd",
            spacing = 5,
            stroke_width = 1,
            align="right",
        )
        # location logo
        add_logo(
            gradient_image,
            location_image_path,
            location_height,
            location_height,
            position=(location_x, location_y),
        )

    ## arrow
    if arrow == "show":
        arrow_width = (gradient_image.size[0] * 6) // 100
        arrow_height = arrow_width
        arrow_x = logo_x + logo_width//2
        arrow_y = min(logo_y - arrow_height - Atext_height,(gradient_image.size[1] * 50) // 100 - arrow_height//2)
        add_logo(
            gradient_image,
            arrow_image_path,
            arrow_width,
            arrow_height,
            position=(arrow_x, arrow_y),
        )

    gradient_image.save(output_img_path,'PNG')


def web_news_story(text, category, input_img_path, output_img_path, crop_mode):
     
    gradient_image, x_min, x_max, y_min, y_max, reduced_font, final_wrapped_text = template_preprocess(text, input_img_path, crop_mode, font_path, font_size_perc = 7, x_mn_prc=10, x_mx_prc=90, y_mn_prc=75, y_mx_prc=80, mx_height_perc=80)
    gradient_image = gradient_bottom_to_top(gradient_image, darkness=1, gradient_magnitude=1.5)
    
    color = "rgb(255,0,0)"
    draw = ImageDraw.Draw(gradient_image)
    x = (gradient_image.size[0] * 50) // 100
    draw.multiline_text(
        (x, y_max),
        text=final_wrapped_text,
        font=reduced_font,
        anchor="md",
        spacing=25,
        align="center",
        stroke_width=0,
        embedded_color=False,
    )

    ### catagory text 
    bbox = draw.multiline_textbbox((x, y_max), final_wrapped_text, font=reduced_font, anchor="md",spacing=25)

    cat_font_size = (reduced_font.size * 65) //100
    cat_font = ImageFont.truetype(font_path, cat_font_size)
    
    y_cat = bbox[1] - (cat_font_size // 2)
    color = 'rgb(255,255,0)'
    draw.text((x, y_cat), text=category, fill = color, font=cat_font, anchor="md", align='center')

    ### logo
    logo_width = (gradient_image.size[0] * 16) // 100
    logo_height = logo_width
    logo_y = y_cat - (cat_font_size) - logo_height

    add_logo(
        gradient_image,
        logo_image_path,
        logo_width,
        logo_height,
        position=(x - logo_width//2, logo_y),
    )

    ## down arrow
    arrow_width = (gradient_image.size[0] * 8) // 100
    arrow_height = logo_width
    
    arrow_x = x - arrow_width//2
    arrow_y = y_max + (cat_font_size)
    
    add_logo(
        gradient_image,
        down_arrow_image_path,
        arrow_width,
        arrow_height,
        position=(arrow_x, arrow_y),
    )

    gradient_image.save(output_img_path,'PNG')


def feed_headline(text, subtitle, input_img_path, output_img_path, crop_mode, arrow):
     
    gradient_image, x_min, x_max, y_min, y_max, reduced_font, final_wrapped_text = template_preprocess(text, input_img_path, crop_mode, font_path, font_size_perc = 7, x_mn_prc=7, x_mx_prc=70, y_mn_prc=75, y_mx_prc=90, mx_height_perc=65)
    gradient_image = gradient_top_left_to_bottom_right(gradient_image, gradient_magnitude=1.5)

    y = (gradient_image.size[1] * 5) // 100
    
    draw = ImageDraw.Draw(gradient_image)
    
    draw.text(
        (x_min, y),
        text=final_wrapped_text,
        font=reduced_font,
        anchor="la",
        spacing = 25,
        align="left",
    )

    ## subtitle text
    bbox = draw.multiline_textbbox((x_min, y), final_wrapped_text, font=reduced_font, anchor="la",spacing=25)

    _ , x_min_subtitle, x_max_subtitle, y_min_subtitle, y_max_subtitle, reduced_font_subtitle, final_wrapped_subtitle = template_preprocess(subtitle, input_img_path, crop_mode, font_path, font_size_perc = 4, x_mn_prc=10, x_mx_prc=40, y_mn_prc=75, y_mx_prc=95, mx_height_perc=80)
    
    y = bbox[3] + reduced_font_subtitle.size
    color = "rgb(255,255,0)"

    draw.text(
        (x_min, y),
        text=final_wrapped_subtitle,
        font=reduced_font_subtitle,
        fill=color,
        anchor="la",
        spacing = 15,
        align="left",
    )
    
    ### logo
    logo_width = (gradient_image.size[0] * 12) // 100
    logo_y = gradient_image.size[1] - (logo_width+ (logo_width // 2))
    add_logo(
        gradient_image, logo_image_path, logo_width, logo_width, position=(x_min,logo_y)
    )

    # arrow
    if arrow == "show":
        arrow_width = (gradient_image.size[0] * 6) // 100
        arrow_height = logo_width
        arrow_x = (gradient_image.size[0] * 90) // 100
        arrow_y = (gradient_image.size[1] * 50) // 100 - arrow_height//2
    
        add_logo(
            gradient_image,
            arrow_image_path,
            arrow_width,
            arrow_height,
            position=(arrow_x, arrow_y),
        )
    
    gradient_image.save(output_img_path,'PNG')


def quotes_writings_art(text, author, output_img_path, crop_mode):
     
    width, height = 1080, 1080
    black_image = Image.new("RGB", (width, height), "black")
    color = "rgb(255,255,255)"
    # Save the black image to a file
    black_image.save(output_img_path,'PNG')

    gradient_image, x_min, x_max, y_min, y_max, reduced_font, final_wrapped_text = template_preprocess(text, output_img_path, crop_mode, font_path, font_size_perc = 7, x_mn_prc=10, x_mx_prc=90, y_mn_prc=20, y_mx_prc=90, mx_height_perc=65)
    x = (gradient_image.size[0] * 50) // 100
    y = (gradient_image.size[1] * 50) // 100
    
    draw = ImageDraw.Draw(gradient_image)

    ### logo
    logo_width = (gradient_image.size[0] * 60) // 100
    logo_height = (gradient_image.size[0] * 50) // 100
    logo_y = (gradient_image.size[1] * 50) // 100
    logo_x = (gradient_image.size[0] * 50) // 100 - logo_width//2

    logo = Image.open(logo_image_path)
    resized_logo = logo.resize((logo_width, logo_height))
    img = resized_logo.convert("RGBA")
    
    datas = img.getdata()
    newData = []

    for item in datas:
        if item[0] != 0 and item[1] != 0 and item[2] != 0:
            newData.append((item[0], item[1], item[2], 60))
        else:
            newData.append(item)
    img.putdata(newData)

    # # Define the paste position
    paste_position = (logo_x,logo_y - logo_width//2) # Adjust the position where you want to paste the logo
    ## Paste the resized and transparent logo onto the input image
    gradient_image.paste(img, paste_position, img)
    
    draw.text(
        (x, y),
        text=final_wrapped_text,
        font=reduced_font,
        anchor="mm",
        fill= color,
        spacing = 25,
        align="center",
    )
    
    # l,t,r,b
    bbox = draw.multiline_textbbox((x, y), final_wrapped_text,anchor="mm", font=reduced_font,spacing=15)
    text_height = bbox[3] - bbox[1]

    # author
    _, x_min_author, x_max_author, y_min_author, y_max_author, reduced_font_author, final_wrapped_text_author = template_preprocess(author, output_img_path, crop_mode, font_path, font_size_perc = 5, x_mn_prc=10, x_mx_prc=90, y_mn_prc=20, y_mx_prc=90, mx_height_perc=25)
    font_size= reduced_font_author.size
    color = "rgb(255,230,0)"
    
    if len(author) != 0:
        draw.multiline_text(
            (x, y + 2*font_size + text_height//2),
            text=final_wrapped_text_author,
            font=reduced_font_author,
            anchor="ma",
            fill= color,
            spacing = 5,
            align="center",
        )

        ## add line to both sides of author
        bbox = draw.multiline_textbbox((x, y + font_size + text_height//2), final_wrapped_text_author, anchor="ma", font=reduced_font_author, spacing=5)
        text_height_author = bbox[3] - bbox[1]

        line_color =  (255, 255, 0)  # RGB color, here it's yellow
        line_width = 3  # Line width in pixels
        
        left_start_point = (bbox[0] - font_size//2,  y + 2*font_size + text_height//2 + text_height_author//2 + 10)
        left_end_point = (bbox[0] - font_size,  y + 2*font_size + text_height//2 + text_height_author//2 + 10)
        draw.line([left_start_point, left_end_point], fill=line_color, width=line_width)
        right_start_point = (bbox[2] + font_size//2,  y +  2*font_size + text_height//2 + text_height_author//2 + 10)
        right_end_point = (bbox[2] + font_size,  y +  2*font_size + text_height//2 + text_height_author//2 + 10)
        draw.line([right_start_point, right_end_point], fill=line_color, width=line_width)

    # hashed text 
    font_size = (gradient_image.size[0] * 4) // 100
    font = ImageFont.truetype(font_path, font_size)
    draw.text(
        (x, y_max + (font_size)),
        text="#artnëvargje",
        font=font,
        anchor="mm",
        spacing = 5,
        align="left",
    )

    gradient_image.save(output_img_path,'PNG')


def quotes_writings_morning(text, output_img_path, crop_mode):
     
    width, height = 1080, 1080
    black_image = Image.new("RGB", (width, height), "white")
    color = "rgb(0,0,0)"
    # Save the black image to a file
    black_image.save(output_img_path,'PNG')

    gradient_image, x_min, x_max, y_min, y_max, reduced_font, final_wrapped_text = template_preprocess(text, output_img_path, crop_mode, font_path, font_size_perc = 7, x_mn_prc=10, x_mx_prc=90, y_mn_prc=20, y_mx_prc=90, mx_height_perc=50)
    x = (gradient_image.size[0] * 50) // 100
    y = (gradient_image.size[1] * 50) // 100
    
    draw = ImageDraw.Draw(gradient_image)
    
    draw.text(
        (x, y),
        text=final_wrapped_text,
        font=reduced_font,
        anchor="mm",
        fill= color,
        spacing = 25,
        align="center",
    )
    
    # l,t,r,b
    bbox = draw.multiline_textbbox((x, y), final_wrapped_text,anchor="mm", font=reduced_font,spacing=25)
    text_height = bbox[3] - bbox[1]

    # hashed text 
    _, x_min_author, x_max_author, y_min_author, y_max_author, reduced_font_author, final_wrapped_text_author = template_preprocess(text, output_img_path, crop_mode, font_path, font_size_perc = 3, x_mn_prc=20, x_mx_prc=80, y_mn_prc=20, y_mx_prc=90, mx_height_perc=30)
    font_size= reduced_font_author.size
    
    ### logo
    logo_width = (gradient_image.size[0] * 60) // 100
    logo_height = (gradient_image.size[0] * 50) // 100
    logo_y = (gradient_image.size[1] * 50) // 100
    logo_x = (gradient_image.size[0] * 50) // 100 - logo_width//2

    logo = Image.open(logo_image_path)
    resized_logo = logo.resize((logo_width, logo_height))
    img = resized_logo.convert("RGBA")
    
    datas = img.getdata()
    newData = []

    for item in datas:
        if item[0] != 0 and item[1] != 0 and item[2] != 0:
            newData.append((item[0], item[1], item[2], 50))
        else:
            newData.append(item)
    img.putdata(newData)

    # # Define the paste position
    paste_position = (logo_x,logo_y - logo_width//2) # Adjust the position where you want to paste the logo

    # # Paste the resized and transparent logo onto the input image
    gradient_image.paste(img, paste_position, img)
    
    draw.text(
        (x, y_max + font_size),
        text="#morningquote",
        font=reduced_font_author,
        fill=color,
        anchor="mm",
        spacing = 5,
        align="left",
    )

    gradient_image.save(output_img_path,'PNG')


def quotes_writings_thonjeza(text, output_img_path, crop_mode, arrow):
     
    width, height = 1080, 1080
    white_image = Image.new("RGB", (width, height), "white")
    color = "rgb(0,0,0)"
    # Save the image to a file
    white_image.save(output_img_path,'PNG')

    gradient_image, x_min, x_max, y_min, y_max, reduced_font, final_wrapped_text = template_preprocess(text, output_img_path, crop_mode, font_path, font_size_perc = 7, x_mn_prc=10, x_mx_prc=90, y_mn_prc=20, y_mx_prc=90, mx_height_perc=50)
    x = (gradient_image.size[0] * 50) // 100
    y = (gradient_image.size[1] * 50) // 100
    
    draw = ImageDraw.Draw(gradient_image)
    
    draw.text(
        (x, y),
        text=final_wrapped_text,
        font=reduced_font,
        anchor="mm",
        fill= color,
        spacing = 25,
        align="center",
    )

    ### logo
    logo_width = (gradient_image.size[0] * 12) // 100
    px = ((gradient_image.size[0] * 10) //100)
    logo_x= gradient_image.size[0] - px - logo_width
    logo_y = (gradient_image.size[1] * 4) //100

    add_logo(
        gradient_image, logo_image_path, logo_width, logo_width, position = (logo_x,logo_y)
    )

    ### faded arrow
    if arrow == "show":
        arrow_width = (gradient_image.size[0] * 40) // 100
        arrow_height = reduced_font.size
        px_arrow = ((gradient_image.size[0] * 6) //100)
        arrow_x= gradient_image.size[0] - px_arrow - arrow_width
        arrow_y = (gradient_image.size[1] * 90) //100

        add_logo(
            gradient_image, faded_arrow_path, arrow_width, arrow_height, position = (arrow_x,arrow_y)
        )

    gradient_image.save(output_img_path,'PNG')


def quotes_writings_citim(text,sub_text, output_img_path, crop_mode, arrow):
         
    width, height = 1080, 1080
    white_image = Image.new("RGB", (width, height), "white")
    color = "rgb(0,0,0)"
    # Save the black image to a file
    white_image.save(output_img_path,'PNG')

    gradient_image, x_min, x_max, y_min, y_max, reduced_font, final_wrapped_text = template_preprocess(text, output_img_path, crop_mode, font_path, font_size_perc = 7, x_mn_prc=10, x_mx_prc=90, y_mn_prc=20, y_mx_prc=90, mx_height_perc=50)
    x = (gradient_image.size[0] * 50) // 100
    y = (gradient_image.size[1] * 50) // 100
    
    draw = ImageDraw.Draw(gradient_image)
    
    draw.text(
        (x, y),
        text=final_wrapped_text,
        font=reduced_font,
        anchor="mm",
        fill= color,
        spacing = 25,
        align="center",
    )
    
    ### logo
    logo_width = (gradient_image.size[0] * 12) // 100
    px = ((gradient_image.size[0] * 10) //100)
    logo_x= gradient_image.size[0] - px - logo_width
    logo_y = (gradient_image.size[1] * 2) //100

    add_logo(
        gradient_image, logo_image_path, logo_width, logo_width, position = (logo_x,logo_y)
    )
    
    bbox = draw.multiline_textbbox((x, y), final_wrapped_text, font=reduced_font, anchor="mm",spacing=25,align="center")
    line_height = bbox[3] - bbox[1]
    
    ## quote 
    quote_width = (gradient_image.size[1] * 12) // 100
    quote_height = quote_width
    quote_x = x_min + quote_width //4
    quote_y = int(bbox[1] - quote_height - reduced_font.size)
    add_logo(gradient_image, quote_image_path, quote_width, quote_height, position=(quote_x,quote_y))

    ## reverse quote
    quote_width = (gradient_image.size[1] * 12) // 100
    quote_height = quote_width
    quote_x = x_max - int(quote_width *1.5)
    quote_y = int(bbox[3] + reduced_font.size)
    add_logo(gradient_image, reverse_quote_image_path, quote_width, quote_height, position=(quote_x,quote_y))

    ### faded arrow 
    arrow_width = (gradient_image.size[0] * 40) // 100
    arrow_height = reduced_font.size
    px_arrow = ((gradient_image.size[0] * 6) //100)
    arrow_x= gradient_image.size[0] - px_arrow - arrow_width
    arrow_y = (gradient_image.size[1] * 90) //100

    if arrow == "show":
        add_logo(
            gradient_image, faded_arrow_path, arrow_width, arrow_height, position = (arrow_x,arrow_y)
        )

    # sub text 
    if len(sub_text) != 0:
        _, x_min_sub, x_max_sub, y_min_sub, y_max_sub, reduced_font_sub, final_wrapped_text_sub = template_preprocess(sub_text, output_img_path, crop_mode, font_path, font_size_perc = 4, x_mn_prc=11, x_mx_prc=60, y_mn_prc=20, y_mx_prc=90, mx_height_perc=30)
        color = "rgb(255, 227, 0)"
        draw.multiline_text(
            (x_min_sub, arrow_y + arrow_height//1.5),
            text=final_wrapped_text_sub,
            font=reduced_font_sub,
            anchor="ld",
            fill= color,
            spacing = 5,
            align="left",
        )

        bbox = draw.multiline_textbbox((x_min_sub, arrow_y + arrow_height//1.5), final_wrapped_text_sub, font=reduced_font_sub, anchor="ld",spacing=5,align="left")
        line_height = bbox[3] - bbox[1]

        ## left faded line 
        line_width = int((gradient_image.size[0] * 10) // 100)
        line_height = int(reduced_font.size)
        line_x= int(bbox[0] - line_width - reduced_font_sub.size//2)
        line_y =  arrow_y + arrow_height//5

        add_logo(
            gradient_image, faded_line_path, line_width, line_height, position = (line_x,line_y)
        )

    gradient_image.save(output_img_path,'PNG')


def web_news_story_2(text, sub_text, category, input_img_path, output_img_path, crop_mode):

    gradient_image, x_min, x_max, y_min, y_max, reduced_font, final_wrapped_text = template_preprocess(text, input_img_path, crop_mode, font_path, font_size_perc = 7, x_mn_prc=10, x_mx_prc=90, y_mn_prc=75, y_mx_prc=85, mx_height_perc=40)

    image1 = gradient_image
    image2 = Image.open(web_story_2_img_path)

    image1.thumbnail((1080,1920), Image.Resampling.LANCZOS)
    # Resize Image 2 to match the dimensions of Image 1
    image2 = image2.resize((image1.size[0],1920))

    HEIGH_OF_THE_BLACK_AREA = 1920 // 2
    new_im1 = Image.new(image1.mode, size = (image1.size[0], image1.size[1] + HEIGH_OF_THE_BLACK_AREA))
    new_im1.putdata(image1.getdata())

    # Make Image 2 half transparent (adjust the transparency level as needed)
    image2 = image2.convert("RGBA")
    data = image2.getdata()
    new_data = []
    for item in data:
        r, g, b, a = item
        new_data.append((r, g, b, a))  # Reduce the alpha channel to make it half transparent
    image2.putdata(new_data)
    
    paste_x = 0
    paste_y = new_im1.size[1] - image2.size[1]
    # Overlay Image 2 on top of Image 1
    new_im1.paste(image2, (paste_x, paste_y), image2)
    ## resize image
    new_im1.thumbnail((1080,1920), Image.Resampling.LANCZOS)
    
    draw = ImageDraw.Draw(new_im1)
    color = "rgb(255, 255, 255)"

    ## logo
    logo_width = (new_im1.size[0] * 20) // 100
    px = ((new_im1.size[0] * 4) //100)
    logo_x= new_im1.size[0] - px - logo_width
    logo_y = (new_im1.size[1] * 33) // 100

    add_logo(
        new_im1, logo_image_path, logo_width, logo_width, position = (logo_x, logo_y)
    )

    ## text
    text_x = new_im1.size[0] - ((new_im1.size[0] * 2) //100)
    text_y = ((new_im1.size[1] * 50) //100)
    draw.text(
        (text_x, text_y),
        text=final_wrapped_text,
        font=reduced_font,
        anchor="ra",
        fill= color,
        spacing = 30,
        align="right",
        stroke_width = 0
    )

    new_im1.save(output_img_path,'PNG')
    
    bbox = draw.multiline_textbbox((text_x, text_y), final_wrapped_text, font=reduced_font, anchor="ra",spacing=30,align="right")
    
    # cat text
    font_size = (gradient_image.size[0] * 5) // 100
    font = ImageFont.truetype(font_path, font_size)
    draw.text(
        (text_x - ((new_im1.size[0] * 2) //100), bbox[1] - int(1.2 * reduced_font.size)),
        text=category,
        font=font,
        anchor="ra",
        fill= color,
        spacing = 5,
        align="right",
    )


    # sub text 
    _, x_min_sub, x_max_sub, y_min_sub, y_max_sub, reduced_font_sub, final_wrapped_text_sub = template_preprocess(sub_text, output_img_path, crop_mode, font_path, font_size_perc = 6, x_mn_prc=10, x_mx_prc=90, y_mn_prc=75, y_mx_prc=85, mx_height_perc=20)
    
    sub_text_x = new_im1.size[0] - ((new_im1.size[0] * 2) //100)
    sub_text_y = bbox[3] + reduced_font_sub.size
    
    draw.text(
        (sub_text_x, sub_text_y),
        text=final_wrapped_text_sub,
        font=reduced_font_sub,
        anchor="ra",
        fill= color,
        spacing = 20,
        align="right",
    )

    ## double reverse arrow
    bbox_sub = draw.multiline_textbbox((sub_text_x, sub_text_y), final_wrapped_text_sub, font=reduced_font_sub, anchor="ra",spacing=25,align="right")
    arrow_x = new_im1.size[0] - px - logo_width//2
    arrow_y = bbox_sub[3] + reduced_font_sub.size
    logo_width = (new_im1.size[0] * 8) // 100
    logo_height = logo_width
    
    add_logo(
        new_im1,
        reverse_arrow_white_path,
        logo_width,
        logo_height,
        position=(arrow_x, arrow_y),
    )

    # # Save the resulting image
    new_im1.save(output_img_path,'PNG')


def story_2(text, category, input_img_path, output_img_path, crop_mode):

    _, x_min, x_max, y_min, y_max, reduced_font, final_wrapped_text = template_preprocess(text, input_img_path, crop_mode, font_path, font_size_perc = 7, x_mn_prc=5, x_mx_prc=95, y_mn_prc=75, y_mx_prc=85, mx_height_perc=25)
    im = Image.open(input_img_path)
    
    target_size = (1215, 2160)  # New target size
    width, height = im.size
    target_height = height
    target_width = int(target_height * 9 / 16)
    left = (width - target_width) // 2
    top = (height - target_height) // 2
    right = left + target_width
    bottom = top + target_height
    
    cropped_im = im.crop((left, top, right, bottom))
    image1 = cropped_im.resize(target_size)
   
    image2 = Image.open(story2_img_path)


    # Resize Image 2 to match the dimensions of Image 1
    image2 = image2.resize((image1.size[0],image2.size[1] +(image2.size[1]*15)//100))
    
    # HEIGH_OF_THE_BLACK_AREA
    # new_im1 = Image.new(image1.mode, size = (image1.size[0], image1.size[1] + HEIGH_OF_THE_BLACK_AREA))
    # new_im1.putdata(image1.getdata())
    
    new_im1 =image1


    # Make Image 2 half transparent (adjust the transparency level as needed)
    image2 = image2.convert("RGBA")
    data = image2.getdata()
    new_data = []
    for item in data:
        r, g, b, a = item
        new_data.append((r, g, b, a))  # Reduce the alpha channel to make it half transparent
    image2.putdata(new_data)
    
    paste_x = 0
    paste_y = new_im1.size[1] - image2.size[1]
    
    # Overlay Image 2 on top of Image 1
    new_im1.paste(image2, (paste_x, paste_y), image2)
    # resize image
    # new_im1.thumbnail((1080,1920), Image.Resampling.LANCZOS)
    
    draw = ImageDraw.Draw(new_im1)
    color = "rgb(255, 255, 255)"

    ## logo
    logo_width = (new_im1.size[0] * 16) // 100
    px = ((new_im1.size[0] * 7) //100)
    logo_x= new_im1.size[0] - px - logo_width + 10
    logo_y = image2.size[1] - logo_width - reduced_font.size//2
    
    add_logo(
        new_im1, logo_image_path, logo_width, logo_width, position = (logo_x, logo_y)
    )

    # cat text
    font_size = (new_im1.size[0] * 4) // 100
    font = ImageFont.truetype(font_path, font_size)
    # cat_x = new_im1.size[0] - ((new_im1.size[0] * 5) //100)
    cat_x = new_im1.size[0] - px
    cat_y = logo_y + logo_width + int(font.size//3)

    draw.text(
        (cat_x, cat_y),
        text=category,
        font=font,
        anchor="ra",
        fill= color,
        spacing = 5,
        align="right",
    )

    ## text
    bbox = draw.multiline_textbbox((cat_x, cat_y), category, font=font, anchor="ra",spacing=5,align="right")
    
    text_x = cat_x + 20
    text_y = cat_y + font.size + reduced_font.size
    draw.text(
        (text_x, text_y),
        text=final_wrapped_text,
        font=reduced_font,
        anchor="ra",
        fill= color,
        spacing = 25,
        align="right",
        stroke_width = 1
    )

    ## double reverse arrow
    bbox_sub = draw.multiline_textbbox((text_x, text_y), final_wrapped_text, font=reduced_font, anchor="ra",spacing=25,align="right")
    arrow_x = new_im1.size[0] - px - logo_width//2
    arrow_y = bbox_sub[3] + reduced_font.size
    logo_width = (new_im1.size[0] * 8) // 100
    logo_height = logo_width
    
    add_logo(
        new_im1,
        reverse_arrow_white_path,
        logo_width,
        logo_height,
        position=(arrow_x, arrow_y),
    )

    # # Save the resulting image
    new_im1.save(output_img_path,'PNG')
