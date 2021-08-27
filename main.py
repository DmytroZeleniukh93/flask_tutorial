from flask import Flask, render_template

app = Flask(__name__)

menu = ['One', 'Two', 'Three']


@app.route('/')
def index():
    return render_template('index.html', title='Головна сторінка', menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', title='Про сайт', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
