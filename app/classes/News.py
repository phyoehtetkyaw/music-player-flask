from flask import render_template, request, redirect, session
import datetime, os
from werkzeug.utils import secure_filename

from .DB import DB

class News:
    @staticmethod
    def index():
        news = []

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_news` WHERE `deleted_at` IS NULL ORDER BY `id` DESC"
        res = conn.execute(sql)
        
        for row in res.fetchall():
            news.append({
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "image": row[3],
            })

        conn.close()

        return render_template("admin/news/index.html", news=news, len=len(news))
    
    @staticmethod
    def create():
        return render_template("admin/news/create.html")
    
    @staticmethod
    def store():
        title = request.form.get("title")
        description = request.form.get("description")
        image = request.files.get("image")
        created_at = datetime.datetime.now()

        if title == "":
            session["news_title_error"] = "Title is required!"
            return redirect("/admin/news/create")
        
        if image.filename == "":
            session["news_image_error"] = "Image is required!"
            return redirect("/admin/news/create")
        
        if description == "":
            session["news_description_error"] = "Description is required!"
            return redirect("/admin/news/create")
        
        image_name = secure_filename(image.filename)
        image.save(os.path.join("static/upload/news/", image_name))

        conn = DB.connect_db()
        conn.cursor()
        sql = "INSERT INTO `tbl_news` (`title`, `description`, `image`, `created_at`) VALUES (?, ?, ?, ?)"
        conn.execute(sql, (title, description, image_name, created_at))
        conn.commit()
        conn.close()

        return redirect("/admin/news")
    
    @staticmethod
    def edit(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/news")

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_news` WHERE `id`=?"
        res = conn.execute(sql, (id))

        raw = res.fetchone()
        news = {
            "id": raw[0],
            "title": raw[1],
            "description": raw[2],
            "image": raw[3],
        }
        conn.close()
        print(news)

        return render_template("admin/news/edit.html", news=news)
    
    @staticmethod
    def update(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/news")
        
        title = request.form.get("title")
        description = request.form.get("description")
        image = request.files.get("image")
        updated_at = datetime.datetime.now()

        if title == "":
            session["news_title_error"] = "Title is required!"
            return redirect(f"/admin/news/edit/{id}")
        
        if description == "":
            session["news_description_error"] = "Description is required!"
            return redirect(f"/admin/news/edit/{id}")

        conn = DB.connect_db()
        conn.cursor()
        
        if image.filename == "":
            sql = "UPDATE `tbl_news` SET `title`=?, `description`=?, `updated_at`=? WHERE `id`=?"
            conn.execute(sql, (title, description, updated_at, id)) 
        else:   
            image_name = secure_filename(image.filename)
            image.save(os.path.join("static/upload/news/", image_name))

            sql = "UPDATE `tbl_news` SET `title`=?, `description`=?, `image`=?, `updated_at`=? WHERE `id`=?"
            conn.execute(sql, (title, description, image_name, updated_at, id))

        conn.commit()
        conn.close()

        return redirect("/admin/news")
    
    @staticmethod
    def delete(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/news")
        
        deleted_at = datetime.datetime.now()

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_news` SET `deleted_at`=? WHERE `id`=?"
        conn.execute(sql, (deleted_at, id))
        conn.commit()
        conn.close()

        return redirect("/admin/news")