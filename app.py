from flask import  Flask, render_template, request, redirect, jsonify
import sqlite3, datetime, os
from werkzeug.utils import secure_filename

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

    conn.close()

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
    conn.close()

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
    conn.close()

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
    conn.close()

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
    conn.close()

    return redirect("/admin/genres")


# main branch
@app.route("/admin/authors")
def admin_authors_index():
    authors = []

    conn = connect_db()
    conn.cursor()
    sql = "SELECT * FROM `tbl_authors` WHERE `deleted_at` IS NULL ORDER BY `id` DESC"
    res = conn.execute(sql)
    
    for row in res.fetchall():
        authors.append({
            "id": row[0],
            "name": row[1],
            "image": row[2],
            "bio": row[3],
            "description": row[4],
            "genre_id": row[5],
            "created_at": row[6]
        })

    conn.close()
    return render_template("admin/authors/index.html", authors=authors, len=len(authors))


@app.route("/admin/authors/create")
def admin_authors_create():
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

    conn.close()
    return render_template("admin/authors/create.html", genres=genres, genres_len=len(genres))


@app.route("/admin/authors/store", methods=["POST"])
def admin_authors_store():
    name = request.form.get("name")
    image = request.files.get("image")
    bio = request.form.get("bio")
    description = request.form.get("description")
    genre_id = request.form.get("genre")
    created_at = datetime.datetime.now()
    print(created_at)

    image_name = secure_filename(image.filename)
    image.save(os.path.join("storage/authors/", image_name))

    conn = connect_db()
    conn.cursor()
    sql = "INSERT INTO `tbl_authors` (`name`, `image`, `bio`, `description`, `genre_id`, `created_at`) VALUES (?, ?, ?, ?, ?, ?)"
    conn.execute(sql, (name, image_name, bio, description, genre_id, created_at))
    conn.commit()
    conn.close()

    return redirect("/admin/authors")


@app.route("/admin/authors/edit")
def admin_authors_edit():
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

    conn.close()

    return render_template("admin/authors/edit.html", genre=genre)


@app.route("/admin/authors/update", methods=["POST"])
def admin_authors_update():
    id = request.args.get("id")
    name = request.form.get("name")
    updated_at = datetime.datetime.now()

    conn = connect_db()
    conn.cursor()
    sql = "UPDATE `tbl_genres` SET `name`=?, `updated_at`=? WHERE `id`=?"
    conn.execute(sql, (name, updated_at, id))
    conn.commit()
    conn.close()

    return redirect("/admin/authors")


@app.route("/admin/authors/delete")
def admin_authors_delete():
    id = request.args.get("id")
    deleted_at = datetime.datetime.now()

    conn = connect_db()
    conn.cursor()
    sql = "UPDATE `tbl_authors` SET `deleted_at`=? WHERE `id`=?"
    conn.execute(sql, (deleted_at, id))
    conn.commit()
    conn.close()

    return redirect("/admin/authors")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)