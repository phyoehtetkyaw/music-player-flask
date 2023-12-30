from flask import render_template, request, redirect, session
import datetime

from .DB import DB

class NewsCategory:
    @staticmethod
    def index():
        news_categories = []

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_news_categories` WHERE `deleted_at` IS NULL ORDER BY `id` DESC"
        res = conn.execute(sql)
        
        for row in res.fetchall():
            news_categories.append({
                "id": row[0],
                "name": row[1]
            })

        conn.close()

        return render_template("admin/news_categories/index.html", news_categories=news_categories, len=len(news_categories))
    
    @staticmethod
    def create():
        return render_template("admin/news_categories/create.html")
    
    @staticmethod
    def store():
        name = request.form.get("name")
        created_at = datetime.datetime.now()

        if name == "":
            session["categories_name_error"] = "Name is required!"
            return redirect("/admin/news_categories/create")

        conn = DB.connect_db()
        conn.cursor()
        sql = "INSERT INTO `tbl_news_categories` (`name`, `created_at`) VALUES (?, ?)"
        conn.execute(sql, (name, created_at))
        conn.commit()
        conn.close()

        return redirect("/admin/news_categories")
    
    @staticmethod
    def edit(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/news_categories")

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_news_categories` WHERE `id`=?"
        res = conn.execute(sql, (id))

        raw = res.fetchone()
        category = {
            "id": raw[0],
            "name": raw[1]
        }
        conn.close()

        return render_template("admin/news_categories/edit.html", category=category)
    
    @staticmethod
    def update(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/news_categories")
        
        name = request.form.get("name")
        updated_at = datetime.datetime.now()

        if name == "":
            session["categories_name_error"] = "Name is required!"
            return redirect(f"/admin/news_categories/edit/{id}")

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_news_categories` SET `name`=?, `updated_at`=? WHERE `id`=?"
        conn.execute(sql, (name, updated_at, id))
        conn.commit()
        conn.close()

        return redirect("/admin/news_categories")
    
    @staticmethod
    def delete(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/news_categories")
        
        deleted_at = datetime.datetime.now()

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_news_categories` SET `deleted_at`=? WHERE `id`=?"
        conn.execute(sql, (deleted_at, id))
        conn.commit()
        conn.close()

        return redirect("/admin/news_categories")