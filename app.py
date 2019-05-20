import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
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

            os.rename(file_path, os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("--- %s seconds ---" % str (time.time() - start_time))
            return render_template('template.html', label='', imagesource='../uploads/' + filename)



if __name__ == '__main__':
    app.run()
