# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, redirect, session, flash, url_for
import mysql.connector  # Замените pyodbc на mysql.connector
import time
import random
import requests
from io import BytesIO
from PIL import Image
import subprocess
import os
import bcrypt
import re


# Подключение к MySQL
connection_config = {
    'user': 'Serg0239',
    'password': 'Young_jaba123',
    'host': 'Serg0239.mysql.pythonanywhere-services.com',
    'database': 'Serg0239$Secret_Santa',
}

app = Flask(__name__)
app.secret_key = 'ssshizi'

@app.route('/')
def hello_world():
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def submit():
    return post_def()

@app.route('/registration', methods=['POST'])
def submit1():
    return registration()

@app.route('/register')
def register():
    return render_template('registration.html')

@app.route('/update_profile_page')
def update_profile_page():
    username_lk = session.get('username')
    if username_lk:
        info_lk = get_user_info(username_lk)
        FullName = info_lk[1]
        Wish = info_lk[2]
        Wish_list = info_lk[3]
        Photo_path = info_lk[4]
        Discription = info_lk[5]

        with open(f'/home/Serg0239/mysite/static/userslinks/{username_lk}.txt', 'r', encoding='utf-8') as file:
            link_line = file.readline()

        return render_template('update_info.html', username=username_lk, FullName=FullName, Wish=Wish, Wish_list=link_line, Photo_path=Photo_path, Discription=Discription)
    else:
        return redirect(url_for('error'))

@app.route('/save_profile', methods=['POST'])
def save_profile():
    username_lk = session.get('username')
    if username_lk:
        FullName = request.form['fullname']
        Discription = request.form['description']
        Wish = request.form['wish']
        Wish_url = request.form['wish_list']
        #Photo_path = request.form['photo_path']
        Photo_path = request.files['photo_path']
        #print(Photo_path)

        if 'Введи ссылку в формате' in Wish_url or not Wish_url:
            with open(f'/home/Serg0239/mysite/static/userslinks/{username_lk}.txt', 'w', encoding='utf-8') as file:
                link_line = file.write('Введи ссылку в формате: Пиво$https://serg0239.pythonanywhere.com/static/usersphoto/pivo.jpg')
        else:
            with open(f'/home/Serg0239/mysite/static/userslinks/{username_lk}.txt', 'w', encoding='utf-8') as file:
                link_line = file.write(Wish_url)

        if Photo_path:
            app.config['UPLOAD_FOLDER'] = '/home/Serg0239/mysite/static/usersphoto'
            Photo_path_new = f'{username_lk}.jpg'
            filename = os.path.join(app.config['UPLOAD_FOLDER'], Photo_path_new)
            Photo_path.save(filename)

            conn = mysql.connector.connect(**connection_config)
            cursor2 = conn.cursor()
            test = f"UPDATE Users_info SET FullName='{FullName}', Wish='{Wish}', Wish_url='/home/Serg0239/mysite/static/userslinks/{username_lk}.txt', Discription='{Discription}', Photo_path='https://serg0239.pythonanywhere.com/static/usersphoto/{username_lk}.jpg' WHERE UserName='{username_lk}'"
            #print(test)
            cursor2.execute(test)
            conn.commit()
            cursor2.close()
            conn.close()
        else:
            conn = mysql.connector.connect(**connection_config)
            cursor2 = conn.cursor()
            test = f"UPDATE Users_info SET FullName='{FullName}', Wish='{Wish}', Wish_url='/home/Serg0239/mysite/static/userslinks/{username_lk}.txt', Discription='{Discription}', Photo_path='https://serg0239.pythonanywhere.com/static/usersphoto/{username_lk}.jpg' WHERE UserName='{username_lk}'"
            #print(test)
            cursor2.execute(test)
            conn.commit()
            cursor2.close()
            conn.close()

        return redirect(url_for('lk'))
    else:
        return redirect(url_for('error'))

