from flask import Flask, request, url_for, redirect, render_template, make_response, send_file
import pandas as pd 
import pickle
from flask_cors import CORS
from werkzeug.utils import secure_filename

from io import BytesIO
import zipfile

from encryption_class import Encrypted_file
from decryption_class import Decrypted_file

app = Flask(__name__)
CORS(app)

@app.route('/')
def use_template():
    return render_template("index.html")


@app.route('/encrypt_file', methods=['POST','GET'])
def encrypt_file():
    
    if request.method == "POST":

        file_ = request.files["file"]

        #if file_ and allowed_file(file_.filename):
            # Tab

        filename = secure_filename(file_.filename)
        new_filename = filename.split(".")[0]

        #process here the file encyption with file_ and key_
        encrypt_object = Encrypted_file(file_)
        encrypt_object.write_key()
        encrypt_object.encrypt()

        #if unique file then send resp otherwise compress in zip file all files

        #resp_file = make_response(encrypt_object.encrypted_file)
        #resp_file.headers["Content-Disposition"] = f"attachment; filename={new_filename}_encrypted.py_encrypted"
        #resp_file.headers["Content-Type"] = "text/py_encrypted"

        #resp_key = make_response(encrypt_object.key)
        #resp_key.headers["Content-Disposition"] = f"attachment; filename={new_filename}_encrypted.key"
        #resp_key.headers["Content-Type"] = "text/key"
        
        stream = BytesIO()
        with zipfile.ZipFile(stream, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('file_encrypted.text', encrypt_object.encrypted_file)
            zf.writestr('key.text', encrypt_object.key)
        stream.seek(0)

        return send_file(
            stream,
            as_attachment=True,
            download_name='archive.zip'
        )

    return render_template("encrypt.html", msg="Please Choose a file to be encrypted")

@app.route('/decrypt_file', methods=['POST','GET'])
def decrypt_file():
    if request.method == 'POST':
        files = request.files.getlist("file_name")
        filenames = []
        for file_ in files: filenames.append(secure_filename(file_.filename))

        if (len(filenames) == 1 or len(filenames)>2):
            return render_template("decrypt.html", msg="Please make sure you upload 2 files - Select both by pressing Ctrl+click on each file")

        if ("key.text" not in filenames and len([s for s in filenames if '_encrypted' in s])!=1):
            return render_template("decrypt.html", msg="Please make sure you upload both: encrypted model and key text files")
        
        if ("key.text" in filenames and len([s for s in filenames if '_encrypted' in s])!=1):
            return render_template("decrypt.html", msg="Please make sure you upload encrypted text model file too")

        if ("key.text" not in filenames and len([s for s in filenames if '_encrypted' in s])==1):
            return render_template("decrypt.html", msg="Please make sure you upload key text file too")

        for file_ in files:
            print(secure_filename(file_.filename))

        files_local = files.copy()
        key_file = files_local.pop(filenames.index('key.text')).read()
        model_file = files_local[0].read()

        #decrypt_object = Decrypted_file()

        from cryptography.fernet import Fernet
        f = Fernet(key_file)
        decrypted_data = f.decrypt(model_file)

        resp = make_response(decrypted_data)
        resp.headers["Content-Disposition"] = f"attachment; filename=file_decrypted.text"
        resp.headers["Content-Type"] = "text/plain"

        return resp
        #return render_template("test.html",msg="Files has been uploaded successfully", filename=resp)

    return render_template("decrypt.html", msg="Please Choose encrypted file and key file")


if  __name__ == '__main__':
    app.run(debug = True)
