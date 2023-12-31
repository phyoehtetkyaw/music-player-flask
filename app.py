from flask import  Flask, render_template, request, redirect, session
import secrets

from app.classes.Genre import Genre
from app.classes.Author import Author
from app.classes.Ticket import Ticket
from app.classes.AlbumComment import AlbumComment
from app.classes.AlbumReply import AlbumReply
from app.classes.NewsCategory import NewsCategory

from app.classes.Event import Event
from app.classes.Album import Album
from app.classes.News import News
from app.classes.Product import Product
from app.classes.Track import Track

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

# album_comments
app.add_url_rule('/admin/albums/comments', "album_comments_index", view_func=AlbumComment.index)
app.add_url_rule('/admin/albums/comments/delete/<id>', "album_comments_delete", view_func=AlbumComment.delete)

# album_replies
app.add_url_rule('/admin/albums/replies', "album_replies_index", view_func=AlbumReply.index)
app.add_url_rule('/admin/albums/replies/delete/<id>', "album_replies_delete", view_func=AlbumReply.delete)

# news_categories
app.add_url_rule('/admin/news_categories', "news_categories_index", view_func=NewsCategory.index)
app.add_url_rule('/admin/news_categories/create', "news_categories_create", view_func=NewsCategory.create)
app.add_url_rule('/admin/news_categories/store', "news_categories_store", methods=["POST"], view_func=NewsCategory.store)
app.add_url_rule('/admin/news_categories/edit/<id>', "news_categories_edit", view_func=NewsCategory.edit)
app.add_url_rule('/admin/news_categories/update/<id>', "news_categories_update", methods=["POST"], view_func=NewsCategory.update)
app.add_url_rule('/admin/news_categories/delete/<id>', "news_categories_delete", view_func=NewsCategory.delete)

# events
app.add_url_rule('/admin/events', "events_index", view_func=Event.index)
app.add_url_rule('/admin/events/create', "events_create", view_func=Event.create)
app.add_url_rule('/admin/events/store', "events_store", methods=["POST"], view_func=Event.store)
app.add_url_rule('/admin/events/edit/<id>', "events_edit", view_func=Event.edit)
app.add_url_rule('/admin/events/update/<id>', "events_update", methods=["POST"], view_func=Event.update)
app.add_url_rule('/admin/events/delete/<id>', "events_delete", view_func=Event.delete)

# albums
app.add_url_rule('/admin/albums', "albums_index", view_func=Album.index)
app.add_url_rule('/admin/albums/create', "albums_create", view_func=Album.create)
app.add_url_rule('/admin/albums/store', "albums_store", methods=["POST"], view_func=Album.store)
app.add_url_rule('/admin/albums/edit/<id>', "albums_edit", view_func=Album.edit)
app.add_url_rule('/admin/albums/update/<id>', "albums_update", methods=["POST"], view_func=Album.update)
app.add_url_rule('/admin/albums/delete/<id>', "albums_delete", view_func=Album.delete)

# news
app.add_url_rule('/admin/news', "news_index", view_func=News.index)
app.add_url_rule('/admin/news/create', "news_create", view_func=News.create)
app.add_url_rule('/admin/news/store', "news_store", methods=["POST"], view_func=News.store)
app.add_url_rule('/admin/news/edit/<id>', "news_edit", view_func=News.edit)
app.add_url_rule('/admin/news/update/<id>', "news_update", methods=["POST"], view_func=News.update)
app.add_url_rule('/admin/news/delete/<id>', "news_delete", view_func=News.delete)

# products
app.add_url_rule('/admin/products', "products_index", view_func=Product.index)
app.add_url_rule('/admin/products/create', "products_create", view_func=Product.create)
app.add_url_rule('/admin/products/store', "products_store", methods=["POST"], view_func=Product.store)
app.add_url_rule('/admin/products/edit/<id>', "products_edit", view_func=Product.edit)
app.add_url_rule('/admin/products/update/<id>', "products_update", methods=["POST"], view_func=Product.update)
app.add_url_rule('/admin/products/delete/<id>', "products_delete", view_func=Product.delete)

# tracks
app.add_url_rule('/admin/tracks', "tracks_index", view_func=Track.index)
app.add_url_rule('/admin/tracks/create', "tracks_create", view_func=Track.create)
app.add_url_rule('/admin/tracks/store', "tracks_store", methods=["POST"], view_func=Track.store)
app.add_url_rule('/admin/tracks/edit/<id>', "tracks_edit", view_func=Track.edit)
app.add_url_rule('/admin/tracks/update/<id>', "tracks_update", methods=["POST"], view_func=Track.update)
app.add_url_rule('/admin/tracks/delete/<id>', "tracks_delete", view_func=Track.delete)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)