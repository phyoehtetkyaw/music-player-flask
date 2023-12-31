from flask import redirect, render_template

class ClientView:
    @staticmethod
    def index():
        return render_template("index.html")
    
    @staticmethod
    def artists():
        return render_template("artists.html")
    
    @staticmethod
    def releases():
        return render_template("releases.html")
    
    @staticmethod
    def events():
        return render_template("events.html")
    
    @staticmethod
    def podcasts():
        return render_template("podcasts.html")
    
    @staticmethod
    def store():
        return render_template("store.html")
    
    @staticmethod
    def news():
        return render_template("news.html")
    
    @staticmethod
    def profile():
        return render_template("profile.html")
    
    @staticmethod
    def about():
        return render_template("about.html")
    
    @staticmethod
    def contacts():
        return render_template("contacts.html")