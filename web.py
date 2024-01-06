from flask import Flask, render_template, request, redirect, url_for
import pickle
import sqlite3
import pandas as pd
import numpy as np
import os

# from io import BytesIO

# Connect to SQLite database (this will create a new database if it doesn't exist)
conn = sqlite3.connect("titanic_database.db")

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Define the table schema
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pclass INTEGER,
        gender INTEGER,
        age INTEGER,
        sibsp INTEGER,
        parch INTEGER,
        fare INTEGER,
        embarked INTEGER,
        prediction INTEGER,
        Probability INTEGER
    )
"""
)

# Commit the changes and close the connection
conn.commit()
conn.close()


with open("titanic_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", Titanic="Titanic")


@app.route("/about")
def about():
    return render_template("about.html", About="About")


@app.route("/Team")
def contact():
    return render_template("team.html", Team="Team")


@app.route("/dashboard")
def dashboard():
    FLASK_PORT = 5000
    STREAMLIT_PORT = 8501

    # Run Flask in a separate thread
    import threading

    flask_thread = threading.Thread(
        target=app.run, kwargs={"debug": True, "port": FLASK_PORT}
    )
    flask_thread.start()

    # Wait for Flask to start before running Streamlit
    import time

    time.sleep(0)

    # Run Streamlit in a separate thread
    streamlit_thread = threading.Thread(
        target=os.system,
        args=(f"streamlit run streamlit_app.py --server.port {STREAMLIT_PORT}",),
    )
    streamlit_thread.start()
    return redirect("http://localhost:8501/")


@app.route("/predict", methods=["POST"])
def predict():
    Pclass = int(request.form["Pclass"])
    Sex = int(request.form["Gender"])
    Age = int(request.form["Age"])
    SibSp = int(request.form["SibSp"])
    Parch = int(request.form["Parch"])
    Fare = int(request.form["Fare"])
    Embarked = int(request.form["Embarked"])

    model_survival = model.predict([[Pclass, Sex, Age, SibSp, Parch, Fare, Embarked]])
    probs = model.predict_proba(
        np.array([Pclass, Sex, Age, SibSp, Parch, Fare, Embarked]).reshape(1, -1)
    )
    prob = round(probs[0, 1], 2)
    # Insert data into the database
    conn = sqlite3.connect("titanic_database.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO predictions (pclass, gender, age, sibsp, parch, fare, embarked, prediction,Probability)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
    """,
        (Pclass, Sex, Age, SibSp, Parch, Fare, Embarked, model_survival[0], prob),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("result", prediction=model_survival[0], Probability=prob))


@app.route("/result")
def result():
    current_prediction = request.args.get("prediction", type=int)
    current_prob = request.args.get("Probability", type=float)
    # Fetch recent predictions from the database
    conn = sqlite3.connect("titanic_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions ORDER BY id DESC LIMIT 5")
    recent_predictions = cursor.fetchall()
    conn.close()

    # Convert each prediction to a tuple of integers
    recent_predictions = [
        (
            pred[0],
            "First Class"
            if pred[1] == 1
            else ("Second Class" if pred[1] == 2 else "Third Class"),
            "Female" if pred[2] else "Male",
            pred[3],
            pred[4],
            pred[5],
            pred[6],
            "Cherbourg"
            if pred[7] == 2
            else ("Queenstown" if pred[7] == 0 else "Southampton"),
            "Survived"
            if int.from_bytes(pred[8], byteorder="big", signed=False)
            else "Not Survived",
            pred[9],
        )
        for pred in recent_predictions
    ]

    # Create a DataFrame
    columns = [
        "ID",
        "pclass",
        "gender",
        "age",
        "sibsp",
        "parch",
        "fare",
        "embarked",
        "prediction",
        "Probability",
    ]
    df = pd.DataFrame(recent_predictions, columns=columns)

    # Convert the DataFrame to HTML table
    table_html = df.to_html(index=False)

    return render_template(
        "result.html",
        Probability=current_prob,
        prediction=current_prediction,
        recent_predictions=recent_predictions,
        Prediction="Prediction",
        table_html=table_html,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
    # Specify the ports for Flask and Streamlit
