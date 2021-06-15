from flask import Flask, request, jsonify
import psycopg2
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from config_db import SERVER, PORT, DATABASE, USERNAME, PASSWORD


app = Flask(__name__)
# client = app.test_client()
app.config["JWT_SECRET_KEY"] = "super-secret"   # =)
jwt = JWTManager(app)


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


@app.route('/sign_in', methods=['POST'])
def check_user():
    """
    Производится проверка имени и пароля пользователя.
    В случае успешной проверки генерируется JWT токен.
    :return: json c token формата {"token": token}
    """
    login = request.json.get('name')
    password = request.json.get('password')
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"""select * from login_password where login='{login}'""")
    row = cur.fetchone()
    if not row or row[1] != password:
        return jsonify({"msg": "Bad name or password"}), 401
    token = create_access_token(identity=login)
    return jsonify({"token": token})


# @app.route("/protected", methods=["GET"])
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200


if __name__ == '__main__':
    app.run()
