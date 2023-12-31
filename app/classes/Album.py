from flask import render_template, request, redirect, session
import datetime, os
from werkzeug.utils import secure_filename

from .DB import DB

class Album:
    @staticmethod
    def index():
        albums = []

        conn = DB.connect_db()
        conn.cursor()
        sql = """
            SELECT `tbl_albums`.*, `tbl_authors`.`name` AS `author` 
            FROM `tbl_albums` 
            JOIN `tbl_authors` ON `tbl_albums`.`author_id`=`tbl_authors`.`id`
            WHERE `tbl_albums`.`deleted_at` IS NULL
            ORDER BY `tbl_albums`.`id` DESC
        """
        res = conn.execute(sql)
        
        for row in res.fetchall():
            albums.append({
                "id": row[0],
                "title": row[1],
                "author": row[9],
                "description": row[3],
                "thumbnail": row[4],
                "price": row[5],
            })

        conn.close()

        return render_template("admin/albums/index.html", albums=albums, len=len(albums))
    
    @staticmethod
    def create():
        authors = []

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_authors` WHERE `deleted_at` IS NULL ORDER BY `id` DESC"
        res = conn.execute(sql)
        
        for row in res.fetchall():
            authors.append({
                "id": row[0],
                "name": row[1]
            })

        conn.close()
        return render_template("admin/albums/create.html", authors=authors, len=len(authors))
    
    @staticmethod
    def store():
        title = request.form.get("title")
        author_id = request.form.get("author")
        thumbnail = request.files.get("thumbnail")
        description = request.form.get("description")
        price = request.form.get("price")
        created_at = datetime.datetime.now()

        if title == "":
            session["album_title_error"] = "Title is required!"
            return redirect("/admin/albums/create")
        
        if author_id == "":
            session["album_author_error"] = "Author is required!"
            return redirect("/admin/albums/create")
        
        if thumbnail.filename == "":
            session["album_thumbnail_error"] = "Thumbnail is required!"
            return redirect("/admin/albums/create")
        
        if description == "":
            session["album_description_error"] = "Description is required!"
            return redirect("/admin/albums/create")
        
        if price == "":
            session["album_price_error"] = "Price is required!"
            return redirect("/admin/albums/create")
        
        thumbnail_name = secure_filename(thumbnail.filename)
        thumbnail.save(os.path.join("static/upload/albums/", thumbnail_name))

        conn = DB.connect_db()
        conn.cursor()
        sql = "INSERT INTO `tbl_albums` (`title`, `author_id`, `thumbnail`, `description`, `price`, `created_at`) VALUES (?, ?, ?, ?, ?, ?)"
        conn.execute(sql, (title, author_id, thumbnail_name, description, price, created_at))
        conn.commit()
        conn.close()

        return redirect("/admin/albums")
    
    @staticmethod
    def edit(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/albums")

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_albums` WHERE `id`=?"
        res = conn.execute(sql, (id))

        raw = res.fetchone()
        albums = {
            "id": raw[0],
            "title": raw[1],
            "author_id": raw[2],
            "thumbnail": raw[3],
            "description": raw[4],
            "price": raw[5]
        }

        authors = []
        sql = "SELECT * FROM `tbl_authors` WHERE `deleted_at` IS NULL ORDER BY `id` DESC"
        res = conn.execute(sql)
        
        for row in res.fetchall():
            authors.append({
                "id": row[0],
                "name": row[1]
            })

        conn.close()

        return render_template("admin/albums/edit.html", albums=albums, authors=authors, len=len(authors))
    
    @staticmethod
    def update(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/albums")
        
        title = request.form.get("title")
        author_id = request.form.get("author")
        thumbnail = request.files.get("thumbnail")
        description = request.form.get("description")
        price = request.form.get("price")
        updated_at = datetime.datetime.now()

        if title == "":
            session["album_title_error"] = "Title is required!"
            return redirect(f"/admin/albums/edit/{id}")
        
        if author_id == "":
            session["album_author_error"] = "Author is required!"
            return redirect(f"/admin/albums/edit/{id}")
        
        if description == "":
            session["album_description_error"] = "Description is required!"
            return redirect(f"/admin/albums/edit/{id}")
        
        if price == "":
            session["album_price_error"] = "Price is required!"
            return redirect(f"/admin/albums/edit/{id}")

        conn = DB.connect_db()
        conn.cursor()
        
        if thumbnail.filename == "":
            sql = "UPDATE `tbl_albums` SET `title`=?, `author_id`=?, `description`=?, `price`=?, `updated_at`=? WHERE `id`=?"
            conn.execute(sql, (title, author_id, description, price, updated_at, id)) 
        else:   
            thumbnail_name = secure_filename(thumbnail.filename)
            thumbnail.save(os.path.join("static/upload/albums/", thumbnail_name))

            sql = "UPDATE `tbl_albums` SET `title`=?, `author_id`=?, `description`=?, `thumbnail`=?, `price`=?, `updated_at`=? WHERE `id`=?"
            conn.execute(sql, (title, author_id, description, thumbnail_name, price, updated_at, id))

        conn.commit()
        conn.close()

        return redirect("/admin/albums")
    
    @staticmethod
    def delete(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/albums")
        
        deleted_at = datetime.datetime.now()

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_albums` SET `deleted_at`=? WHERE `id`=?"
        conn.execute(sql, (deleted_at, id))
        conn.commit()
        conn.close()

        return redirect("/admin/albums")