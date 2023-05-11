import os
from flask import Flask, jsonify, request, url_for, render_template
import FinalBeamDesign
from flask_cors import CORS
import io
from base64 import encodebytes
from PIL import Image

app = Flask(__name__)

app.config['DEBUG'] = True

def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img

@app.route('/data', methods = ['POST'])
def getData():
    data = request.json
    beam_length = data["beam_length"]
    dead_load = data["dead_load"]
    live_load = data["live_load"]
    h = data["h"]
    b = data["b"]
    fprimec = data["fprimec"]
    fy = data["fy"]

    figureName = FinalBeamDesign.beamDesign(beam_length,dead_load,live_load,h,b,fprimec,fy)
    print(figureName)

    encoded_img1 = get_response_image(figureName[0] + ".png")
    encoded_img2 = get_response_image(figureName[1] + ".png")
    encoded_img3 = get_response_image(figureName[2] + ".png")
    os.remove(figureName[0] + ".png")
    os.remove(figureName[1] + ".png")
    os.remove(figureName[2] + ".png")
    return jsonify({
         "image1": encoded_img1,
         "image2": encoded_img2,
         "image3": encoded_img3,
        "dataFrame":figureName[3]
    })


@app.route('/')
def index():
	return render_template('home.html')

if __name__ == '__main__':
    app.run()