from flask import render_template, request, redirect, session
import datetime

from .DB import DB

class AlbumComment:
    @staticmethod
    def index():
        album_comments = []

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_album_comments` WHERE `deleted_at` IS NULL ORDER BY `id` DESC"
        res = conn.execute(sql)
        
        for row in res.fetchall():
            album_comments.append({
                "id": row[0],
                "user_id": row[1],
                "album_id": row[2],
                "comment": row[3]
            })

        conn.close()

        return render_template("admin/album_comments/index.html", album_comments=album_comments, len=len(album_comments))
    
    @staticmethod
    def create():
        return render_template("admin/album_comments/create.html")
    
    @staticmethod
    def delete(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/album_comments")
        
        deleted_at = datetime.datetime.now()

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_album_comments` SET `deleted_at`=? WHERE `id`=?"
        conn.execute(sql, (deleted_at, id))
        conn.commit()
        conn.close()

        return redirect("/admin/album_comments")