from flask import Flask, request
from decouple import config
from utils.amazons3utils import upload_to_s3_bucket, create_presigned_url
from werkzeug.utils import secure_filename
app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_to_cdn():
    if 'file' not in request.files:
        return {"msg": "No file is present to upload."}, 422
    file = request.files['file']
    file.save(secure_filename(file.filename))
    upload_to_s3_bucket(secure_filename(file.filename))

    return {"msg": "File uploaded successfully."}


@app.route('/get_signed_url', methods=['GET'])
def get_signed_url():
    if 'file_name' not in request.args:
        return {"msg": "File name is not present."}, 422
    file_name = request.args.get('file_name')
    expiry = 3600
    if 'expiry' in request.args:
        expiry = int(request.args.get('expiry'))

    return {"signed_url": create_presigned_url(file_name, expiration=expiry)}


if __name__ == "__main__":
    app.secret_key = config('SECRET_KEY')
    app.run(debug=True)