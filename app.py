from flask import  Flask, render_template, request, redirect, session
import sqlite3, datetime, os, secrets
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

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

    if name == "":
        session["genre_name_error"] = "Name is required!"
        return redirect("/admin/genres/create")

    conn = connect_db()
    conn.cursor()
    sql = "INSERT INTO `tbl_genres` (`name`, `created_at`) VALUES (?, ?)"
    conn.execute(sql, (name, created_at))
    conn.commit()
    conn.close()

    return redirect("/admin/genres")


@app.route("/admin/genres/edit/<id>")
def admin_genres_edit(id):
    
    if id.isnumeric() != True or int(id) < 1:
        return redirect("/admin/genres")

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


@app.route("/admin/genres/update/<id>", methods=["POST"])
def admin_genres_update(id):

    if id.isnumeric() != True or int(id) < 1:
        return redirect("/admin/genres")
    
    name = request.form.get("name")
    updated_at = datetime.datetime.now()

    if name == "":
        session["genre_name_error"] = "Name is required!"
        return redirect(f"/admin/genres/edit/{id}")

    conn = connect_db()
    conn.cursor()
    sql = "UPDATE `tbl_genres` SET `name`=?, `updated_at`=? WHERE `id`=?"
    conn.execute(sql, (name, updated_at, id))
    conn.commit()
    conn.close()

    return redirect("/admin/genres")


@app.route("/admin/genres/delete/<id>")
def admin_genres_delete(id):

    if id.isnumeric() != True or int(id) < 1:
        return redirect("/admin/genres")
    
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
    sql = """
        SELECT `tbl_authors`.*, `tbl_genres`.`name` AS `genre` 
        FROM `tbl_authors` 
        JOIN `tbl_genres` 
        ON `tbl_authors`.`genre_id`=`tbl_genres`.`id` 
        WHERE `tbl_authors`.`deleted_at` IS NULL 
        ORDER BY `tbl_authors`.`id` DESC
    """
    res = conn.execute(sql)
    
    for row in res.fetchall():
        authors.append({
            "id": row[0],
            "name": row[1],
            "image": row[2],
            "bio": row[3],
            "description": row[4],
            "genre": row[9],
            "created_at": row[6],
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

    if name == "":
        session["author_name_error"] = "Name is required!"
        return redirect("/admin/authors/create")
    
    if image.filename == "":
        session["author_image_error"] = "Image is required!"
        return redirect("/admin/authors/create")
    
    if bio == "":
        session["author_bio_error"] = "Bio is required!"
        return redirect("/admin/authors/create")
    
    if description == "":
        session["author_description_error"] = "Description is required!"
        return redirect("/admin/authors/create")
    
    if genre_id == "":
        session["author_genreid_error"] = "Genre is required!"
        return redirect("/admin/authors/create")


    image_name = secure_filename(image.filename)
    image.save(os.path.join("static/upload/authors/", image_name))

    conn = connect_db()
    conn.cursor()
    sql = "INSERT INTO `tbl_authors` (`name`, `image`, `bio`, `description`, `genre_id`, `created_at`) VALUES (?, ?, ?, ?, ?, ?)"
    conn.execute(sql, (name, image_name, bio, description, genre_id, created_at))
    conn.commit()
    conn.close()

    return redirect("/admin/authors")


@app.route("/admin/authors/edit/<id>")
def admin_authors_edit(id):
    
    if id.isnumeric() != True or int(id) < 1:
        return redirect("/admin/authors")
    
    genres = []

    conn = connect_db()
    conn.cursor()
    sql = "SELECT * FROM `tbl_authors` WHERE `id`=?"
    res = conn.execute(sql, (id))

    raw = res.fetchone()
    authors = {
        "id": raw[0],
        "name": raw[1],
        "bio": raw[3],
        "description": raw[4],
        "genre_id": raw[5]
    }

    sql = "SELECT * FROM `tbl_genres` WHERE `deleted_at` IS NULL ORDER BY `id` DESC"
    res = conn.execute(sql)
    
    for row in res.fetchall():
        genres.append({
            "id": row[0],
            "name": row[1]
        })

    conn.close()

    return render_template("admin/authors/edit.html", authors=authors, genres=genres, genres_len=len(genres))


@app.route("/admin/authors/update/<id>", methods=["POST"])
def admin_authors_update(id):

    if id.isnumeric() != True or int(id) < 1:
        return redirect("/admin/authors")
    
    name = request.form.get("name")
    image = request.files.get("image")
    bio = request.form.get("bio")
    description = request.form.get("description")
    genre_id = request.form.get("genre")
    updated_at = datetime.datetime.now()

    if name == "":
        session["author_name_error"] = "Name is required!"
        return redirect(f"/admin/authors/edit/{id}")
    
    if bio == "":
        session["author_bio_error"] = "Bio is required!"
        return redirect(f"/admin/authors/edit/{id}")
    
    if description == "":
        session["author_description_error"] = "Description is required!"
        return redirect(f"/admin/authors/edit/{id}")
    
    if genre_id == "":
        session["author_genreid_error"] = "Genre is required!"
        return redirect(f"/admin/authors/edit/{id}")

    conn = connect_db()
    conn.cursor()

    if image.filename == "":
        sql = "UPDATE `tbl_authors` SET `name`=?, `bio`=?, `description`=?, `genre_id`=?, `updated_at`=? WHERE `id`=?"
        conn.execute(sql, (name, bio, description, genre_id, updated_at, id)) 
    else:   
        image_name = secure_filename(image.filename)
        image.save(os.path.join("static/upload/authors/", image_name))

        sql = "UPDATE `tbl_authors` SET `name`=?, `image`=?, `bio`=?, `description`=?, `genre_id`=?, `updated_at`=? WHERE `id`=?"
        conn.execute(sql, (name, image_name, bio, description, genre_id, updated_at, id))

    conn.commit()
    conn.close()

    return redirect("/admin/authors")


@app.route("/admin/authors/delete/<id>")
def admin_authors_delete(id):

    if id.isnumeric() != True or int(id) < 1:
        return redirect("/admin/authors")
    
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