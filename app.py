from __future__ import annotations

from pathlib import Path

from flask import Flask, render_template, request, send_from_directory

from file_hasher import hash_file
from ip_lookup import get_ip_info
from password_generator import generate_password
from ping_sweeper import ping_host

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = Path("uploads")
app.config["UPLOAD_FOLDER"].mkdir(exist_ok=True)


@app.route("/image/<path:filename>")
def serve_image(filename):
    return send_from_directory("image", filename)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/generate-password", methods=["POST"])
def generate_password_route():
    length = request.form.get("length", "12")
    try:
        password_length = max(4, min(128, int(length)))
    except ValueError:
        password_length = 12

    password = generate_password(password_length)
    return render_template("index.html", password=password, section="password")


@app.route("/lookup-ip", methods=["POST"])
def lookup_ip_route():
    ip_address = request.form.get("ip_address", "").strip()
    if not ip_address:
        return render_template("index.html", error="Please enter an IP address.", section="ip")

    try:
        ip_data = get_ip_info(ip_address)
    except Exception as exc:  # pragma: no cover - network-dependent path
        return render_template("index.html", error=f"Lookup failed: {exc}", section="ip")

    return render_template("index.html", ip_data=ip_data, section="ip")


@app.route("/hash-file", methods=["POST"])
def hash_file_route():
    uploaded_file = request.files.get("file")
    if uploaded_file is None or uploaded_file.filename == "":
        return render_template("index.html", error="Please choose a file to hash.", section="hash")

    upload_path = app.config["UPLOAD_FOLDER"] / uploaded_file.filename
    uploaded_file.save(upload_path)
    try:
        digest = hash_file(str(upload_path))
    finally:
        if upload_path.exists():
            upload_path.unlink()

    return render_template("index.html", file_digest=digest, filename=uploaded_file.filename, section="hash")


@app.route("/ping-sweep", methods=["POST"])
def ping_sweep_route():
    base_ip = request.form.get("base_ip", "").strip()
    if not base_ip:
        return render_template("index.html", error="Please enter a base IP such as 192.168.1.", section="ping")

    try:
        base_ip = base_ip.rstrip(".")
        if base_ip.count(".") == 3:
            addresses = [base_ip]
        else:
            prefix = ".".join(base_ip.split(".")[:3])
            addresses = [f"{prefix}.{index}" for index in range(1, 255)]
    except Exception:
        addresses = []

    online_hosts = [host for host in addresses if ping_host(host)]
    return render_template("index.html", online_hosts=online_hosts, section="ping")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
