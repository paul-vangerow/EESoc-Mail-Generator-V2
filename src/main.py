import webbrowser
from email_content import email_content
from flask import Flask, request, make_response
import os
import signal

app: Flask = Flask(__name__)
current_email: email_content = email_content()

def main():

    webbrowser.open_new('http://localhost:2000/')
    app.run(host="localhost", port=2000) # Blocking

# Primary page to load

@app.route("/")
def main_page():
    return open_page("interface/main.html")

@app.route("/fetch/<item>", methods = ['GET'] )
def fetch_page(item: str):
    resp = make_response( open_page('gen/'+item) )
    resp.set_cookie('cookie1', 'value1', samesite='Lax')
    resp.set_cookie('cookie2', 'value2', samesite='None', secure=True)
    return resp

@app.route("/send", methods = ['POST'])
def send_email():
    resp = make_response('OK')
    current_email.update_parameters()
    current_email.send_email()
    return resp

@app.route("/update", methods = ['POST'])
def update_pars():
    with open(os.path.abspath("gen/gen.yaml"), "w") as file:
        if file.write(request.data.decode()):
            file.close()
            current_email.update_parameters()
            resp = make_response('OK')
        else:
            resp = make_response('ERROR')
    return resp

@app.route("/data/<file>", methods = ['GET'])
def get_file(file: str):
    cont: str
    with open(os.path.abspath('interface/'+file), 'r') as f:
        cont = f.read()
    return cont

# When application is closed, kill the server.

@app.route("/close", methods = ['POST'] )
def close_app():
    os.kill(os.getpid(), signal.SIGINT)
    return 'KILL'

def open_page(file_path: str):

    # Used to load HTML files from the interface folder (Or any folder really)

    file_content = ""

    with open(os.path.abspath(file_path), "r" ) as stream:
        file_content = stream.read()

    return file_content
    
if __name__ == '__main__':
    main()