# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask, render_template, request, redirect, url_for, jsonify
from google.cloud import storage
from werkzeug.utils import secure_filename
import json
import requests
import os
import os.path

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'YOURGOOGLECREDENTIALS.json'

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

@app.route('/implicit')
def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    return "success"


@app.route("/imagesubmit", methods=['GET', 'POST'])
def imagesubmit():
    if request.form.get('submit') == 'submit':
        f = request.files['image']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        storage_client = storage.Client()
        bucket = storage_client.bucket("ruhack2020")
        blob = bucket.blob("userupload.jpg")

        blob.upload_from_filename('yogurt.jpg')

        payload = {
                    "requests": [
                    {
                        "image": {
                        "source": {
                            "gcsImageUri": "gs://ruhack2020/userupload.jpg"
                        }
                        },
                        "features": [
                        {
                            "maxResults": 5,
                            "type": "LABEL_DETECTION"
                        }
                        ]
                    }
                    ]
                }

        r = requests.post("https://vision.googleapis.com/v1/images:annotate?key=YOURGOOGLEAPIKEY", json=payload)
        b = r.json()

        for i in b["responses"]:
            ingredients = "&ingredients=" + i["labelAnnotations"][4]["description"]
            apiRequest = "https://api.spoonacular.com/recipes/findByIngredients?apiKey=YOURAPIKEY"
            strings = apiRequest + ingredients + "&number=5"
        c = requests.get(strings)
        a = c.json()
        return render_template('results.html', data=a)
    return render_template('upload.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_blob():
    if request.method == 'POST':
        """Uploads a file to the bucket."""
        #bucket_name = "ruhack2020"
        #source_file_name = "templates\table.jpg"
        #destination_blob_name = "table"

        storage_client = storage.Client()
        bucket = storage_client.bucket("ruhack2020")
        blob = bucket.blob("userupload.jpg")

        blob.upload_from_filename('yogurt.jpg')

        payload = {
                    "requests": [
                    {
                        "image": {
                        "source": {
                            "gcsImageUri": "gs://ruhack2020/userupload.jpg"
                        }
                        },
                        "features": [
                        {
                            "maxResults": 5,
                            "type": "LABEL_DETECTION"
                        }
                        ]
                    }
                    ]
                }

        r = requests.post("https://vision.googleapis.com/v1/images:annotate?key=YOURGOOGLEAPIKEY", json=payload)
        b = r.json()

        for i in b:
            ingredients = i["labelAnnotations"][3]["description"]
            apiRequest = "https://api.spoonacular.com/recipes/findByIngredients?apiKey=YOURAPIKEY"
            strings = apiRequest + ingredients + "5"
            c = requests.get(strings)
            a = c.json()
            return a
    return render_template("upload.html")

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return render_template('home.html')

@app.route('/faq')
def faq():
	return render_template('about.html')

@app.route('/searchbyingredients', methods=['GET', 'POST'])
def searchByIngredients():
    """Return a friendly HTTP greeting."""
    if request.method == 'POST':
        ingredients = "&ingredients=" + request.form['ingredients']
        apiRequest = "https://api.spoonacular.com/recipes/findByIngredients?apiKey=YOURAPIKEY"
        number = "&number=" + request.form['amount']
        strings = apiRequest + ingredients + number
        r = requests.get(strings)
        b = r.json()
        #name = b["title"]
        #artistName = artistName.replace(' ', '-').lower()
        return render_template("results.html", data = b)
    return render_template("search.html")


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
