from flask import render_template, request, redirect, session
import datetime, os
from werkzeug.utils import secure_filename

from .DB import DB

class Event:
    @staticmethod
    def index():
        events = []

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_events` WHERE `deleted_at` IS NULL ORDER BY `id` DESC"
        res = conn.execute(sql)
        
        for row in res.fetchall():
            events.append({
                "id": row[0],
                "title": row[1],
                "location": row[2],
                "description": row[3],
                "banner": row[4],
                "start_datetime": row[5],
            })

        conn.close()

        return render_template("admin/events/index.html", events=events, len=len(events))
    
    @staticmethod
    def create():
        return render_template("admin/events/create.html")
    
    @staticmethod
    def store():
        title = request.form.get("title")
        location = request.form.get("location")
        description = request.form.get("description")
        banner = request.files.get("banner")
        start_datetime = request.form.get("start_datetime")
        created_at = datetime.datetime.now()

        if title == "":
            session["event_title_error"] = "Title is required!"
            return redirect("/admin/events/create")
        
        if location == "":
            session["event_location_error"] = "Location is required!"
            return redirect("/admin/events/create")
        
        if banner.filename == "":
            session["event_banner_error"] = "Banner is required!"
            return redirect("/admin/events/create")
        
        if description == "":
            session["event_description_error"] = "Description is required!"
            return redirect("/admin/events/create")
        
        if start_datetime == "":
            session["event_start_datetime_error"] = "Start datetime is required!"
            return redirect("/admin/events/create")
        
        directory = "static/upload/events/"
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        timestamp = str(datetime.datetime.now().timestamp()).split(".")[0]
        banner_name = f"{timestamp}_{secure_filename(banner.filename)}"
        banner.save(os.path.join(directory, banner_name))

        conn = DB.connect_db()
        conn.cursor()
        sql = "INSERT INTO `tbl_events` (`title`, `location`, `banner`, `description`, `start_datetime`, `created_at`) VALUES (?, ?, ?, ?, ?, ?)"
        conn.execute(sql, (title, location, banner_name, description, start_datetime, created_at))
        conn.commit()
        conn.close()

        return redirect("/admin/events")
    
    @staticmethod
    def edit(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/events")

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_events` WHERE `id`=?"
        res = conn.execute(sql, (id))

        raw = res.fetchone()
        events = {
            "id": raw[0],
            "title": raw[1],
            "location": raw[2],
            "description": raw[3],
            "banner": raw[4],
            "start_datetime": raw[5],
        }
        conn.close()
        print(events)

        return render_template("admin/events/edit.html", events=events)
    
    @staticmethod
    def update(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/events")
        
        title = request.form.get("title")
        location = request.form.get("location")
        description = request.form.get("description")
        banner = request.files.get("banner")
        start_datetime = request.form.get("start_datetime")
        updated_at = datetime.datetime.now()

        if title == "":
            session["event_title_error"] = "Title is required!"
            return redirect(f"/admin/events/edit/{id}")
        
        if location == "":
            session["event_location_error"] = "Location is required!"
            return redirect(f"/admin/events/edit/{id}")
        
        if description == "":
            session["event_description_error"] = "Description is required!"
            return redirect(f"/admin/events/edit/{id}")
        
        if start_datetime == "":
            session["event_start_datetime_error"] = "Start datetime is required!"
            return redirect(f"/admin/events/edit/{id}")

        conn = DB.connect_db()
        conn.cursor()
        
        if banner.filename == "":
            sql = "UPDATE `tbl_events` SET `title`=?, `location`=?, `description`=?, `start_datetime`=?, `updated_at`=? WHERE `id`=?"
            conn.execute(sql, (title, location, description, start_datetime, updated_at, id)) 
        else:   
            directory = "static/upload/events/"
        
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            timestamp = str(datetime.datetime.now().timestamp()).split(".")[0]
            banner_name = f"{timestamp}_{secure_filename(banner.filename)}"
            banner.save(os.path.join(directory, banner_name))

            sql = "UPDATE `tbl_events` SET `title`=?, `location`=?, `description`=?, `banner`=?, `start_datetime`=?, `updated_at`=? WHERE `id`=?"
            conn.execute(sql, (title, location, description, banner_name, start_datetime, updated_at, id))

        conn.commit()
        conn.close()

        return redirect("/admin/events")
    
    @staticmethod
    def delete(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/events")
        
        deleted_at = datetime.datetime.now()

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_events` SET `deleted_at`=? WHERE `id`=?"
        conn.execute(sql, (deleted_at, id))
        conn.commit()
        conn.close()

        return redirect("/admin/events")