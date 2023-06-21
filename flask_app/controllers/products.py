from flask_app import app
from flask_app.models.user import User
from flask_app.models.product import Product

from flask import render_template, redirect, session, request, flash

from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS
from datetime import datetime
from werkzeug.utils import secure_filename
import os

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
# The limit is 3 MB

#Check if the format is right
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add/product')
def addProduct():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        loggedUser = User.get_user_by_id(data)
        return render_template('addProduct.html', loggedUser = loggedUser)
    return redirect('/')

@app.route('/create/product', methods = ['POST'])
def createProduct():
    if 'user_id' in session:
        if not Product.validate_product(request.form):
            return redirect(request.referrer)
        
###############################################################################
        # 1  Check is image exist / is uploadedn
        if not request.files['image']:
            flash('Product image is required!', 'product')
            return redirect(request.referrer)
        image = request.files['image']
        # IMAGE
        # 2  Controll if it is in the correct format 
        if not allowed_file(image.filename):
            flash('Product image showld be in png, jpg. jpeg format!', 'productImage')
            return redirect(request.referrer)
  
        # 3  ADD Timestamp to use as name to avaid same names on uploaded files

        if image and allowed_file(image.filename):
            filename1 = secure_filename(image.filename)
            time = datetime.now().strftime("%d%m%Y%S%f")
            time += filename1
            filename1=time
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename1))
        
        # 4 - Save it in the db at data 
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'category': request.form['category'],
            'price': request.form['price'],
            'user_id': session['user_id'],
            'image' : filename1
        }
        Product.save(data)
        return redirect('/sell')
    return redirect('/')



@app.route('/edit/product/<int:id>')
def editProduct(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'product_id': id
        }
        loggedUser = User.get_user_by_id(data)
        product = Product.get_product_by_id(data)
        print(loggedUser['id'])
        print(product['user_id'])
        if loggedUser['id'] == product['user_id']:
            return render_template('editProduct.html', loggedUser = loggedUser, product= product)
        return redirect('/dashboard')
    return redirect('/')

@app.route('/product/<int:id>')
def viewProduct(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'product_id': id
        }
        loggedUser = User.get_user_by_id(data)
        product = Product.get_product_by_id(data)
        savesNr = Product.get_product_savers(data)
        loggedUserSavedProduct = User.get_user_saved_products(data)


        return render_template('showOne.html',savedproducts=loggedUserSavedProduct, loggedUser = loggedUser, product= product, savesNr= savesNr)
    return redirect('/')

@app.route('/edit/product/<int:id>', methods = ['POST'])
def updateProduct(id):
    if 'user_id' in session:
        data1 = {
            'user_id': session['user_id'],
            'product_id': id
        }
        loggedUser = User.get_user_by_id(data1)
        product = Product.get_product_by_id(data1)
        if loggedUser['id'] == product['user_id']:

            if not Product.validate_product(request.form):
                return redirect(request.referrer)
            
    ###############################################################################
            # 1  Check is image exist / is uploadedn
            if not request.files['image']:
                filename1 = product['image']
            image = request.files['image']
            # IMAGE
            # 2  Controll if it is in the correct format 
            if request.files['image']:
                if not allowed_file(image.filename):
                    flash('Product image showld be in png, jpg. jpeg format!', 'productImage')
                    return redirect(request.referrer)
        
                # 3  ADD Timestamp to use as name to avaid same names on uploaded files

                if image and allowed_file(image.filename):
                    filename1 = secure_filename(image.filename)
                    time = datetime.now().strftime("%d%m%Y%S%f")
                    time += filename1
                    filename1=time
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename1))
                    print(image)
            # 4 - Save it in the db at data 
            data = {
                'name': request.form['name'],
                'description': request.form['description'],
                'category': request.form['category'],
                'price': request.form['price'],

                'product_id': product['id'],
                'user_id': session['user_id'],
                'image' : filename1
            }
            Product.update(data)
            return redirect('/sell')
        return redirect('/buy')
    return redirect('/')

@app.route('/delete/product/<int:id>')
def deleteProduct(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'product_id': id
        }
        loggedUser = User.get_user_by_id(data)
        product = Product.get_product_by_id(data)
                # Check that loggedUser and product are not boolean values
        if isinstance(product, bool):
            return "Error: Could not retrieve user or product data"
        Product.deleteAllSaves(data)
        Product.delete(data)
        return redirect(request.referrer)

        return redirect('/dashboard')
    return redirect('/')

@app.route('/save/<int:id>')
def saveProduct(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'product_id': id
        }
        
        savedProduct = User.get_user_saved_products(data)
        print("///////////////////////////////")
        print(savedProduct)
        if id not in savedProduct:
            Product.addSave(data)
            print("************************************")
            return redirect(request.referrer)
        return redirect(request.referrer)
    return redirect('/')

@app.route('/unsave/<int:id>')
def unsaveProduct(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'product_id': id
        }
        print("/------------------------------------")
        Product.unSave(data)
        return redirect(request.referrer)
    return redirect('/')
