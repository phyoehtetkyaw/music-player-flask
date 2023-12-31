from flask import render_template, request, redirect, session
import datetime, os
from werkzeug.utils import secure_filename

from .DB import DB

class Track:
    @staticmethod
    def index():
        tracks = []

        conn = DB.connect_db()
        conn.cursor()
        sql = """
            SELECT `tbl_tracks`.*, `tbl_authors`.`name` AS `author`, `tbl_albums`.`title` AS `album`
            FROM `tbl_tracks` 
            JOIN `tbl_authors` ON `tbl_tracks`.`author_id`=`tbl_authors`.`id`
            JOIN `tbl_albums` ON `tbl_tracks`.`album_id`=`tbl_albums`.`id`
            WHERE `tbl_tracks`.`deleted_at` IS NULL 
            ORDER BY `tbl_tracks`.`id` DESC
        """
        res = conn.execute(sql)
        
        for row in res.fetchall():
            tracks.append({
                "id": row[0],
                "title": row[1],
                "album": row[9],
                "author": row[8],
                "track": row[4],
            })

        conn.close()

        return render_template("admin/tracks/index.html", tracks=tracks, len=len(tracks))
    
    @staticmethod
    def create():
        authors = []
        albums = []

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_authors` WHERE `deleted_at` IS NULL ORDER BY `id` DESC"
        res = conn.execute(sql)
        
        for row in res.fetchall():
            authors.append({
                "id": row[0],
                "name": row[1]
            })

        sql = "SELECT * FROM `tbl_albums` WHERE `deleted_at` IS NULL ORDER BY `id` DESC"
        res = conn.execute(sql)
        
        for row in res.fetchall():
            albums.append({
                "id": row[0],
                "name": row[1]
            })

        conn.close()
        return render_template("admin/tracks/create.html", albums=albums, albums_len=len(albums), authors=authors, authors_len=len(authors))
    
    @staticmethod
    def store():
        title = request.form.get("title")
        author_id = request.form.get("author")
        album_id = request.form.get("album")
        audio = request.files.get("audio")
        created_at = datetime.datetime.now()

        if title == "":
            session["track_title_error"] = "Title is required!"
            return redirect("/admin/tracks/create")
        
        if author_id == "":
            session["track_author_error"] = "Author is required!"
            return redirect("/admin/tracks/create")
        
        if album_id == "":
            session["track_album_error"] = "Album is required!"
            return redirect("/admin/tracks/create")
        
        if audio.filename == "":
            session["track_audio_error"] = "Audio File is required!"
            return redirect("/admin/tracks/create")
        
        audio_name = secure_filename(audio.filename)
        audio.save(os.path.join("static/upload/tracks/", audio_name))

        conn = DB.connect_db()
        conn.cursor()
        sql = "INSERT INTO `tbl_tracks` (`title`, `author_id`, `album_id`, `audio`, `created_at`) VALUES (?, ?, ?, ?, ?)"
        conn.execute(sql, (title, author_id, album_id, audio_name, created_at))
        conn.commit()
        conn.close()

        return redirect("/admin/tracks")
    
    @staticmethod
    def edit(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/tracks")

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_tracks` WHERE `id`=?"
        res = conn.execute(sql, (id))

        raw = res.fetchone()
        tracks = {
            "id": raw[0],
            "title": raw[1],
            "author_id": raw[2],
            "album_id": raw[3],
            "track": raw[4],
        }

        authors = []
        albums = []

        sql = "SELECT * FROM `tbl_authors` WHERE `deleted_at` IS NULL ORDER BY `id` DESC"
        res = conn.execute(sql)
        
        for row in res.fetchall():
            authors.append({
                "id": row[0],
                "name": row[1]
            })

        sql = "SELECT * FROM `tbl_albums` WHERE `deleted_at` IS NULL ORDER BY `id` DESC"
        res = conn.execute(sql)
        
        for row in res.fetchall():
            albums.append({
                "id": row[0],
                "name": row[1]
            })

        conn.close()

        return render_template("admin/tracks/edit.html", tracks=tracks, albums=albums, albums_len=len(albums), authors=authors, authors_len=len(authors))
    
    @staticmethod
    def update(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/tracks")
        
        title = request.form.get("title")
        author_id = request.form.get("author")
        album_id = request.form.get("album")
        audio = request.files.get("audio")
        updated_at = datetime.datetime.now()

        if title == "":
            session["track_title_error"] = "Title is required!"
            return redirect(f"/admin/tracks/edit/{id}")
        
        if author_id == "":
            session["track_author_error"] = "Author is required!"
            return redirect(f"/admin/tracks/edit/{id}")
        
        if album_id == "":
            session["track_album_error"] = "Album is required!"
            return redirect(f"/admin/tracks/edit/{id}")

        conn = DB.connect_db()
        conn.cursor()
        
        if audio.filename == "":
            sql = "UPDATE `tbl_tracks` SET `title`=?, `author_id`=?, `album_id`=?, `updated_at`=? WHERE `id`=?"
            conn.execute(sql, (title, author_id, album_id, updated_at, id)) 
        else:   
            audio_name = secure_filename(audio.filename)
            audio.save(os.path.join("static/upload/tracks/", audio_name))

            sql = "UPDATE `tbl_tracks` SET `title`=?, `author_id`=?, `album_id`=?, `audio`=? `updated_at`=? WHERE `id`=?"
            conn.execute(sql, (title, author_id, album_id, audio, updated_at, id))

        conn.commit()
        conn.close()

        return redirect("/admin/tracks")
    
    @staticmethod
    def delete(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/tracks")
        
        deleted_at = datetime.datetime.now()

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_tracks` SET `deleted_at`=? WHERE `id`=?"
        conn.execute(sql, (deleted_at, id))
        conn.commit()
        conn.close()

        return redirect("/admin/tracks")