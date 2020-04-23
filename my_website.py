from flask import Flask, render_template, url_for, request, Response, redirect
import os
from db import helper
import json

app = Flask(__name__)
error = None

@app.route('/')
def home():
    return render_template(
        "home_page.html"
    )

@app.route('/photos')
def photos():
    return render_template(
        "photo_page.html"
    )

@app.route('/blog')
def blog():
    return render_template(
        "blog_page.html"
    )

@app.route('/projects')
def projects():
    all_items = get_all_items()
    print(all_items["items"])
    return render_template(
        "projects_page.html",err='error',data=all_items["items"]
    )

@app.route('/item/new', methods=['POST'])
def add_item():
    item = request.form['item']
    status = request.form['status']
    res_data = helper.add_to_list(item,status)
    if res_data is None:
        response = Response("{'error': 'Item not added - " + item + "'}", status=400 , mimetype='application/json')
        return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    return projects()

@app.route('/items/all')
def get_all_items():
    res_data = helper.get_all_items()
    response = Response(json.dumps(res_data), mimetype='application/json')
    return json.loads(json.dumps(res_data))

@app.route('/item/status', methods=['GET'])
def get_item():
    item_name = request.args.get('name')
    status = helper.get_item(item_name)
    if status is None:
        response = Response("{'error': 'Item Not Found - %s'}"  % item_name, status=404 , mimetype='application/json')
        return response
    res_data = {
        'status': status
    }
    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    return response

@app.route('/item/update', methods=['POST'])
def update_status():
    error = None
    item = request.form['item']
    status = request.form['status']
    res_data = helper.update_status(item, status)
    if res_data is None:
        error = 'update_error'
        response = Response("{'error': 'Error updating item - '" + item + ", " + status   +  "}", status=400 , mimetype='application/json')
        return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    return projects()

@app.route('/item/remove', methods=['POST'])
def delete_item():
    error = None
    item = request.form['item']
    res_data = helper.delete_item(item)
    if res_data is None:
        error = 'delete_error'
        response = Response("{'error': 'Error deleting item - '" + item +  "}", status=400 , mimetype='application/json')
        return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    return redirect(url_for('projects'))

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
