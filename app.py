
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = 'blog.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/posts', methods=['GET'])
def get_posts():
    with get_db() as conn:
        posts = conn.execute('SELECT * FROM posts').fetchall()
        return jsonify([dict(post) for post in posts])

@app.route('/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    if 'title' not in data or 'content' not in data:
        abort(400, description="Missing 'title' or 'content' in request body")
    with get_db() as conn:
        cursor = conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (data['title'], data['content']))
        conn.commit()
        post_id = cursor.lastrowid
        return jsonify({'id': post_id, 'title': data['title'], 'content': data['content']}), 201

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    with get_db() as conn:
        conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        conn.commit()
        return jsonify({'message': 'Post deleted'}), 200

if __name__ == '__main__':
    init_db()
    app.run(port=5000)