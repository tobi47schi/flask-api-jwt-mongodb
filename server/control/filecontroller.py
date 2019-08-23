import os
from flask import request, jsonify
from werkzeug import secure_filename

def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      filename = secure_filename(f.filename)
      filepath = os.path.join('uploads', filename)
      f.save(filepath)
      return jsonify(filepath = filepath)

