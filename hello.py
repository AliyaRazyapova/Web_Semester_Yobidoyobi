import datetime

from flask import Flask, make_response, session, request, render_template, redirect, url_for
from db_util import Database

app = Flask(__name__)
app.secret_key = "111"

app.permanent_session_lifetime = datetime.timedelta(days=365)

db = Database()


# метод для создания куки
@app.route("/add_cookie")
def add_cookie():
    resp = make_response("Add cookie")
    resp.set_cookie("test", "val")
    return resp


# метод для удаления куки
@app.route("/delete_cookie")
def delete_cookie():
    resp = make_response("Delete cookie")
    resp.set_cookie("test", "val", 0)


# реализация визитов
@app.route("/visits")
def visits():
    visits_count = session['visits'] if 'visits' in session.keys() else 0
    session['visits'] = visits_count + 1

    return f"Количество визитов: {session['visits']}"


# удаление данных о посещениях
@app.route("/delete_visits")
def delete_visits():
    session.pop('visits')
    return "ok"


@app.route("/")
def main_page():
    return redirect("/main/")


@app.route("/main/")
def main_list():
    return render_template("main.html")


@app.route("/login/")
def login_list():
    return render_template("login.html")


@app.route("/registration/")
def registration_list():
    return render_template("registration.html")


if __name__ == '__main__':
    app.run(port=8000, debug=True)