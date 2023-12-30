from flask import render_template, request, redirect, session
import datetime

from .DB import DB

class Ticket:
    @staticmethod
    def index():
        tickets = []

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_tickets` WHERE `deleted_at` IS NULL ORDER BY `id` DESC"
        res = conn.execute(sql)
        
        for row in res.fetchall():
            tickets.append({
                "id": row[0],
                "ticket_type": row[1],
                "ticket_price": row[2]
            })

        conn.close()

        return render_template("admin/tickets/index.html", tickets=tickets, len=len(tickets))
    
    @staticmethod
    def create():
        return render_template("admin/tickets/create.html")
    
    @staticmethod
    def store():
        ticket_type = request.form.get("ticket_type")
        ticket_price = request.form.get("ticket_price")
        created_at = datetime.datetime.now()

        if ticket_type == "":
            session["ticket_type_error"] = "Ticket Type is required!"
            return redirect("/admin/tickets/create")

        if ticket_price == "":
            session["ticket_price_error"] = "Ticket Price is required!"
            return redirect("/admin/tickets/create")

        conn = DB.connect_db()
        conn.cursor()
        sql = "INSERT INTO `tbl_tickets` (`ticket_type`, `ticket_price`, `created_at`) VALUES (?, ?, ?)"
        conn.execute(sql, (ticket_type, ticket_price, created_at))
        conn.commit()
        conn.close()

        return redirect("/admin/tickets")
    
    @staticmethod
    def edit(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/tickets")

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_tickets` WHERE `id`=?"
        res = conn.execute(sql, (id))

        raw = res.fetchone()
        ticket = {
            "id": raw[0],
            "ticket_type": raw[1],
            "ticket_price": raw[2]
        }
        conn.close()

        return render_template("admin/tickets/edit.html", ticket=ticket)
    
    @staticmethod
    def update(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/tickets")
        
        ticket_type = request.form.get("ticket_type")
        ticket_price = request.form.get("ticket_price")
        updated_at = datetime.datetime.now()

        if ticket_type == "":
            session["ticket_type_error"] = "Ticket Type is required!"
            return redirect("/admin/tickets/create")

        if ticket_price == "":
            session["ticket_price_error"] = "Ticket Price is required!"
            return redirect("/admin/tickets/create")

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_tickets` SET `ticket_type`=?, `ticket_price`=?, `updated_at`=? WHERE `id`=?"
        conn.execute(sql, (ticket_type, ticket_price, updated_at, id))
        conn.commit()
        conn.close()

        return redirect("/admin/tickets")
    
    @staticmethod
    def delete(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/tickets")
        
        deleted_at = datetime.datetime.now()

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_tickets` SET `deleted_at`=? WHERE `id`=?"
        conn.execute(sql, (deleted_at, id))
        conn.commit()
        conn.close()

        return redirect("/admin/tickets")