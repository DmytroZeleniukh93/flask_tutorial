from flask import Flask, render_template, url_for, request

app = Flask(__name__)

menu = [{'name': 'Головна сторінка', 'url': 'index'},
        {'name': 'Про сайт', 'url': 'about'},
        {'name': 'Контакти', 'url': 'contact'}]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Головна сторінка', menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', title='Про сайт', menu=menu)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        print(request.form)
    return render_template('contact.html', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