@app.route('/lk')
def lk():
    username_lk = session.get('username')
    if username_lk:
        info_lk = get_user_info(username_lk)
        FullName = info_lk[1]
        Wish = info_lk[2]
        Wish_list = info_lk[3]
        Photo_path = info_lk[4]
        Discription = info_lk[5]
        print(Photo_path)

        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor()
        cursor.execute("SELECT UserID from Users_pasport_new where Login = %s", (username_lk,))
        id =  cursor.fetchone()
        print(id)
        cursor.execute("SELECT U.Login FROM Secret_Santa_Assignments AS S JOIN Users_pasport_new AS U ON U.UserID = S.ReceiverID WHERE S.GiverID = %s", (id[0],))
        List_of_giter = cursor.fetchall()

        New_List_of_giter = []
        for gifter_from_list in List_of_giter:
            New_List_of_giter.append(gifter_from_list[0])
        Unique_New_List_of_giter = set(New_List_of_giter)
        #print(Unique_New_List_of_giter )

        cursor.execute("SELECT Login FROM Users_pasport_new WHERE UserID in (1,21,24,26,27,29,30,31,32,33,34,35) and UserID <> %s", (id[0],))
        List_of_user_wals = cursor.fetchall()
        print(List_of_user_wals )

        New_List_of_user_wals = []
        for wal_from_list in List_of_user_wals:
            New_List_of_user_wals.append(wal_from_list[0])
        Unique_New_List_user_wals = set(New_List_of_user_wals)
        print(Unique_New_List_user_wals)

        Wish_list_itog = pars_link(Wish_list)
        print(Wish_list_itog)

        return render_template('lk_inside.html', username=username_lk, FullName=FullName, Wish=Wish, Wish_list_itog=Wish_list_itog, Photo_path=Photo_path, Discription=Discription, Unique_New_List_of_giter=Unique_New_List_of_giter, Unique_New_List_user_wals=Unique_New_List_user_wals)
    else:
        flash('Пожалуйста, войдите в систему для доступа к личному кабинету.', 'error')
        return redirect(url_for('register'))

@app.route('/logout')
def logout():
    session.pop('username', None)  # Удаляем данные сессии
    flash('Вы успешно вышли из системы.', 'success')
    return redirect(url_for('register'))

@app.route('/error')
def register3():
    return render_template('error.html')

@app.route('/registr_new_user')
def register4():
    return render_template('registr_new_user.html')

@app.route('/about')
def about():
    username_lk = session.get('username')
    if username_lk:
        info_lk = get_user_info(username_lk)
        Photo_path = info_lk[4]
    return render_template('lk.html', username=username_lk, Photo_path=Photo_path)

@app.route('/game_create')
def game_create():
    username_lk = session.get('username')  # Используем безопасное извлечение
    print(username_lk)
    if username_lk:  # Если имя пользователя есть
        # users = get_users()
        info_lk = get_user_info(username_lk)
        Photo_path = info_lk[4]
    return render_template('Game_create.html', username=username_lk, Photo_path=Photo_path)


@app.route('/Game', methods=['POST'])
def game_create1():
    username_lk = session.get('username')  # Используем безопасное извлечение
    #print(username_lk)
    if username_lk:  # Если имя пользователя есть
        users = request.form['username']
        exc = request.form['except']

        inf_for_game = user_get_from_form(exc, users)
        contain_users_for_sql = inf_for_game[0]
        except_users = inf_for_game[1]
        contain_users = inf_for_game[2]
        #print(except_users)
        #print(contain_users)

        main(contain_users_for_sql, except_users, contain_users)
        info_lk = get_user_info(username_lk)
        Photo_path = info_lk[4]
    return render_template('Game_create.html', username=username_lk, Photo_path=Photo_path)

