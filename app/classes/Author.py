from flask import render_template, request, redirect, session
import datetime, os
from werkzeug.utils import secure_filename

from .DB import DB

class Author:
    @staticmethod
    def index():
        authors = []

        conn = DB.connect_db()
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
    
    @staticmethod
    def create():
        genres = []

        conn = DB.connect_db()
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
    
    @staticmethod
    def store():
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

        directory = "static/upload/authors/"
        
        if not os.path.exists(directory):
            os.makedirs(directory)

        timestamp = str(datetime.datetime.now().timestamp()).split(".")[0]
        image_name = f"{timestamp}_{secure_filename(image.filename)}"
        image.save(os.path.join(directory, image_name))

        conn = DB.connect_db()
        conn.cursor()
        sql = "INSERT INTO `tbl_authors` (`name`, `image`, `bio`, `description`, `genre_id`, `created_at`) VALUES (?, ?, ?, ?, ?, ?)"
        conn.execute(sql, (name, image_name, bio, description, genre_id, created_at))
        conn.commit()
        conn.close()

        return redirect("/admin/authors")
    
    @staticmethod
    def edit(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/authors")
        
        genres = []

        conn = DB.connect_db()
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
    
    @staticmethod
    def update(id):
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

        conn = DB.connect_db()
        conn.cursor()

        if image.filename == "":
            sql = "UPDATE `tbl_authors` SET `name`=?, `bio`=?, `description`=?, `genre_id`=?, `updated_at`=? WHERE `id`=?"
            conn.execute(sql, (name, bio, description, genre_id, updated_at, id)) 
        else:   
            directory = "static/upload/authors/"
        
            if not os.path.exists(directory):
                os.makedirs(directory)

            timestamp = str(datetime.datetime.now().timestamp()).split(".")[0]
            image_name = f"{timestamp}_{secure_filename(image.filename)}"
            image.save(os.path.join(directory, image_name))

            sql = "UPDATE `tbl_authors` SET `name`=?, `image`=?, `bio`=?, `description`=?, `genre_id`=?, `updated_at`=? WHERE `id`=?"
            conn.execute(sql, (name, image_name, bio, description, genre_id, updated_at, id))

        conn.commit()
        conn.close()

        return redirect("/admin/authors")
    
    @staticmethod
    def delete(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/authors")
        
        deleted_at = datetime.datetime.now()

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_authors` SET `deleted_at`=? WHERE `id`=?"
        conn.execute(sql, (deleted_at, id))
        conn.commit()
        conn.close()

        return redirect("/admin/authors")