from flask import  Flask, render_template, request, redirect, session
import secrets

from app.classes.Genre import Genre
from app.classes.Author import Author
from app.classes.Ticket import Ticket

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('admin/404.html'), 404


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin")
def admin_index():
    return render_template("admin/index.html")

# genres
app.add_url_rule('/admin/genres', "genres_index", view_func=Genre.index)
app.add_url_rule('/admin/genres/create', "genres_create", view_func=Genre.create)
app.add_url_rule('/admin/genres/store', "genres_store", methods=["POST"], view_func=Genre.store)
app.add_url_rule('/admin/genres/edit/<id>', "genres_edit", view_func=Genre.edit)
app.add_url_rule('/admin/genres/update/<id>', "genres_update", methods=["POST"], view_func=Genre.update)
app.add_url_rule('/admin/genres/delete/<id>', "genres_delete", view_func=Genre.delete)

# authors
app.add_url_rule('/admin/authors', "authors_index", view_func=Author.index)
app.add_url_rule('/admin/authors/create', "authors_create", view_func=Author.create)
app.add_url_rule('/admin/authors/store', "authors_store", methods=["POST"], view_func=Author.store)
app.add_url_rule('/admin/authors/edit/<id>', "authors_edit", view_func=Author.edit)
app.add_url_rule('/admin/authors/update/<id>', "authors_update", methods=["POST"], view_func=Author.update)
app.add_url_rule('/admin/authors/delete/<id>', "authors_delete", view_func=Author.delete)

# tickets
app.add_url_rule('/admin/tickets', "tickets_index", view_func=Ticket.index)
app.add_url_rule('/admin/tickets/create', "tickets_create", view_func=Ticket.create)
app.add_url_rule('/admin/tickets/store', "tickets_store", methods=["POST"], view_func=Ticket.store)
app.add_url_rule('/admin/tickets/edit/<id>', "tickets_edit", view_func=Ticket.edit)
app.add_url_rule('/admin/tickets/update/<id>', "tickets_update", methods=["POST"], view_func=Ticket.update)
app.add_url_rule('/admin/tickets/delete/<id>', "tickets_delete", view_func=Ticket.delete)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)