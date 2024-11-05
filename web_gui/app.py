from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

DATABASE = {
    'dbname': 'torg_firm',
    'user': 'postgres',
    'password': 'postgres',
    'host': '127.0.0.1',
    'port': '5432'
}

def db_connect():
    return psycopg2.connect(**DATABASE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load_data', methods=['POST'])
def load_data():
    table = request.json.get('table')
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(f'SELECT * FROM "{table}"')
            rows = cur.fetchall()
    return jsonify(rows)

@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.json.get('data')
    table = request.json.get('table')
    placeholders = ', '.join(['%s'] * len(data))
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(f'INSERT INTO "{table}" VALUES ({placeholders})', data)
            conn.commit()
    return jsonify(success=True)

@app.route('/delete_record', methods=['POST'])
def delete_record():
    table = request.json.get('table')
    record_id = request.json.get('id')  # получаем ID записи из запроса

    with db_connect() as conn:
        with conn.cursor() as cur:
            # Попробуем удалить запись с нужным ID
            cur.execute(f'DELETE FROM "{table}" WHERE id = %s', (record_id,))
            conn.commit()
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
