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
    title = 'Ёбидоёби'
    error = 'Товара данной категории нет'
    products = db.select(f"SELECT * FROM products WHERE category = 'popular'")

    if len(products) == 0:
        return render_template('error.html', error=error)
    return render_template("main.html", products=products, title=title)


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
    user_1 = user[0]['user_id']
    orders = db.select(f"SELECT * FROM orders WHERE user_id = '{user_1}';")
    order_num = []
    for i in range(len(orders)):
        kek = int(orders[i]['order_number'])
        if not kek in order_num:
            order_num.append(kek)
    tk_1 = []
    for i in range(len(order_num)):
        tk = db.select(f"SELECT COUNT(*) FROM orders WHERE order_number = '{str(order_num[i])}';")
        tk_1.append(tk[0]['count'])
    kek = len(tk_1)
    lol = len(order_num)
    if request.method == 'POST':
        return redirect(url_for('profil_redactor'), 301)
    return render_template("profil.html", user=user, kek=kek, orders=orders, lol=lol, tk=tk_1, order_num=order_num)


@app.route("/profil/redactor/", methods=['GET', 'POST'])
def profil_redactor():
    error = ''
    email_1 = request.cookies.get('postgres')
    user = db.select(f"SELECT * FROM users WHERE email = '{email_1}';")
    id = user[0]['user_id']
    if request.method == 'POST':
        surname = request.form.get('surname')
        name = request.form.get('name')
        patronymic = request.form.get('patronymic')
        email = request.form.get('email')
        floor = request.form.get('floor')
        birthday = request.form.get('birthday')
        phone = request.form.get('phone')
        adres = request.form.get('adres')
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
            if adres != user[0]['adres']:
                db.insert(f"UPDATE users SET adres = '{adres}' WHERE user_id = '{id}'")
                res = make_response("")
                res.set_cookie("postgres", email, 60 * 60 * 24 * 15)
                res.headers['location'] = url_for('profil_list')
                return res, 301
            return redirect(url_for('profil_list'), 301)
        return render_template('profil_redactor.html', user=user, error=error)
    return render_template("profil_redactor.html", user=user, error=error)


@app.route("/wishes/")
def wishes_list():
    error = 'Вам ничего не нравится? Жмите кнопочку "Избранное"'
    email_1 = request.cookies.get('postgres')
    user = db.select(f"SELECT * FROM users WHERE email = '{email_1}';")
    user_1 = user[0]['user_id']
    products = db.select(
        f"SELECT * FROM products JOIN (SELECT product_id, user_id FROM wishes GROUP BY user_id, product_id) c ON products.product_id = c.product_id WHERE user_id='{user_1}';")
    if products:
        return render_template("wishes.html", products=products)
    else:
        return render_template('error.html', error=error)


@app.route("/cart/", methods=['POST', 'GET'])
def cart_list():
    error = 'Корзина пуста'
    email_1 = request.cookies.get('postgres')
    user = db.select(f"SELECT * FROM users WHERE email = '{email_1}';")
    user_1 = user[0]['user_id']
    products = db.select(
        f"SELECT * FROM products JOIN (SELECT product_id, user_id FROM cart GROUP BY user_id, product_id) c ON products.product_id = c.product_id WHERE user_id='{user_1}';")
    ab = len(products)
    amount_1 = []
    cost_1 = []
    for i in range(len(products)):
        product_1 = products[i]['product_id']
        amount = db.select(f"SELECT amount FROM cart WHERE user_id = '{user_1}' AND product_id = '{product_1}';")[0]['amount']
        if amount == 0:
            get_product_cart_delete(product_1)
        amount_1.append(amount)
        price = int(products[i]['price'])
        cost = price * amount
        cost_1.append(cost)
    cost_all = sum(cost_1)
    if products:
        return render_template("cart.html", products=products, ab=ab, amount=amount_1, cost=cost_1, cost_all=cost_all)
    else:
        return render_template('error.html', error=error)


