from flask import Flask, request, redirect, render_template_string, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

users = {}

@app.route("/")
def home():
    if "user" in session:
        return f"Welcome {session['user']}! <a href='/logout'>Logout</a>"
    return "<a href='/register'>Register</a> | <a href='/login'>Login</a>"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        users[username] = password
        return redirect("/login")
    return render_template_string("<form method='post'>Username:<input name='username'>Password:<input name='password' type='password'><button>Register</button></form>")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and check_password_hash(users[username], password):
            session["user"] = username
            return redirect("/")
        return "Invalid credentials"
    return render_template_string("<form method='post'>Username:<input name='username'>Password:<input name='password' type='password'><button>Login</button></form>")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)
