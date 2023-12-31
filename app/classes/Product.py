from flask import render_template, request, redirect, session, url_for
import datetime, os
from werkzeug.utils import secure_filename

from .DB import DB

class Product:
    @staticmethod
    def index():
        products = []

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_products` WHERE `deleted_at` IS NULL ORDER BY `id` DESC"
        res = conn.execute(sql)
        
        for row in res.fetchall():
            products.append({
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": row[3],
                "instock": row[4],
                "images": Product.get_images(int(row[0]))
            })

        conn.close()

        return render_template("admin/products/index.html", products=products, len=len(products))
    
    @staticmethod
    def get_images(id:int):
        images = ""

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_product_images` WHERE `product_id`=? AND `deleted_at` IS NULL ORDER BY `id` DESC"
        res = conn.execute(sql, [id])
        
        for row in res.fetchall():
            images += f"""<img style="width: 100px;" src="{url_for('static', filename='upload/products/' + row[2])}" alt="{row[2]}">"""

        conn.close()

        return images
    
    @staticmethod
    def create():
        return render_template("admin/products/create.html")
    
    @staticmethod
    def store():
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        instock = request.form.get("instock")
        images = request.files.getlist("images") 
        created_at = datetime.datetime.now()

        if name == "":
            session["product_name_error"] = "Name is required!"
            return redirect("/admin/products/create")
        
        if description == "":
            session["product_description_error"] = "Description is required!"
            return redirect("/admin/products/create")
        
        if price == "":
            session["product_price_error"] = "Price is required!"
            return redirect("/admin/products/create")
        
        if instock == "":
            session["product_instock_error"] = "Instock is required!"
            return redirect("/admin/products/create")
        
        if len(images) > 0:
            session["product_image_error"] = "Images are required!"
            return redirect("/admin/products/create")
        
        directory = "static/upload/products/"
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        image_list = []
        for image in images:
            timestamp = str(datetime.datetime.now().timestamp()).split(".")[0]
            image_name = f"{timestamp}_{secure_filename(image.filename)}"
            image.save(os.path.join(directory, image_name))
            print(image_name)
            image_list.append(image_name)

        conn = DB.connect_db()
        conn.cursor()
        sql = "INSERT INTO `tbl_products` (`name`, `description`, `price`, `instock`, `created_at`) VALUES (?, ?, ?, ?, ?)"
        conn.execute(sql, (name, description, price, instock, created_at))
        conn.commit()

        sql = "SELECT `id` FROM `tbl_products` ORDER BY `id` DESC LIMIT 1"
        res = conn.execute(sql)
        row = res.fetchone()
        id = row[0]

        for image in image_list:
            sql = "INSERT INTO `tbl_product_images` (`product_id`, `image`, `created_at`) VALUES (?, ?, ?)"
            conn.execute(sql, (id, image, created_at))
            conn.commit()
        
        conn.close()
        
        return redirect("/admin/products")
    
    @staticmethod
    def edit(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/products")

        conn = DB.connect_db()
        conn.cursor()
        sql = "SELECT * FROM `tbl_products` WHERE `id`=?"
        res = conn.execute(sql, (id))

        raw = res.fetchone()
        products = {
            "id": raw[0],
            "name": raw[1],
            "description": raw[2],
            "price": raw[3],
            "instock": raw[4]
        }
        conn.close()

        return render_template("admin/products/edit.html", products=products)
    
    @staticmethod
    def update(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/products")
        
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        instock = request.form.get("instock")
        images = request.files.getlist("images") 
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        if name == "":
            session["product_name_error"] = "Name is required!"
            return redirect(f"/admin/products/edit/{id}")
        
        if description == "":
            session["product_description_error"] = "Description is required!"
            return redirect(f"/admin/products/edit/{id}")
        
        if price == "":
            session["product_price_error"] = "Price is required!"
            return redirect(f"/admin/products/edit/{id}")
        
        if instock == "":
            session["product_instock_error"] = "Instock is required!"
            return redirect(f"/admin/products/edit/{id}")

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_products` SET `name`=?, `description`=?, `price`=?, `instock`=?, `updated_at`=? WHERE `id`=?"
        conn.execute(sql, (name, description, price, instock, updated_at, id))
        conn.commit()

        if len(images) > 0:

            sql = "UPDATE `tbl_product_images` SET `deleted_at`=? WHERE `product_id`=?"
            conn.execute(sql, (updated_at, id))
            conn.commit()

            directory = "static/upload/products/"
        
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            image_list = []
            for image in images:
                timestamp = str(datetime.datetime.now().timestamp()).split(".")[0]
                image_name = f"{timestamp}_{secure_filename(image.filename)}"
                image.save(os.path.join(directory, image_name))
                print(image_name)
                image_list.append(image_name)
                
            for image in image_list:
                sql = "INSERT INTO `tbl_product_images` (`product_id`, `image`, `created_at`) VALUES (?, ?, ?)"
                conn.execute(sql, (id, image, created_at))
                conn.commit()

        conn.close()

        return redirect("/admin/products")
    
    @staticmethod
    def delete(id):
        if id.isnumeric() != True or int(id) < 1:
            return redirect("/admin/products")
        
        deleted_at = datetime.datetime.now()

        conn = DB.connect_db()
        conn.cursor()
        sql = "UPDATE `tbl_products` SET `deleted_at`=? WHERE `id`=?"
        conn.execute(sql, (deleted_at, id))
        conn.commit()
        conn.close()

        return redirect("/admin/products")