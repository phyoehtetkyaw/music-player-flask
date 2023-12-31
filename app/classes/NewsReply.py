from flask import render_template, request, redirect, session
import datetime

from .DB import DB

class NewsReply:
    @staticmethod
    def index():
        news_replies = []

        conn = DB.connect_db()
        conn.cursor()
        sql = """
            SELECT `tbl_news_replies`.*, `tbl_users`.`username`, `tbl_news`.`title` , `tbl_news_comments`.`comment`
            FROM `tbl_news_replies` 
            JOIN `tbl_users` ON `tbl_news_replies`.`user_id`=`tbl_users`.`id` 
            JOIN `tbl_news` ON `tbl_news_replies`.`news_id`=`tbl_news`.`id`  
            JOIN `tbl_news_comments` ON `tbl_news_replies`.`comment_id`=`tbl_news_comments`.`id`  
            WHERE `tbl_news_replies`.`deleted_at` IS NULL 
            ORDER BY `tbl_news_replies`.`id` DESC
        """
        res = conn.execute(sql)
        
        for row in res.fetchall():
            news_replies.append({
                "id": row[0],
                "user": row[1],
                "news": row[2],
                "comment": row[3],
                "reply": row[4]
            })

        conn.close()

        return render_template("admin/news/replies/index.html", news_replies=news_replies, len=len(news_replies))
    
    @staticmethod
    def create():
        return render_template("admin/news/replies/create.html")
    
    @staticmethod
    def delete(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/news/replies")
        
        deleted_at = datetime.datetime.now()

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_news_replies` SET `deleted_at`=? WHERE `id`=?"
        conn.execute(sql, (deleted_at, id))
        conn.commit()
        conn.close()

        return redirect("/admin/news/replies")