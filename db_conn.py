"""Модуль подготовки тестовых данных в БД"""

import psycopg2
from config_db import SERVER, PORT, DATABASE, USERNAME, PASSWORD


def connect_db() -> any:
    """
    Соединение с базой данных.
    :return: коннект с базой данных.
    """
    conn = psycopg2.connect(host=SERVER,
                            port=PORT,
                            database=DATABASE,
                            user=USERNAME,
                            password=PASSWORD)
    return conn


def drop_table(conn: any, table_name: str) -> str:
    """
    Удаление таблицы
    :param conn: коннект к БД
    :param table_name: название таблицы
    :return: сообщение об удалении таблицы
    """
    with conn.cursor() as cursor:
        cursor.execute(f"DROP table {table_name} CASCADE")
        conn.commit()
    return f"Таблица {table_name} удалена"


def create_db_login_pass(conn):
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE login_password (
        login varchar(20) PRIMARY KEY ,
        password varchar(20));"""
    )
    conn.commit()
    return "Таблица login_password создана"


def create_db_messages(conn):
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE messages (
        id int PRIMARY KEY,
        dt text,
        login varchar(20) references login_password(login),
        message text);"""
    )
    conn.commit()
    return "Таблица messages создана"


def add_to_login_pass(conn):
    cursor = conn.cursor()
    for i in range(11, 21):
        cursor.execute(f"insert into login_password (login, password) values ('user{i}', 'pass{i}')")
    conn.commit()
    return "Successfully added"


def add_to_messages(conn):
    cursor = conn.cursor()
    for i in range(11, 41):
        cursor.execute(f"insert into messages (dt, login, message) values ('datetime-{i}', 'user{i}', 'some text{i}')")
    conn.commit()
    return "Successfully added"


if __name__ == '__main__':
    conn = connect_db()
    drop_table(conn, "login_password")
    drop_table(conn, "messages")
    create_db_login_pass(conn)
    create_db_messages(conn)
    add_to_login_pass(conn)
    add_to_messages(conn)
    conn.close()
