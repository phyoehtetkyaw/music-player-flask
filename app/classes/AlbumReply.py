from flask import render_template, request, redirect, session
import datetime

from .DB import DB

class AlbumReply:
    @staticmethod
    def index():
        album_replies = []

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_album_replies` WHERE `deleted_at` IS NULL ORDER BY `id` DESC"
        res = conn.execute(sql)
        
        for row in res.fetchall():
            album_replies.append({
                "id": row[0],
                "user_id": row[1],
                "album_id": row[2],
                "comment_id": row[3],
                "reply": row[4]
            })

        conn.close()

        return render_template("admin/album_replies/index.html", album_replies=album_replies, len=len(album_replies))
    
    @staticmethod
    def create():
        return render_template("admin/album_replies/create.html")
    
    @staticmethod
    def delete(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/album_replies")
        
        deleted_at = datetime.datetime.now()

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_album_replies` SET `deleted_at`=? WHERE `id`=?"
        conn.execute(sql, (deleted_at, id))
        conn.commit()
        conn.close()

        return redirect("/admin/album_replies")