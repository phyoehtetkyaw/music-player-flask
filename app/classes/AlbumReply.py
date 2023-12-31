from flask import render_template, request, redirect, session
import datetime

from .DB import DB

class AlbumReply:
    @staticmethod
    def index():
        album_replies = []

        conn = DB.connect_db()
        conn.cursor()
        sql = """
            SELECT `tbl_album_replies`.*, `tbl_users`.`username`, `tbl_albums`.`title`, `tbl_album_comments`.`comment`
            FROM `tbl_album_replies` 
            JOIN `tbl_users` ON `tbl_album_replies`.`user_id`=`tbl_users`.`id` 
            JOIN `tbl_albums` ON `tbl_album_replies`.`album_id`=`tbl_albums`.`id`  
            JOIN `tbl_album_comments` ON `tbl_album_replies`.`comment_id`=`tbl_album_comments`.`id`  
            WHERE `tbl_album_replies`.`deleted_at` IS NULL 
            ORDER BY `tbl_album_replies`.`id` DESC
        """
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

        return render_template("admin/albums/replies/index.html", album_replies=album_replies, len=len(album_replies))
    
    @staticmethod
    def create():
        return render_template("admin/albums/replies/create.html")
    
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

        return redirect("/admin/albums/replies")