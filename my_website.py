from flask import Flask, render_template, url_for, request, Response, redirect, jsonify
import os
from db import helper
from db.helper import books
import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template(
        "home_page.html"
    )

@app.route('/api', methods=['GET'])
def apihome():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    results = helper.api_all()
    return jsonify(results)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    if not (id or published or author):
        return page_not_found(404)
        
    results = helper.api_filter(id,published,author)

    return jsonify(results)


@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in helper.books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)



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
    try:
        message = request.args['message']
    except:
        message = None
    all_items = get_all_items()
    return render_template(
        "projects_page.html",err=message,data=all_items["items"]
    )

@app.route('/item/new', methods=['POST'])
def add_item():
    error = None
    item = request.form['item']
    status = request.form['status']
    res_data = helper.add_to_list(item,status)
    if res_data is None:
        return redirect(url_for('projects',message='add_error'))
    response = Response(json.dumps(res_data), mimetype='application/json')
    return redirect(url_for('projects'))

@app.route('/item/update', methods=['POST'])
def update_status():
    item = request.form['item']
    status = request.form['status']
    res_data = helper.update_status(item, status)
    if res_data is None:
        return redirect(url_for('projects',message='update_error'))
    response = Response(json.dumps(res_data), mimetype='application/json')
    print(response)
    return redirect(url_for('projects'))

@app.route('/item/remove', methods=['POST'])
def delete_item():
    item = request.form['item']
    res_data = helper.delete_item(item)
    if res_data is None:
        return redirect(url_for('projects',message='delete_error'))
    response = Response(json.dumps(res_data), mimetype='application/json')
    return redirect(url_for('projects'))

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

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

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
