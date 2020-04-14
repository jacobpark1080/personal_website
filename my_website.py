from flask import Flask, render_template, url_for, request, Response
import os
from db import helper
import json

app = Flask(__name__)

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
        "projects_page.html",data=all_items["items"]
    )

@app.route('/item/new', methods=['POST'])
def add_item():
    item = request.form['item']
    status = request.form['status']
    
    # Add item to the list
    res_data = helper.add_to_list(item,status)

    # Return error if item not added
    if res_data is None:
        response = Response("{'error': 'Item not added - " + item + "'}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    return projects()

@app.route('/items/all')
def get_all_items():
    # Get items from the helper
    res_data = helper.get_all_items()

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    return json.loads(json.dumps(res_data))#response

@app.route('/item/status', methods=['GET'])
def get_item():
    # Get parameter from the URL
    item_name = request.args.get('name')

    # Get items from the helper
    status = helper.get_item(item_name)

    # Return 404 if item not found
    if status is None:
        response = Response("{'error': 'Item Not Found - %s'}"  % item_name, status=404 , mimetype='application/json')
        return response

    # Return status
    res_data = {
        'status': status
    }

    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    return response

@app.route('/item/update', methods=['PUT'])
def update_status():
    # Get item from the POST body
    req_data = request.get_json()
    item = req_data['item']
    status = req_data['status']

    # Update item in the list
    res_data = helper.update_status(item, status)

    # Return error if the status could not be updated
    if res_data is None:
        response = Response("{'error': 'Error updating item - '" + item + ", " + status   +  "}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response

@app.route('/item/remove', methods=['DELETE'])
def delete_item():
    # Get item from the POST body
    req_data = request.get_json()
    item = req_data['item']

    # Delete item from the list
    res_data = helper.delete_item(item)

    # Return error if the item could not be deleted
    if res_data is None:
        response = Response("{'error': 'Error deleting item - '" + item +  "}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response

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