@app.route("/message/", methods=['POST', 'GET'])
def message_list():
    email_1 = request.cookies.get('postgres')
    user = db.select(f"SELECT * FROM users WHERE email = '{email_1}';")
    user_1 = user[0]['user_id']
    products = db.select(
        f"SELECT * FROM products JOIN (SELECT product_id, user_id FROM cart GROUP BY user_id, product_id) c ON products.product_id = c.product_id WHERE user_id='{user_1}';")
    ab = len(products)
    amount_1 = []
    cost_1 = []
    orders = db.select(f"SELECT * FROM orders WHERE user_id = '{user_1}';")
    if not orders:
        order_number = 1
    else:
        order_number = 0
        for i in range(len(orders)):
            if int(orders[i]['order_number']) > order_number:
                order_number = int(orders[i]['order_number'])
        order_number += 1
    for i in range(len(products)):
        product_1 = products[i]['product_id']
        amount = db.select(f"SELECT amount FROM cart WHERE user_id = '{user_1}' AND product_id = '{product_1}';")[0][
            'amount']
        if amount == 0:
            get_product_cart_delete(product_1)
        amount_1.append(amount)
        price = int(products[i]['price'])
        cost = price * amount
        cost_1.append(cost)
    cost_all = sum(cost_1)
    for i in range(len(products)):
        product_1 = products[i]['product_id']
        db.insert(f"INSERT INTO orders(user_id, product_name, order_number, cost) values ('{user_1}', '{products[i]['name']}', '{order_number}', '{cost_all}');")
        get_product_cart_delete(product_1)
    if products:
        return render_template("message.html")
    else:
        return redirect(url_for('main_list'), 302)


@app.route("/order/", methods=['POST', 'GET'])
def order_list():
    email_1 = request.cookies.get('postgres')
    user = db.select(f"SELECT * FROM users WHERE email = '{email_1}';")
    user_1 = user[0]['user_id']
    products = db.select(
        f"SELECT * FROM products JOIN (SELECT product_id, user_id FROM cart GROUP BY user_id, product_id) c ON products.product_id = c.product_id WHERE user_id='{user_1}';")
    ab = len(products)
    amount_1 = []
    cost_1 = []
    orders = db.select(f"SELECT * FROM orders WHERE user_id = '{user_1}';")
    if not orders:
        order_number = 1
    else:
        order_number = 0
        for i in range(len(orders)):
            if int(orders[i]['order_number']) > order_number:
                order_number = int(orders[i]['order_number'])
        order_number += 1
    for i in range(len(products)):
        product_1 = products[i]['product_id']
        amount = db.select(f"SELECT amount FROM cart WHERE user_id = '{user_1}' AND product_id = '{product_1}';")[0]['amount']
        if amount == 0:
            get_product_cart_delete(product_1)
        amount_1.append(amount)
        price = int(products[i]['price'])
        cost = price * amount
        cost_1.append(cost)
    cost_all = sum(cost_1)
    if products:
        return render_template("orders.html", products=products, ab=ab, amount=amount_1, cost=cost_1, cost_all=cost_all, user=user[0], order_number=order_number)


@app.route("/product/<int:product_id>/wishes_add/")
def get_product_wishes_add(product_id):
    product = db.select(f"SELECT * FROM products WHERE product_id = {product_id}")
    email_1 = request.cookies.get('postgres')
    user = db.select(f"SELECT * FROM users WHERE email = '{email_1}';")
    user_1 = user[0]['user_id']
    product_1 = product[0]['product_id']
    db.insert(f"INSERT INTO wishes(user_id, product_id) values ('{user_1}', '{product_1}');")
    return redirect(url_for("wishes_list"), 302)


@app.route("/product/<int:product_id>/cart_add/")
def get_product_cart_add(product_id):
    product = db.select(f"SELECT * FROM products WHERE product_id = {product_id}")
    email_1 = request.cookies.get('postgres')
    user = db.select(f"SELECT * FROM users WHERE email = '{email_1}';")
    user_1 = user[0]['user_id']
    product_1 = product[0]['product_id']
    db.insert(f"INSERT INTO cart(user_id, product_id) values ('{user_1}', '{product_1}');")
    return redirect(url_for("cart_list"), 302)


