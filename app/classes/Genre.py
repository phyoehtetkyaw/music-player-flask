from flask import render_template, request, redirect
from flask.views import View
import datetime

from .DB import DB

class Genre(View):
    @staticmethod
    def index():
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

        return render_template("admin/genres/index.html", genres=genres, len=len(genres))
    
    @staticmethod
    def create():
        return render_template("admin/genres/create.html")
    
    @staticmethod
    def store():
        name = request.form.get("name")
        created_at = datetime.datetime.now()

        conn = DB.connect_db()
        conn.cursor()
        sql = "INSERT INTO `tbl_genres` (`name`, `created_at`) VALUES (?, ?)"
        conn.execute(sql, (name, created_at))
        conn.commit()

        return redirect("/admin/genres")
    
    @staticmethod
    def edit():
        id = request.args.get("id")

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_genres` WHERE `id`=?"
        res = conn.execute(sql, (id))

        raw = res.fetchone()
        genre = {
            "id": raw[0],
            "name": raw[1]
        }

        return render_template("admin/genres/edit.html", genre=genre)
    
    @staticmethod
    def update():
        id = request.args.get("id")
        name = request.form.get("name")
        updated_at = datetime.datetime.now()

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_genres` SET `name`=?, `updated_at`=? WHERE `id`=?"
        conn.execute(sql, (name, updated_at, id))
        conn.commit()

        return redirect("/admin/genres")
    
    @staticmethod
    def delete():
        id = request.args.get("id")
        deleted_at = datetime.datetime.now()

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_genres` SET `deleted_at`=? WHERE `id`=?"
        conn.execute(sql, (deleted_at, id))
        conn.commit()

        return redirect("/admin/genres")