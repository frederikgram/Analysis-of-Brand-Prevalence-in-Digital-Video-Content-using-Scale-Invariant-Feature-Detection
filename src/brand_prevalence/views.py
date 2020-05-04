""" """

import os
import subprocess

from flask import Flask, Response, request, send_from_directory, render_template
from .processing import pipe
from brand_prevalence import app

@app.route("/generate_report", methods=["GET"])
def generate_report():
    """ """

    video_id = request.form.get('video_id')

    if video_id is None or video_id == "":
        return Exception("Video ID field is empty")

    try:
        # Generate Report
        p = subprocess.Popen([
            "python", "-m", "./processing/pipe.py", 
            "--video-id", f"{video_id}",
            "--output-dir", "./output",
            "--brand-logo", "./resources/template.png",
            "--use-grayscale"],
            shell=True
        )

        # Wait for report to be finished
        p_status = p.wait()
    except Exception as e:
        return e

    filename = f"{str(video_id)}_report.pdf"
    if not os.path.isfile(os.path.join("output", filename)):
        return Exception("Report file could not be found") 

    return send_from_directory('output', filename)

@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")