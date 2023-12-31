from flask import render_template, request, redirect, session
import datetime

from .DB import DB

class NewsComment:
    @staticmethod
    def index():
        news_comments = []

        conn = DB.connect_db()
        conn.cursor()
        sql = """
            SELECT `tbl_news_comments`.*, `tbl_users`.`username`, `tbl_news`.`title` 
            FROM `tbl_news_comments` 
            JOIN `tbl_users` ON `tbl_news_comments`.`user_id`=`tbl_users`.`id` 
            JOIN `tbl_news` ON `tbl_news_comments`.`news_id`=`tbl_news`.`id`  
            WHERE `tbl_news_comments`.`deleted_at` IS NULL 
            ORDER BY `tbl_news_comments`.`id` DESC
        """
        res = conn.execute(sql)
        
        for row in res.fetchall():
            news_comments.append({
                "id": row[0],
                "user": row[1],
                "news": row[2],
                "comment": row[3]
            })

        conn.close()

        return render_template("admin/news/comments/index.html", news_comments=news_comments, len=len(news_comments))
    
    @staticmethod
    def create():
        return render_template("admin/news/comments/create.html")
    
    @staticmethod
    def delete(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/news/comments")
        
        deleted_at = datetime.datetime.now()

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_news_comments` SET `deleted_at`=? WHERE `id`=?"
        conn.execute(sql, (deleted_at, id))
        conn.commit()
        conn.close()

        return redirect("/admin/news/comments")