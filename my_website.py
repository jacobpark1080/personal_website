from flask import Flask, render_template, url_for
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template(
        "home_page.html"
    )

@app.route('/test')
def testing():
    return 'Test Page'

@app.route('/test/<name>')
def name_html(name):
    html = '<h1>This is ' + name.title() + "'s Website!</h1>"
    html += '\n' + '<h2>:P</h2>'
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0')
