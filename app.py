import os
import requests
from flask import Flask, request, jsonify, send_file
from templates import *
from scraper import scrape_artical
from io import BytesIO

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate_image():
    # try:
        
        artical_url = request.form.get("artical_url",None)

        output_img_path = request.form.get("output_img_path")
        template_type = request.form.get("template_type", "sample")
        crop_mode = request.form.get("crop_mode", "square")

        if template_type in ["quotes_writings_art", "quotes_writings_morning", "quotes_writings_citim", "quotes_writings_thonjeza"]:
            text = request.form.get("text","")
            if template_type == "quotes_writings_art":
                author = request.form.get("sub_text","")
                quotes_writings_art(text, author, output_img_path, crop_mode)
                
            elif template_type == "quotes_writings_morning":
                quotes_writings_morning(text, output_img_path, crop_mode)

            elif template_type == "quotes_writings_thonjeza":
                arrow = request.form.get("arrow","")
                quotes_writings_thonjeza(text, output_img_path, crop_mode, arrow)

            elif template_type == "quotes_writings_citim":
                sub_text = request.form.get("sub_text","").upper()
                arrow = request.form.get("arrow")
                quotes_writings_citim(text,sub_text, output_img_path, crop_mode, arrow)

        else:
            title = ""
            input_img_path_url = None
            if artical_url:
                title, img_url = scrape_artical(artical_url)
                if title == None or img_url == None:
                    response = {"error": "can not scrape given URL"}
                    return jsonify(response), 500
                
                response = requests.get(img_url)
                input_img_path_url = BytesIO(response.content)

            text = request.form.get("text",title)
            input_img_path = request.form.get("input_img_path",input_img_path_url)

            if template_type == "feed_basic":
                arrow = request.form.get("arrow")
                feed_basic(text, input_img_path, output_img_path, crop_mode, arrow)

            elif template_type == "feed_swipe":
                arrow = request.form.get("arrow")
                feed_swipe(text, input_img_path, output_img_path, crop_mode, arrow)

            elif template_type == "highlight":
                text_to_hl = request.form.get('text_to_hl', "")
                arrow = request.form.get("arrow")
                highlight_template(text, input_img_path, output_img_path, crop_mode, arrow, text_to_hl)

            elif template_type == "logo_only":
                logo_position = int(request.form.get("logo_position"))
                logo_only(input_img_path, output_img_path, crop_mode, logo_position)

            elif template_type == "web_news":
                sub_text = request.form.get("sub_text","LAJME").upper()
                sub_text="LAJME" if len(sub_text)==0 else sub_text

                text_to_hl = request.form.get("text_to_hl", "")
                arrow = request.form.get("arrow")
                web_news(text, sub_text, text_to_hl, input_img_path, output_img_path, crop_mode, arrow)

            elif template_type == "citim":
                author = request.form.get("sub_text")
                sub_text = author.upper()
                citim(text, sub_text, input_img_path, output_img_path, crop_mode)

            elif template_type == "iconic_location":
                iconic_location(text, input_img_path, output_img_path, crop_mode)

            elif template_type == "feed_location":
                location = request.form.get("location", "")
                arrow = request.form.get("arrow")
                feed_location(text, input_img_path, output_img_path, crop_mode, location, arrow)

            elif template_type == "web_news_story":
                cat = request.form.get("sub_text","LAJME")
                category = cat.upper()
                web_news_story(text, category, input_img_path, output_img_path, crop_mode)
            
            elif template_type == "feed_headline":
                sub_text = request.form.get("sub_text")
                arrow = request.form.get("arrow")
                feed_headline(text, sub_text, input_img_path, output_img_path, crop_mode, arrow)

            elif template_type == "web_news_story_2":
                sub_text = request.form.get("sub_text","")
                category = request.form.get("category","LAJME").upper()
                category="LAJME" if len(category)==0 else category
                crop_mode = "square"
                web_news_story_2(text,sub_text, category, input_img_path, output_img_path, crop_mode)

            elif template_type == "story_2":
                category = request.form.get("sub_text","LAJME").upper()
                category="LAJME" if len(category)==0 else category
                crop_mode = "story"
                story_2(text, category, input_img_path, output_img_path, crop_mode)

##########################################---- ReformA ----##########################################
            elif template_type == "feed_1":
                category = request.form.get("sub_text","LAJME").upper()
                category="LAJME" if len(category)==0 else category
                crop_mode = "portrait"
                feed_1(text, category, input_img_path, output_img_path, crop_mode)

            elif template_type == "feed_2":
                category = request.form.get("sub_text","LAJME").upper()
                category="LAJME" if len(category)==0 else category
                crop_mode = "portrait"
                feed_2(text, category, input_img_path, output_img_path, crop_mode)

            elif template_type == "citim_reforma":
                author = request.form.get("sub_text")
                sub_text = author.upper()
                citim_reforma(text, sub_text, input_img_path, output_img_path, crop_mode)

            elif template_type == "feed_location_reforma":
                location = request.form.get("location", "")
                arrow = request.form.get("arrow")
                feed_location_reforma(text, input_img_path, output_img_path, crop_mode, location, arrow)

            elif template_type == "logo_only_reforma":
                logo_position = int(request.form.get("logo_position"))
                logo_only_reforma(input_img_path, output_img_path, crop_mode, logo_position)

            elif template_type == "feed_swipe_reforma":
                arrow = request.form.get("arrow")
                feed_swipe_reforma(text, input_img_path, output_img_path, crop_mode, arrow)

            else:
                response = {"Invalid Template": template_type}
                return jsonify(response)


        # Return the filename of the generated image as a response
        response = {"output_file_path": output_img_path}
        return jsonify(response), 200

    # except Exception as e:
    #     response = {"error": str(e)}
    #     return jsonify(response), 500

if __name__ == "__main__":
    app.run(debug=True)
