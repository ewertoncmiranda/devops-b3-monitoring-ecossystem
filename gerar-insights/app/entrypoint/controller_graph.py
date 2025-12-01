from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)
CHART_DIR = "/app/output_charts"

@app.route("/")
def index():
    files = os.listdir(CHART_DIR)
    html = """
    <h1>Dashboard - Insights</h1>
    {% for f in files %}
        <div style="margin-bottom:30px">
            <h3>{{ f }}</h3>
            <img src="/chart/{{ f }}" width="600">
        </div>
    {% endfor %}
    """
    return render_template_string(html, files=files)

@app.route("/chart/<path:filename>")
def get_chart(filename):
    return send_from_directory(CHART_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
