from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from services.local_service import save_to_local_csv
from services.aws_service import send_to_lambda

load_dotenv()

app = Flask(__name__)

ENV = os.getenv("ENV")
FILE_NAME = os.getenv("FILE_NAME")
LAMBDA_URL = os.getenv("LAMBDA_URL")


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "phone": request.form['phone']
    }

    if ENV == "local":
        save_to_local_csv(data, FILE_NAME)
        return "Saved Locally ✅"

    elif ENV == "prod":
        send_to_lambda(data, LAMBDA_URL)
        return "Saved to AWS ☁️"

    return "Invalid ENV ❌"


if __name__ == "__main__":
    app.run(debug=True)