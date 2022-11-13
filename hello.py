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


@app.route("/main/login/", methods=['GET', 'POST'])
def login_list():
    error, email = '', ''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        clients = db.select(f"SELECT * FROM users ORDER BY id")
        for user in clients:
            if user['email'] == email and user['password'] == password:
                response = f'успешно добавлен'
        error = 'Неверные пароль или логин'
        context = {'error': error,
                   'email': email,
                   'response': response}
        return render_template("login.html", **context)
    context = {'error': error,
               'email': email}
    return render_template("login.html", **context)


@app.route("/registration/", methods=['GET', 'POST'])
def registration_list():
    error = ''
    email, name, surname, patronymic, birthday, phone = '', '', '', '', '', ''
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        surname = request.form.get('surname')
        patronymic = request.form.get('patronymic')
        birthday = request.form.get('birthday')
        phone = request.form.get('phone')
        floor = request.form.get('floor')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        id = request.form.get('id')
        # emails = db.select_something('client', 'email')
        # if email in emails:
        #     error = 'Пользователь с таким логином уже зарегестрирован'
        # if password != repeat_password:
        #     error = 'Пароли не совпадают'
        # elif ('@' not in email or '.' not in email) and email != 'admin':
        #     error = 'Логин не верный'
        # elif birthday >= '2020-12-31':
        #     error = 'Дата не верна'
        if not error:
            db.insert(f"INSERT INTO users(id, email, name, surname, patronymic, floor, birthday, password, phone) values ({int(id)}, '{email}', '{name}', '{surname}', '{patronymic}', '{floor}', '{birthday}', '{password}', {phone});")
            res = make_response("main.html")
            res.set_cookie("user", email, 60 * 60 * 24 * 15)
            res.headers['location'] = url_for('main_page')
            response = f'"{name}" успешно добавлен'
        context = {'error': error,
                   'id': id,
                   'email': email,
                   'name': name,
                   'patronymic': patronymic,
                   'floor': floor,
                   'surname': surname,
                   'birthday': birthday,
                   'phone': phone,
                   'response': response}
        return render_template("registration.html", **context)
    context = {'error': error,
                   'email': email,
                   'name': name,
                   'patronymic': patronymic,
                   'surname': surname,
                   'birthday': birthday,
                   'phone': phone}
    return render_template("registration.html", **context)


@app.route("/wishes/")
def wishes_list():
    return render_template("wishes.html")


@app.route("/cart/")
def cart_list():
    return render_template("cart.html")


@app.route("/product/<int:product_id>")
def get_product(product_id):
    product = db.select(f"SELECT * FROM products WHERE id = {product_id}")

    if len(product):
        return render_template("product.html", title=product[0]['id'], product=product[0])


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


@app.route('/product_form/', methods=['GET', 'POST'])
def render_form():
    if request.method == 'GET':
        return render_template('product_form.html')

    id = request.form.get('id')
    category = request.form.get('category')
    name = request.form.get('name')
    gramms = request.form.get('gramms')
    price = request.form.get('price')
    img = request.form.get('img')
    description = request.form.get('description')
    nutritional_value = request.form.get('nutritional_value')

    products = db.insert(
        f"INSERT INTO products (id, category, name, gramms, price, img, description, nutritional_value) VALUES ({int(id)}, '{category}', '{name}', {int(gramms)}, {int(price)}, '{img}', '{description}', '{nutritional_value}');")

    response = f'"{name}" успешно добавлен'
    context = {
        'response': response,
        'products': products,
        'img': img,
        'name': name,
        'category': category,
        'id': id,
        'gramms': gramms,
        'price': price,
        'description': description,
        'nutritional_value': nutritional_value
    }

    return render_template('product_form.html', **context)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
