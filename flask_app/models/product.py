from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Product:
    db_name = 'shop'
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.user_id = data['user_id']
        self.image = data['image']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_product_by_id(cls, data):
        query = "SELECT * FROM products WHERE products.id = %(product_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    #READ
    @classmethod
    def get_all(cls):
        query = "SELECT products.*, users.first_name, users.last_name, COUNT(saves.product_id) as num_saves FROM products LEFT JOIN users ON products.user_id = users.id LEFT JOIN saves ON products.id = saves.product_id GROUP BY products.id ORDER BY created_at DESC;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db_name).query_db(query)
        # Create an empty list to append our instances of users
        products = []
        if results:
        # Iterate over the db results and create instances of friends with cls.
            for product in results:
                products.append(product)
            return products
        return products
    
    #CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO products (name, description, image,category, price, user_id) VALUES ( %(name)s, %(description)s, %(image)s, %(category)s, %(price)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE products SET name = %(name)s, description = %(description)s, image = %(image)s, category = %(category)s, price = %(price)s WHERE products.id = %(product_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM products WHERE products.id = %(product_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
        #DELETE
    @classmethod
    def deleteAllSaves(cls, data):
        query = "DELETE FROM saves WHERE product_id = %(product_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #add save
    @classmethod
    def addSave(cls, data):
        query = "INSERT INTO saves (product_id, user_id) VALUES ( %(product_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    @classmethod
    def unSave(cls, data):
        query = "DELETE FROM saves WHERE product_id = %(product_id)s and user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_product_savers(cls, data):
        query = "SELECT * from saves LEFT JOIN users on saves.user_id = users.id WHERE product_id = %(product_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        nrOfSaves = []
        if results:
            for row in results:
                nrOfSaves.append(row['email'])
            return nrOfSaves
        return nrOfSaves


    @staticmethod
    def validate_product(product):
        is_valid = True
        
        if len(product['name']) <2:
            flash('Product title should be more than 2 characters!', 'nameProduct')
            is_valid= False
        if len(product['description']) <2:
            flash('Description should be more than 2 characters!', 'descriptionProduct')
            is_valid= False
        # if int(product['price']) <0:
        #     flash('Product price should be a positive value!', 'priceProduct')
        #     is_valid= False
        if not product.get('category'):
            flash('Category should be selected!', 'categoryProduct')
            is_valid = False
        if not product.get('price'):
            flash('Price is obligatory!', 'priceProduct')
            is_valid = False

        return is_valid
        