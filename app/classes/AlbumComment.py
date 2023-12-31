from flask import render_template, request, redirect, session
import datetime

from .DB import DB

class AlbumComment:
    @staticmethod
    def index():
        album_comments = []

        conn = DB.connect_db()
        conn.cursor()
        sql = """
            SELECT `tbl_album_comments`.*, `tbl_users`.`username`, `tbl_albums`.`title` 
            FROM `tbl_album_comments` 
            JOIN `tbl_users` ON `tbl_album_comments`.`user_id`=`tbl_users`.`id` 
            JOIN `tbl_albums` ON `tbl_album_comments`.`album_id`=`tbl_albums`.`id`  
            WHERE `tbl_album_comments`.`deleted_at` IS NULL 
            ORDER BY `tbl_album_comments`.`id` DESC
        """
        res = conn.execute(sql)
        
        for row in res.fetchall():
            album_comments.append({
                "id": row[0],
                "user": row[1],
                "album_id": row[2],
                "comment": row[3]
            })

        conn.close()

        return render_template("admin/albums/comments/index.html", album_comments=album_comments, len=len(album_comments))
    
    @staticmethod
    def create():
        return render_template("admin/albums/comments/create.html")
    
    @staticmethod
    def delete(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/albums/comments")
        
        deleted_at = datetime.datetime.now()

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_album_comments` SET `deleted_at`=? WHERE `id`=?"
        conn.execute(sql, (deleted_at, id))
        conn.commit()
        conn.close()

        return redirect("/admin/albums/comments")