@app.route('/user/<user_id>')
def user_profile(user_id):
    username_lk = session.get('username')
    info_lk = get_user_info(username_lk)
    Photo = info_lk[4]
    if username_lk:
        username_lk = session.get('username')
        info_lk = get_user_info(username_lk)
        Photo = info_lk[4]
        user_data = get_user_profile(user_id)
        #print(user_data)
        Wish_list = user_data['Wish_url']
        Wish_list_itog = pars_link(Wish_list)
        print(Wish_list)
        if user_data:
            return render_template('success_gameCreate.html', user=user_data, Photo=Photo, username=username_lk,Wish_list_itog=Wish_list_itog )
        else:
            return "User not found", 404

@app.route('/user/wall/<user_id>')
def user_profile_wall(user_id):
    username_lk = session.get('username')
    info_lk = get_user_info(username_lk)
    Photo = info_lk[4]
    if username_lk:
        username_lk = session.get('username')
        info_lk = get_user_info(username_lk)
        Photo = info_lk[4]
        user_data = get_user_profile(user_id)
        print(user_data)
        if user_data:
            return render_template('Wall.html', user=user_data, Photo=Photo, username=username_lk)
        else:
            return "User not found", 404

def check_password():
    username = request.form.get('username')
    password = request.form.get('password')
    #hashed = hash_password(password)
    #print(hashed)
    # подключение к базе данных
    conn = mysql.connector.connect(**connection_config)

    # создание объекта cursor
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users_pasport_new WHERE Login = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    global identity
    identity = username
    TrueFalse_password = check_password_hashed(password, user[3])
    if user and TrueFalse_password: #user[3] == password:
        session['username'] = username
        return redirect('/lk')
    else:
        return redirect('/error')

def post_def():
    if request.method == 'POST':
        check_password()
    return check_password()

def registration():
    username = str(request.form.get('username'))
    password = str(request.form.get('password'))
    mail = str(request.form.get('mail'))
    fullname = str(request.form.get('fullname'))
    confirmpassword = str(request.form.get('confirmpassword'))

    if registration_check(username, password, mail, confirmpassword) == 'Success':
        conn = mysql.connector.connect(**connection_config)

        command = f"cp /home/Serg0239/mysite/static/usersphoto/standartuserphoto.jpg /home/Serg0239/mysite/static/usersphoto/{username}.jpg"
        process = subprocess.run(command, shell=True, text=True, capture_output=True)

        command1 = f"cp /home/Serg0239/mysite/static/userslinks/link.txt /home/Serg0239/mysite/static/userslinks/{username}.txt"
        process1 = subprocess.run(command1, shell=True, text=True, capture_output=True)


        password = hash_password(password)
        print(password)
        cursor1 = conn.cursor()
        test = f'INSERT INTO Users_pasport_new (Login, Email, Password) VALUES ("{username}", "{mail}", "{password}")'
        print(test)
        cursor1.execute(test)
        conn.commit()
        cursor1.execute("CALL UpdateUserInfoIdByLogin(%s)", (username,))
        conn.commit()
        cursor1.execute(f'INSERT INTO Users_info (UserName,FullName,Wish,Wish_url,Photo_path,Discription) VALUES ("{username}", "None", "None", "/home/Serg0239/mysite/static/userslinks/{username}.txt", "https://serg0239.pythonanywhere.com/static/usersphoto/{username}.jpg", "None")')
        conn.commit()
        cursor1.execute(f"UPDATE Users_pasport_new SET Users_info_ID = (select UserID from Users_info where UserName = '{username}') where Login = '{username}'")
        conn.commit()
        cursor1.close()
        conn.close()

        return redirect('/')
    else:
        return redirect('/error')

