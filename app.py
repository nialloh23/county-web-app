from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def template_test():
    return render_template('template.html', label='', imagesource='../uploads/template.jpg')


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run()
