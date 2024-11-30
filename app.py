from flask import Flask, render_template, request, make_response
import enscryption_helper as crypt  # Make sure the module name is correct
# Remove waitress import

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/encrypt", methods=['POST'])
def encrypt():
    f = request.files['file']
    passphrase = request.form['passphrase'].encode()
    c = crypt.encrypt(f.read(), passphrase)
    response = make_response(c)
    response.headers.set('Content-Type', 'application/octet-stream')
    response.headers.set('Content-Disposition', 'attachment', filename=f.filename)
    return response

@app.route("/decrypt", methods=['POST'])
def decrypt():
    f = request.files['file']
    passphrase = request.form['passphrase'].encode()
    c = crypt.decrypt(f.read(), passphrase)
    if c:
        response = make_response(c)
        response.headers.set('Content-Type', 'application/octet-stream')
        response.headers.set('Content-Disposition', 'attachment', filename=f.filename)
        return response
    return "Invalid request"

if __name__ == "__main__":
    # Do not use waitress.serve here, as Gunicorn will handle it.
    app.run()
