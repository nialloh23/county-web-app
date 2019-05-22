import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
from flask import send_from_directory
import json
import requests
import cv2
from PIL import Image
import sys
import base64
import boto3


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create an S3 client
s3 = boto3.client('s3')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def template_test():
    return render_template('template.html', label='', imagesource='../uploads/template.jpg')



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        import time
        start_time = time.time()
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            s3_bucket_name = 'countyclassifier'
            s3.upload_file(filename, s3_bucket_name, filename)

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            address='https://rhnuvxmfmk.execute-api.us-west-2.amazonaws.com/dev'
            url = address + '/v1/predict'
            content_type = 'application/json'
            headers = {'Content-Type': content_type}

            image = open(file_path, "rb")
            image_read = image.read()  #open binary file in read mode
            image_64_encode = base64.b64encode(image_read) #encode the string in base64-encoded data

            payload= {"image": "data:image/jpg;base64,{}".format(image_64_encode)}

            #img = open('uploads/13.jpg', 'rb').read()
            #img = cv2.imread('uploads/13.jpg')
            #encode image as jpeg
            #_, img_encoded = cv2.imencode('.jpg', img)
            # send http request with image and receive response

            response = requests.post(url, headers=headers, data=json.dumps(payload) )

            json_response = response.json()

            # decode response
            #print (json.loads(response.text))


            #payload = {"image": "data:image/jpg;base64,'$(base64 -w0 -i uploads/31.jpg)'"}
            #result = client.invoke(FunctionName=conf.lambda_function_name,
            #                    InvocationType='RequestResponse',
            #                    LogType='Tail',
            #                    Payload=json.dumps(payload))
            #print('result:{}'.format(result))
            #range = result['Payload'].read()
            #print('range:{}'.format(range))
            #api_response = json.loads(range)
            #print('api_response:{}'.format(api_response))
        #    result = predict(file_path)
        #    if result == 0:
        #        label = 'Daisy'
        #    elif result == 1:
        #        label = 'Rose'
        #    elif result == 2:
        #        label = 'Sunflowers'
        #    print(result)
        #    print(file_path)
        #    filename = my_random_string(6) + filename

            #os.rename(file_path, os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("--- %s seconds ---" % str (time.time() - start_time))
            return render_template('template.html', label=json_response, imagesource='../uploads/' + filename)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.debug=True
    app.run()
