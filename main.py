from itertools import product
from flask import Flask
from flask import render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
from database import get_db
import os
from database import get_db



app=Flask(__name__)

CUSTOMERID=1

@app.route("/")
def home_page():
     con=get_db().cursor()
     con.execute("select * from customers;")
     customers=con.fetchall()
     con.close()
     return render_template('home_page.html',customers=customers)


@app.route("/shop",methods=('GET','POST'))
def shop_page():
     if request.method=='POST':
          customerid=CUSTOMERID
          productid=request.form['productid']
          con =get_db()
          con.execute(f"insert into customersproducts(customerid,productid) values('{customerid}','{productid}')")
          con.commit()
          con.close()
          # return admin_products() 
     con=get_db().cursor()
     con.execute("select * from products;")
     products=con.fetchall()
     con.close()
     return render_template('shop_page.html', products=products)





@app.route("/admin")
def admin_home():
     return render_template('admin_home.html')

@app.route("/admin/listProducts")
def admin_products():
    con=get_db().cursor()
    con.execute("select * from products;")
    products=con.fetchall()
    con.close()
    return render_template('admin_products.html', products=products)




@app.route('/admin/add',methods=('GET','POST'))
def admin_add():
     if request.method=='POST':
          productname=request.form['productname']
          price=request.form['price']
          if 'image' not in request.files:
            return redirect(request.url)
          file = request.files['image']
          filename = secure_filename(file.filename)
          file.save(os.path.join('static','uploads',filename))
          con =get_db()
          con.execute(f"insert into products(productname,price,imagefile) values('{productname}',{price},'{filename}')")
          con.commit()
          con.close()
          return admin_products()        
     return render_template ('admin_add.html')


@app.get('/admin/delete/<int:productid>')
def admin_delete(productid):
          con =get_db()
          con.execute(f"delete from products where productid='{productid}'")
          con.commit()
          con.close()
          return redirect(url_for('admin_products'))


@app.route('/admin/addcustomer',methods=('GET','POST'))
def admin_add_customer():
     if request.method=='POST':
          customername=request.form['customername']
          con =get_db()
          con.execute(f"insert into customers(customername) values('{customername}')")
          con.commit()
          con.close()
          return admin_products()        
     return render_template ('admin_add_customer.html')


@app.route('/listorders')
def list_orders():
          customerid=f"{CUSTOMERID}"
          con =get_db().cursor()
          con.execute(f"select * from customersproducts cp join products on cp.productid = products.productid  join customers on cp.customerid = customers.customerid where customers.customerid={customerid}")
          products=con.fetchall()
          con.close()    
          return render_template ('list_orders.html',products=products)




@app.route('/admin/update/<int:productid>',methods=['GET','POST'])
def admin_update(productid):
     if request.method=="POST":
           productname=request.form['productname']
           price=request.form['productprice']
           if 'image' not in request.files:
            return redirect(request.url)
           file = request.files['image']
           filename = secure_filename(file.filename)
           file.save(os.path.join('static','uploads',filename))
           con=get_db()
           con.execute(f"update products set productname='{productname}',price={price},imagefile='{filename}' where productid={productid};")
           con.commit()
           con.close()
           return redirect (url_for('admin_products'))
     con= get_db().cursor()
     con.execute(f"select * from products where productid={productid};")
     product=con.fetchone()
     con.close()
     return render_template('admin_update.html', product=product)


@app.post('/search')
def search_page():
     if 'productid' in request.form:
         return shop_page()
     else:
          name=request.form['search']
          con=get_db().cursor()
          con.execute(f"select * from products where productname like '%{name}%'")
          data=con.fetchall()
          return render_template('shop_page.html',products=data)



@app.post('/admin/search')
def admin_search():
     name=request.form['adminsearch']
     con=get_db().cursor()
     con.execute(f"select * from products where productname like '%{name}%'")
     data=con.fetchall()
     return render_template('admin_products.html',products=data)


@app.get('/delete/<int:productid>')
def delete_order(productid):
     con=get_db()
     con.execute(f"delete from customersproducts where productid={productid} and customerid={CUSTOMERID};")
     con.commit()
     con.close()
     return redirect(url_for('list_orders'))