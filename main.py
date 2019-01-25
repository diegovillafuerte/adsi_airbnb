from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, jsonify, flash
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

#1
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
	'''Returns a list of all the restaurants in the database
	It allows addition, deletion and edition of restaurants'''
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants = restaurants)

#2
@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>')
def showMenu(restaurant_id):
	'''This function shows all the menu items for the specified restaurant. 
	It also allows edition, deletion and addition of menu items'''
	restaurants = session.query(Restaurant).all()
	items = session.query(MenuItem).all()
	return render_template('menu.html', restaurants = restaurants, items = items, restaurant_id = restaurant_id)

#3
@app.route('/restaurant/new', methods = ['POST', 'GET'])
def newRestaurants():
	#return "This page will be for making a new restaurant"
	if request.form:
		newRest = Restaurant(name = request.form.get('name'))
		session.add(newRest)
		session.commit()
		flash("New restaurant succesfully created")
		return redirect(url_for('showRestaurants'))
	return render_template('newRestaurant.html')

#4
@app.route('/restaurant/<int:restaurant_id>/delete', methods = ['POST', 'GET'])
def deleteRestaurants(restaurant_id):
	#return "This page will delete restaurant %s" % (restaurant_id)
	restaurants = session.query(Restaurant).all()
	if request.method == 'POST':
		restToDelete = session.query(Restaurant).filter_by(id = restaurant_id).one()
		session.delete(restToDelete)
		session.commit()
		flash("Restaurant succesfully deleted")
		return redirect(url_for('showRestaurants'))
	return render_template('deleteRestaurant.html', restaurants = restaurants, restaurant_id = restaurant_id)

#5
@app.route('/restaurant/<int:restaurant_id>/edit', methods = ['POST', 'GET'])
def editRestaurants(restaurant_id):
	#return "This page will edit restaurant %s" % (restaurant_id)
	restaurants = session.query(Restaurant).all()
	if request.method == 'POST':
		restToEdit = session.query(Restaurant).filter_by(id = restaurant_id).one()
		restToEdit.name = request.form.get('name')
		session.add(restToEdit)
		session.commit()
		flash("Restaurant succesfully edited")
		return redirect(url_for('showRestaurants'))
	return render_template('editRestaurant.html', restaurants = restaurants, restaurant_id = restaurant_id)


#6
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods = ['POST', 'GET'])
def newMenuItem(restaurant_id):
	#return "This page will be for making a new menu item for restaurant %s" % (restaurant_id)
	restaurants = session.query(Restaurant).all()
	if request.method == 'POST':
		niuMenuItem = MenuItem(name = request.form.get('name'), description = request.form.get('description'),\
		 price = request.form.get('price'), course = request.form.get('course'), restaurant_id = restaurant_id)
		session.add(niuMenuItem)
		session.commit()
		flash("New menu item succesfully added")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	return render_template('newMenuItem.html', restaurants = restaurants, restaurant_id = restaurant_id)

#7
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/delete', methods = ['POST', 'GET'])
def deleteMenuItem(restaurant_id, menuItem_id):
	#return "This page will be for deleting menu item %s for restaurant %d" % (menuItem_id, restaurant_id)
	restaurants = session.query(Restaurant).all()
	items = session.query(MenuItem).all()
	if request.method == 'POST':
		itemToDelete = session.query(MenuItem).filter_by(id = menuItem_id).one()
		session.delete(itemToDelete)
		session.commit()
		flash("Menu item succesfully deleted")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	return render_template('deleteMenuItem.html', restaurants = restaurants, restaurant_id = restaurant_id, items = items, menuItem_id = menuItem_id)


#8
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/edit', methods = ['POST', 'GET'])
def editMenuItem(restaurant_id, menuItem_id):
	#return "This page will be for editing menu item %s for restaurant %d" % (menuItem_id, restaurant_id)
	restaurants = session.query(Restaurant).all()
	items = session.query(MenuItem).all()
	if request.method == 'POST':
		itemToEdit = session.query(MenuItem).filter_by(id = menuItem_id).one()
		itemToEdit.name = request.form.get('name')
		itemToEdit.description = request.form.get('description')
		itemToEdit.price = request.form.get('price')
		itemToEdit.course = request.form.get('course')
		session.add(itemToEdit)
		session.commit()
		flash("Menu item succesfully edited")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))

	return render_template('editMenuItem.html', restaurants = restaurants, restaurant_id = restaurant_id, items = items, menuItem_id = menuItem_id)

@app.route('/restaurants/JSON')
@app.route('/JSON')
def restaurantsJSON():
	'''Send data in JSON format'''
	restaurants = session.query(Restaurant).all()
	return jsonify(restaurant=[i.serialize for i in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
@app.route('/restaurant/<int:restaurant_id>/JSON')
def MenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menuItem_id>/JSON')
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/JSON')
def menuItemJSON(restaurant_id, menuItem_id):
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).filter_by(id=menuItem_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000, threaded = False)