def registration_check(username, password, mail, confirmpassword):
    exception = []
    mail_list = ['@yandex.ru','@mail.ru','@bk.ru','@gmail.com']

    conn = mysql.connector.connect(**connection_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users_pasport_new WHERE Login = %s", (username,))
    user_inf = cursor.fetchone()

    if mail != '' and mail_list_def(mail, mail_list):
        if user_inf is None:
            if len(password) >= 8 and password == confirmpassword:
                status = 'Success'
                return status
            else:
                status = 'Code 403.Error. Invalid Password.'
                return status
        else:
            status = 'Code 401.Error. Invalid Username.'
            return status
    else:
        status = 'Code 402.Error. Invalid Mail.'
        return status

def mail_list_def(str_, mail_list):
    for mail in mail_list:
        if mail.lower() in str_.lower():
            return True
    return False

def registr_def():
    if request.method == 'POST':
        registration()
    return registration()

def get_user_info(username):
    conn = mysql.connector.connect(**connection_config)
    cursor = conn.cursor()
    cursor.execute("CALL GetUserInfo(%s)", (username,))
    user_inf_lk = cursor.fetchone()
    cursor.close()
    conn.close()
    return user_inf_lk
#################################################################################
def user_get_from_form(exc, users):
    """
    Обрабатывает входные данные для списка исключений и пользователей.
    """
    list_users = users.split(',')  # Список пользователей
    placeholders = ', '.join(['%s'] * len(list_users))

    if not exc:  # Если список исключений пуст
        return placeholders, None, sorted(list_users)  # Возвращаем список пользователей без исключений

    # Обработка исключений
    list_exc = exc.split(',')
    list_exc_tule = []

    for i in list_exc:
        a = tuple(i.split(':'))
        list_exc_tule.append(a)
    return placeholders, list_exc_tule, sorted(list_users)

def create_game():
    """Создаёт новую запись игры и возвращает GameID."""
    conn = mysql.connector.connect(**connection_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Games (CreatedAt) VALUES (NOW())")
    conn.commit()
    return cursor.lastrowid

def get_users(placeholders,contain_users):
    """Получает всех пользователей из базы данных."""
    conn = mysql.connector.connect(**connection_config)
    cursor = conn.cursor()
    querry = f"SELECT UserID, Login FROM Users_pasport_new WHERE Login IN ({placeholders})"
    cursor.execute(querry,contain_users)
    return cursor.fetchall()

def create_exclusions(game_id,except_users):
    """Получает всех пользователей из базы данных."""
    conn = mysql.connector.connect(**connection_config)
    cursor = conn.cursor()
    for except_users_rez in except_users:
        cursor.execute("SELECT UserID FROM Users_pasport_new where Login in (%s, %s)",(except_users_rez[0], except_users_rez[1]))
        get_excep_userid=cursor.fetchall()
        #print(except_users_rez[0], except_users_rez[1])
        print(get_excep_userid)
        cursor.execute("INSERT INTO Exclusions (GameID, UserID, ExcludedUserID) VALUES (%s, %s, %s)",(game_id,get_excep_userid[0][0],get_excep_userid[1][0]))
        conn.commit()
    return cursor.fetchall()

def get_exclusions(game_id):
    """Возвращает словарь исключений для текущей игры."""
    conn = mysql.connector.connect(**connection_config)
    cursor = conn.cursor()
    cursor.execute("SELECT UserID, ExcludedUserID FROM Exclusions WHERE GameID = %s", (game_id,))
    exclusions = cursor.fetchall()

    exclusion_dict = {}
    for exclusion in exclusions:
        user_id = exclusion[0]
        excluded_user_id = exclusion[1]

        if user_id not in exclusion_dict:
            exclusion_dict[user_id] = set()
        exclusion_dict[user_id].add(excluded_user_id)
    return exclusion_dict

def assign_secret_santa(users, exclusions):
    """
    Назначает каждому участнику случайного получателя с учётом исключений.
    """
    user_ids = [user[0] for user in users]
    max_attempts = 100  # Ограничиваем число попыток поиска корректного распределения

    for attempt in range(max_attempts):
        assignments = []
        available_receivers = user_ids[:]

        success = True
        for giver in user_ids:
            # Фильтруем доступных получателей
            possible_receivers = [
                uid for uid in available_receivers
                if uid != giver and uid not in exclusions.get(giver, set())
            ]

            if not possible_receivers:
                # Если нет доступных получателей, начинаем заново
                success = False
                break

            # Назначаем случайного доступного получателя
            receiver = random.choice(possible_receivers)
            assignments.append((giver, receiver))
            available_receivers.remove(receiver)  # Убираем назначенного получателя из доступных

        if success:
            return assignments  # Успешное распределение

    raise ValueError("Не удалось назначить получателей после нескольких попыток.")

def save_assignments(assignments, game_id):
    """Сохраняет результаты жеребьёвки в базе данных с GameID."""
    conn = mysql.connector.connect(**connection_config)
    cursor = conn.cursor()
    for giver_id, receiver_id in assignments:
        cursor.execute(
            "INSERT INTO Secret_Santa_Assignments (GameID, GiverID, ReceiverID) VALUES (%s, %s, %s)",
            (game_id, giver_id, receiver_id)
        )
    conn.commit()

def main(placeholders, except_users, contain_users):
    game_id = create_game()  # Создаём новую игру и получаем GameID
    users = get_users(placeholders, contain_users)

    if len(users) < 2:
        print("Недостаточно участников для игры.")
        return

    if not except_users:  # Если список исключений пустой
        print("Игра создаётся без исключений.")
        try:
            assignments = assign_secret_santa(users, {})  # Пустой словарь исключений
            save_assignments(assignments, game_id)
            print(f"Результаты игры 'Секретный Санта' для игры ID {game_id} успешно сохранены в базе данных.")
        except ValueError as e:
            print("Ошибка назначения получателей:", e)
        return

    # Если список исключений не пуст, выполняем стандартную логику
    create_exclusions(game_id, except_users)
    exclusions = get_exclusions(game_id)

    try:
        assignments = assign_secret_santa(users, exclusions)
        save_assignments(assignments, game_id)
        print(f"Результаты игры 'Секретный Санта' для игры ID {game_id} успешно сохранены в базе данных.")
    except ValueError as e:
        print("Ошибка назначения получателей:", e)
#################################################################################
def get_user_profile(user_id):
    conn = mysql.connector.connect(**connection_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users_pasport_new AS P LEFT JOIN Users_info AS U ON P.Login = U.UserName WHERE P.Login = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    return user_data
#################################################################################
def hash_password(password):
    salt = bcrypt.gensalt()  # Генерация соли
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def check_password_hashed(password, hashed):
    if isinstance(hashed, bytes):
        hashed = hashed.decode('utf-8')  # Преобразуем в строку
    if hashed.startswith("b'") and hashed.endswith("'"):
        hashed = hashed[2:-1]  # Убираем внешние кавычки и префикс b
    hashed = hashed.encode('utf-8')  # Преобразуем обратно в байт
    print(f"Password: {password}")
    print(f"Hashed password from DB: {hashed}")
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
#################################################################################
def pars_link(link_from_db):
    with open(link_from_db,'r', encoding='utf-8') as file:
        link_line = file.readline()
    full_list_for_lk = []  # Инициализация пустого списка, чтобы избежать ошибок с неопределённой переменной
    try:
        if 'Введи ссылку в формате' in link_line or not link_line or 'None' in link_line:
            # Обработка строки, если она не содержит указанных слов
            link_line_lk = link_line[24:]  # Обрезаем строку, начиная с 24-го символа
            list_link = link_line_lk.split('$')  # Разбиваем по символу '$'
            full_list_for_lk.append(list_link)
            print(list_link)
        else:
            # Обработка строки с удалением пробелов и делением по запятым
            text_without_whitespace = re.sub(r"\s+", "", link_line)  # Удаляем пробелы
            list_link = text_without_whitespace.split(',')  # Разбиваем по запятым
            print(list_link)

            # Создаём список кортежей из обработанных ссылок
            for link in list_link:
                new_link = link.split('$')  # Разбиваем по символу '$'
                full_list_for_lk.append(tuple(new_link))
            print(full_list_for_lk)

    except Exception as e:  # Ловим любые исключения
        print("Ошибка: формат ввода ссылки нарушен.", e)

    # Возвращаем итоговый список, даже если он пустой
    return full_list_for_lk
#################################################################################
if __name__ == '__main__':
    app.run()
