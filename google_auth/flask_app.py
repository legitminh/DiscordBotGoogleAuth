from flask import Flask, session, abort, redirect, request, render_template_string
from google_auth_oauthlib.flow import Flow
import os
import pathlib
import google.auth.transport.requests
import cachecontrol
from google.oauth2 import id_token
import requests
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import jsonDatabase
from const import const
import time

app = Flask("Google Login App")
app.secret_key = "CatchbackYay"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Enable HTTP for OAuth (not recommended for production) TODO: CHANGE THIS FOR PROD


client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
DB_FILE = os.path.join(pathlib.Path(__file__).parent.parent,"nonce","link_token_to_userId.json")
database = jsonDatabase.createDatabase(DB_FILE)
database(jsonDatabase.write, {})
# The user need to input their code back into the discord so malicious users can't make another one authenticate for them
DB_CODE_TO_USER = os.path.join(pathlib.Path(__file__).parent, "code_to_user.json")
databaseCodeToUser = jsonDatabase.createDatabase(DB_CODE_TO_USER) 
databaseCodeToUser(jsonDatabase.write, {})

stateData = {} #state -> nonce

flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:5000/callback")

GOOGLE_CLIENT_ID = jsonDatabase.read(client_secrets_file)["web"]["client_id"]

def login_is_required(f):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return f()
    return wrapper

@app.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    nonce = request.args.get("nonce")
    dict = database(jsonDatabase.read)
    print(nonce, dict)
    if nonce not in dict:
        return f"ERROR, INVALID NONCE"
    session["state"] = state  # Simulate a login
    stateData[state] = nonce

    return redirect(authorization_url)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)
    reply_state = request.args["state"]
    if not session["state"] == reply_state:
        abort(500)  # State does not match! Protect cross site attacks
    if reply_state not in stateData:
        return "ERROR, INVALID NONCE"
    
    
    dict = database(jsonDatabase.read)
    nonce = stateData[reply_state]
    if time.time() - dict[nonce]["createdTime"] > const.NONCE_EXPIRATION:
        return "ERROR, EXPIRED NONCE"
    

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    from nonce.nonce_manager import generate_nonce
    secretCode = generate_nonce()
    databaseCodeToUser(jsonDatabase.set, secretCode, {"id": dict[nonce]["id"], "googleId": id_info.get("sub")})

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Copy Secret Code</title>
    </head>
    <body style="font-family:sans-serif; margin:50px;">
        <h2>Your Secret Code</h2>
        <p><span id="secret-code">{{ code }}</span></p>
        <button onclick="copyCode()">Copy Code</button>
        <p id="status"></p>

        <script>
        function copyCode() {
            const code = document.getElementById("secret-code").innerText;
            navigator.clipboard.writeText(code).then(() => {
                document.getElementById("status").innerText = "✅ Code copied!";
            }).catch(err => {
                document.getElementById("status").innerText = "❌ Failed to copy";
                console.error(err);
            });
        }
        </script>
    </body>
    </html>
    """, code=secretCode)
    # return redirect('/protected_area')

    

@app.route('/')
def index():
    return "Hello world <a href='/login'><button>Login</button></a>"

@app.route('/protected_area')
@login_is_required
def protected_area():
    return "Protected area <a href='/logout'><button>Logout</button></a>" 

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)