@app.route("/product/<int:product_id>/cart_redactor_amount_product_plus/", methods=['GET', 'POST'])
def cart_redactor_amount_product_plus(product_id):
    email_1 = request.cookies.get('postgres')
    user = db.select(f"SELECT * FROM users WHERE email = '{email_1}';")
    user_1 = user[0]['user_id']
    amount = db.select(f"SELECT * FROM cart WHERE user_id = '{user_1}';")
    amount_1 = int(amount[0]['amount']) + 1
    product_1 = product_id
    db.insert(f"UPDATE cart SET amount = '{amount_1}' WHERE user_id = {user_1} AND product_id = {product_1};")
    amount_2 = int(db.select(f"SELECT * FROM cart WHERE user_id = '{user_1}';")[0]['amount'])
    if amount_2 < 1:
        get_product_cart_delete(product_1)
    return redirect(url_for("cart_list", amount=amount_2), 302)


@app.route("/product/<int:product_id>/cart_redactor_amount_product_minus/", methods=['GET', 'POST'])
def cart_redactor_amount_product_minus(product_id):
    email_1 = request.cookies.get('postgres')
    user = db.select(f"SELECT * FROM users WHERE email = '{email_1}';")
    user_1 = user[0]['user_id']
    amount = db.select(f"SELECT * FROM cart WHERE user_id = '{user_1}';")
    amount_1 = int(amount[0]['amount']) - 1
    product_1 = product_id
    db.insert(f"UPDATE cart SET amount = '{amount_1}' WHERE user_id = {user_1} AND product_id = {product_1};")
    amount_2 = int(db.select(f"SELECT * FROM cart WHERE user_id = '{user_1}';")[0]['amount'])
    if amount_2 == 0:
        get_product_cart_delete(product_1)
    return redirect(url_for("cart_list", amount=amount_2), 302)

@app.route("/product/<int:product_id>/car_delete/")
def get_product_cart_delete(product_id):
    product = db.select(f"SELECT * FROM products WHERE product_id = {product_id}")
    email_1 = request.cookies.get('postgres')
    user = db.select(f"SELECT * FROM users WHERE email = '{email_1}';")
    user_1 = user[0]['user_id']
    product_1 = product[0]['product_id']
    db.insert(
        f"DELETE FROM cart WHERE user_id = '{user_1}' AND product_id = '{product_1}' AND ctid = (SELECT min(ctid) FROM cart WHERE user_id = '{user_1}' and product_id = '{product_1}');")
    return redirect(url_for("cart_list", product_id=product_1), 301)


@app.route("/product/<int:product_id>/wishes_delete/")
def get_product_wishes_delete(product_id):
    product = db.select(f"SELECT * FROM products WHERE product_id = {product_id}")
    email_1 = (request.cookies.get('postgres'))
    user = db.select(f"SELECT * FROM users WHERE email = '{email_1}';")
    user_1 = user[0]['user_id']
    product_1 = product[0]['product_id']
    db.insert(
        f"DELETE FROM wishes WHERE user_id = '{user_1}' AND product_id = '{product_1}' AND ctid = (SELECT min(ctid) FROM wishes WHERE user_id = '{user_1}' and product_id = '{product_1}');")
    return redirect(url_for("wishes_list"), 302)


@app.route("/product/<int:product_id>")
def get_product(product_id):
    product = db.select(f"SELECT * FROM products WHERE product_id = {product_id}")
    users = db.select(f"SELECT user_id FROM users WHERE role = 'admin'")
    admins = []
    for i in range(len(users)):
        admins.append(users[i]['user_id'])
    email_1 = (request.cookies.get('postgres'))
    user = db.select(f"SELECT * FROM users WHERE email = '{email_1}';")
    user_1 = user[0]['user_id']
    param = False
    if user_1 in admins:
        param = True
    if len(product):
        return render_template("product.html", title=product[0]['product_id'], product=product[0], users=users, param=param)

@app.route("/sets/")
def sets_list():
    error = 'Товара данной категории нет'
    category = 'sets'
    title = 'Наборы'
    products = db.get_category_page('products', category, 'category')

    if len(products) == 0:
        return render_template('error.html', error=error)
    return render_template("base_products.html", products=products, title=title)


