from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

MODEL_PATH = "model/student_model.pkl"

model = joblib.load(MODEL_PATH)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    try:
        study_hours = float(request.form["study_hours"])
        attendance = float(request.form["attendance"])
        previous_marks = float(request.form["previous_marks"])
        assignments = float(request.form["assignments"])
        sleep_hours = float(request.form["sleep_hours"])

        features = np.array([[
            study_hours,
            attendance,
            previous_marks,
            assignments,
            sleep_hours
        ]])

        prediction = model.predict(features)[0]

        prediction = round(float(prediction), 2)

        if prediction >= 75:
            performance = "Excellent"
        elif prediction >= 60:
            performance = "Good"
        elif prediction >= 40:
            performance = "Average"
        else:
            performance = "Needs Improvement"

        return render_template(
            "index.html",
            prediction=prediction,
            performance=performance
        )

    except Exception as e:

        return render_template(
            "index.html",
            error=str(e)
        )


@app.route("/health")
def health():

    return jsonify({
        "status": "healthy",
        "application": "Student Performance Predictor"
    })


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
