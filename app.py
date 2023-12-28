from flask import  Flask, render_template, request, redirect, jsonify
import sqlite3, datetime

app = Flask(__name__)

def connect_db():
    conn = None

    try:
        conn = sqlite3.connect("db_music.sqlite")
    except sqlite3.error as e:
        print(e)

    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin")
def admin_index():
    return render_template("admin/index.html")


@app.route("/admin/genres")
def admin_genres_index():
    genres = []

    conn = connect_db()
    conn.cursor()
    sql = "SELECT * FROM `tbl_genres` WHERE `deleted_at` IS NULL ORDER BY `id` DESC"
    res = conn.execute(sql)
    
    for row in res.fetchall():
        genres.append({
            "id": row[0],
            "name": row[1]
        })

    return render_template("admin/genres/index.html", genres=genres, len=len(genres))


@app.route("/admin/genres/create")
def admin_genres_create():
    return render_template("admin/genres/create.html")


@app.route("/admin/genres/store", methods=["POST"])
def admin_genres_store():
    name = request.form.get("name")
    created_at = datetime.datetime.now()

    conn = connect_db()
    conn.cursor()
    sql = "INSERT INTO `tbl_genres` (`name`, `created_at`) VALUES (?, ?)"
    conn.execute(sql, (name, created_at))
    conn.commit()

    return redirect("/admin/genres")


@app.route("/admin/genres/edit")
def admin_genres_edit():
    id = request.args.get("id")

    conn = connect_db()
    conn.cursor()
    sql = "SELECT * FROM `tbl_genres` WHERE `id`=?"
    res = conn.execute(sql, (id))

    raw = res.fetchone()
    genre = {
        "id": raw[0],
        "name": raw[1]
    }

    return render_template("admin/genres/edit.html", genre=genre)


@app.route("/admin/genres/update", methods=["POST"])
def admin_genres_update():
    id = request.args.get("id")
    name = request.form.get("name")
    updated_at = datetime.datetime.now()

    conn = connect_db()
    conn.cursor()
    sql = "UPDATE `tbl_genres` SET `name`=?, `updated_at`=? WHERE `id`=?"
    conn.execute(sql, (name, updated_at, id))
    conn.commit()

    return redirect("/admin/genres")


@app.route("/admin/genres/delete")
def admin_genres_delete():
    id = request.args.get("id")
    deleted_at = datetime.datetime.now()

    conn = connect_db()
    conn.cursor()
    sql = "UPDATE `tbl_genres` SET `deleted_at`=? WHERE `id`=?"
    conn.execute(sql, (deleted_at, id))
    conn.commit()

    return redirect("/admin/genres")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)