@app.route("/premium/")
def premium_list():
    error = 'Товара данной категории нет'
    category = 'premium'
    products = db.get_category_page('products', category, 'category')

    if len(products)==0:
        return render_template('error.html', error=error)
    return render_template("base_products.html", products=products)

@app.route("/rolls_and_sushi/")
def rolls_and_sushi_list():
    error = 'Товара данной категории нет'
    category = 'rolls_and_sushi'
    products = db.get_category_page('products', category, 'category')

    if len(products) == 0:
        return render_template('error.html', error=error)
    return render_template("base_products.html", products=products)


@app.route("/tempura/")
def tempura_list():
    error = 'Товара данной категории нет'
    category = 'tempura'
    products = db.get_category_page('products', category, 'category')

    if len(products) == 0:
        return render_template('error.html', error=error)
    return render_template("base_products.html", products=products)


@app.route("/baked/")
def baked_list():
    error = 'Товара данной категории нет'
    category = 'baked'
    products = db.get_category_page('products', category, 'category')

    if len(products) == 0:
        return render_template('error.html', error=error)
    return render_template("base_products.html", products=products)


@app.route("/hot_and_salads/")
def hot_and_salads_list():
    error = 'Товара данной категории нет'
    category = 'hot_and_salads'
    products = db.get_category_page('products', category, 'category')

    if len(products) == 0:
        return render_template('error.html', error=error)
    return render_template("base_products.html", products=products)


@app.route("/sauces/")
def sauces_list():
    error = 'Товара данной категории нет'
    category = 'sauces'
    products = db.get_category_page('products', category, 'category')

    if len(products) == 0:
        return render_template('error.html', error=error)
    return render_template("base_products.html", products=products)


@app.route("/drinks_and_desserts/")
def drinks_and_desserts_list():
    error = 'Товара данной категории нет'
    category = 'drinks_and_desserts'
    products = db.get_category_page('products', category, 'category')

    if len(products) == 0:
        return render_template('error.html', error=error)
    return render_template("base_products.html", products=products)


@app.route("/spices/")
def spices_list():
    error = 'Товара данной категории нет'
    category = 'spices'
    products = db.get_category_page('products', category, 'category')

    if len(products) == 0:
        return render_template('error.html', error=error)
    return render_template("base_products.html", products=products)


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


@app.route('/product/<int:product_id>/delete/', methods=['GET', 'POST'])
def render_form_delete(product_id):
    db.insert(f"DELETE FROM products WHERE product_id = '{product_id}'")
    return redirect(url_for('main_list'), 302)


@app.route('/product/<int:product_id>/redactor/', methods=['GET', 'POST'])
def render_form_redactor(product_id):
    products = db.select(f"SELECT * FROM products WHERE product_id = '{product_id}';")
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        gramms = request.form.get('gramms')
        price = request.form.get('price')
        img = request.form.get('img')
        description = request.form.get('description')
        nutritional_value = request.form.get('nutritional_value')
        if category != products[0]['category']:
            db.insert(f"UPDATE products SET category = '{category}' WHERE product_id = '{product_id}';")
        if name != products[0]['name']:
            db.insert(f"UPDATE products SET name = '{name}' WHERE product_id = '{product_id}';")
        if gramms != products[0]['gramms']:
            db.insert(f"UPDATE products SET gramms = '{gramms}' WHERE product_id = '{product_id}';")
        if price != products[0]['price']:
            db.insert(f"UPDATE products SET price = '{price}' WHERE product_id = '{product_id}';")
        if img != products[0]['img']:
            db.insert(f"UPDATE products SET img = '{img}' WHERE product_id = '{product_id}';")
        if description != products[0]['description']:
            db.insert(f"UPDATE products SET description = '{description}' WHERE product_id = '{product_id}';")
        if nutritional_value != products[0]['nutritional_value']:
            db.insert(f"UPDATE products SET nutritional_value = '{nutritional_value}' WHERE product_id = '{product_id}';")
            res = ""
            res.headers['location'] = url_for('main_list')
            return res, 301
        return redirect(url_for('main_list'), 302)
    return render_template('product_redactor.html', products=products)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
