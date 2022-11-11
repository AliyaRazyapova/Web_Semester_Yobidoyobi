import datetime

from flask import Flask, make_response, session, request, render_template, redirect, url_for
from db_util import Database
# from help_function import get_sets_from_db

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
    name = request.args.get("name")
    img = request.args.get("img")
    category = request.args.get("category")
    products = db.select(f"SELECT * FROM products WHERE category = 'popular'")
    context = {
        'products': products,
        'img': img,
        'name': name,
        'category': category
    }

    return render_template("main.html", **context)


@app.route("/login/")
def login_list():
    return render_template("login.html")


@app.route("/registration/")
def registration_list():
    return render_template("registration.html")


@app.route("/wishes/")
def wishes_list():
    return render_template("wishes.html")


@app.route("/cart/")
def cart_list():
    return render_template("cart.html")


@app.route("/product/")
def get_product(product_id):
    product = db.select(f"SELECT * FROM products WHERE id = {product_id}")


@app.route("/sets/")
def sets_list():
    name = request.args.get("name")
    img = request.args.get("img")
    category = request.args.get("category")
    products = db.select(f"SELECT * FROM products WHERE category = 'sets'")
    context = {
        'products': products,
        'img': img,
        'name': name,
        'category': category
    }

    return render_template("sets.html", **context)


@app.route("/premium/")
def premium_list():
    return render_template("premium.html")


@app.route("/rolls_and_sushi/")
def rolls_and_sushi_list():
    return render_template("rolls_and_sushi.html")


@app.route("/tempura/")
def tempura_list():
    return render_template("tempura.html")


@app.route("/baked/")
def baked_list():
    return render_template("baked.html")


@app.route("/hot_and_salads/")
def hot_and_salads_list():
    return render_template("hot_and_salads.html")


@app.route("/sauces/")
def sauces_list():
    return render_template("sauces.html")


@app.route("/drinks_and_desserts/")
def drinks_and_desserts_list():
    return render_template("drinks_and_desserts.html")


@app.route("/spices/")
def spices_list():
    return render_template("spices.html")


if __name__ == '__main__':
    app.run(port=8000, debug=True)