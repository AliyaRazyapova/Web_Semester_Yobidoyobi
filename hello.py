import datetime

from flask import Flask, make_response, session, request, render_template, redirect, url_for
from db_util import Database


app = Flask(__name__)
app.secret_key = "111"

app.permanent_session_lifetime = datetime.timedelta(days=365)

db = Database()


@app.route("/")
def main_page():
    return redirect(url_for("main_list"))


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


@app.route("/login/", methods=['POST', 'GET'])
def login_list():
    error, email = '', ''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        clients = db.select(f"SELECT * FROM users ORDER BY user_id")
        for user in clients:
            if user['email'] == email and user['password'] == password:
                res = make_response()
                res.set_cookie("postgres", email, 60 * 60 * 24 * 15)
                res.headers['location'] = url_for('main_list')
                return res, 302
        error = 'Неверные логин или пароль'
        context = {'error': error,
                   'email': email}
        return render_template("login.html", **context)
    context = {'error': error,
               'email': email}
    return render_template("login.html", **context)


@app.route("/logout/")
def logout():
    res = make_response("")
    email = request.cookies.get('postgres')
    res.set_cookie('postgres', email, max_age=0)
    res.headers['location'] = url_for('main_list')
    return res, 302


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
        emails = db.select(f"SELECT email FROM users;")
        if email in emails:
            error = 'Пользователь с таким логином уже зарегестрирован'
        if password != repeat_password:
            error = f'Пароли не совпадают'
        elif '@' not in email or '.' not in email:
            error = 'Логин не верный'
        elif birthday >= '2012-11-16':
            error = 'Дата не верна'
        if not error:
            db.insert(f"INSERT INTO users(email, name, surname, patronymic, floor, birthday, password, phone) values ('{email}', '{name}', '{surname}', '{patronymic}', '{floor}', '{birthday}', '{password}', {phone});")
            return redirect(url_for("main_list"))
        context = {'email': email,
                   'name': name,
                   'patronymic': patronymic,
                   'floor': floor,
                   'surname': surname,
                   'birthday': birthday,
                   'phone': phone}
        return render_template("registration.html", **context)
    context = {'error': error,
                'email': email,
                'name': name,
                'patronymic': patronymic,
                'surname': surname,
                'birthday': birthday,
                'phone': phone}
    return render_template("registration.html", **context)


@app.route("/profil/", methods=['GET', 'POST'])
def profil_list():
    email_1 = request.cookies.get('postgres')
    user = db.select(f"SELECT * FROM users WHERE email = '{email_1}';")
    if request.method == 'POST':
        return redirect(url_for('profil_redactor'), 301)
    return render_template("profil.html", user=user)


@app.route("/profil/redactor/", methods=['GET', 'POST'])
def profil_redactor():
    error = ''
    email_1 = request.cookies.get('postgres')
    user = db.select(f"SELECT * FROM users WHERE email = '{email_1}';")
    id = user[0]['user_id']
    print(id)
    if request.method == 'POST':
        surname = request.form.get('surname')
        name = request.form.get('name')
        patronymic = request.form.get('patronymic')
        email = request.form.get('email')
        floor = request.form.get('floor')
        birthday = request.form.get('birthday')
        phone = request.form.get('phone')
        if '@' not in email or '.' not in email:
            error = 'Логин не верный'
        elif birthday >= '2012-11-16':
            error = 'Дата не верна'
        if not error:
            if surname != user[0]['surname']:
                db.insert(f"UPDATE users SET surname = '{surname}' WHERE user_id = {id};")
            if name != user[0]['name']:
                db.insert(f"UPDATE users SET name = '{name}' WHERE user_id = {id};")
            if patronymic != user[0]['patronymic']:
                db.insert(f"UPDATE users SET patronymic = '{patronymic}' WHERE user_id = {id};")
            if email != user[0]['email']:
                db.insert(f"UPDATE users SET email = '{email}' WHERE user_id = {id};")
            if floor != user[0]['floor']:
                db.insert(f"UPDATE users SET floor = '{floor}' WHERE user_id = {id};")
            if birthday != user[0]['birthday']:
                db.insert(f"UPDATE users SET birthday = '{birthday}' WHERE user_id = {id};")
            if phone != user[0]['phone']:
                db.insert(f"UPDATE users SET phone = '{phone}' WHERE user_id = {id};")
                res = make_response("")
                res.set_cookie("postgres", email, 60 * 60 * 24 * 15)
                res.headers['location'] = url_for('profil_list')
                return res, 301
            return redirect(url_for('profil_list'), 301)
        return render_template('profil_redactor.html', user=user, error=error)
    return render_template("profil_redactor.html", user=user, error=error)


@app.route("/wishes/")
def wishes_list():
    # if request.method == 'POST':
        # email_1 = request.cookies.get('postgres')
        # user = db.select(f"SELECT * FROM users WHERE email = '{email_1}';")
        # id = user[0]['user_id']
        # print(email_1)
        # print(user)
        # print(id)
    return render_template("wishes.html")


@app.route("/cart/", methods=['POST', 'GET'])
def cart_list():
    return render_template("cart.html")


@app.route("/product/<int:product_id>/wishes_add/")
def get_product_wishes_add(product_id):
    product = db.select(f"SELECT * FROM products WHERE product_id = {product_id}")
    email_1 = request.cookies.get('postgres')
    user = db.select(f"SELECT * FROM users WHERE email = '{email_1}';")
    user_1 = user[0]['user_id']
    product_1 = product[0]['product_id']
    db.insert(f"INSERT INTO wishes(user_id, product_id) values ('{user_1}', '{product_1}');")
    return redirect(url_for("get_product", product_id=product[0]['product_id']), 301)


@app.route("/product/<int:product_id>/cart_add/")
def get_product_cart_add(product_id):
    product = db.select(f"SELECT * FROM products WHERE product_id = {product_id}")
    email_1 = request.cookies.get('postgres')
    user = db.select(f"SELECT * FROM users WHERE email = '{email_1}';")
    user_1 = user[0]['user_id']
    product_1 = product[0]['product_id']
    db.insert(f"INSERT INTO cart(user_id, product_id) values ('{user_1}', '{product_1}');")
    return redirect(url_for("get_product", product_id=product[0]['product_id']), 301)


@app.route("/product/<int:product_id>")
def get_product(product_id):
    product = db.select(f"SELECT * FROM products WHERE product_id = {product_id}")

    if len(product):
        return render_template("product.html", title=product[0]['product_id'], product=product[0])

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

    category = request.form.get('category')
    name = request.form.get('name')
    gramms = request.form.get('gramms')
    price = request.form.get('price')
    img = request.form.get('img')
    description = request.form.get('description')
    nutritional_value = request.form.get('nutritional_value')

    products = db.insert(
        f"INSERT INTO products (category, name, gramms, price, img, description, nutritional_value) VALUES ({category}', '{name}', {int(gramms)}, {int(price)}, '{img}', '{description}', '{nutritional_value}');")

    response = f'"{name}" успешно добавлен'
    context = {
        'response': response,
        'products': products,
        'img': img,
        'name': name,
        'category': category,
        'gramms': gramms,
        'price': price,
        'description': description,
        'nutritional_value': nutritional_value
    }

    return render_template('product_form.html', **context)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
