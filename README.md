# CS-S33a Project 3: Pizza Restaurant Website
This is a pizza restaurant website where users are able to add food items to their cart, order items, and check its order status.



## orders directory

### admin.py
Allowed models in model.py to be accessed in admin page.

* Admin ID: rachelmoon
* Admin PW: hello12345


### apps.py
Added Orders application in the configuration.


### models.py
Added models: Menu, PizzaTopping, SubTopping, Cart, CartEntry, PizzaToppingEntry, SubToppingEntry, Order, OrderEntry, PizzaTopping_OrderEntry, SubTopping_OrderEntry.


### urls.py
Assigned appropriate url route to views.


### views.py
Added functions for each page of the website. Users can log in, sign up, view menu, add items to cart, view cart, add toppings, confirm order, view orders. Superusers can manage orders and update order status.


## pinocchios directory

### settings.py
Added Orders application in list of installed apps, and changed timezone to New York (EST).


### urls.py
Added url route for Orders application.


## templates and static files

### style.css
Stylesheet for html files.


### base.html
This is the base html template.


### index.html
This is the main home page for visitors.


### error.html
This is the error template.


### login.html
Users can log in here.


### signup.html
Users can sign up here.

### signupsuccess.html
This html shows that signup was successful.


### user.html
This is logged in user(customer)'s main page.


### menu.html
This is menu page, where users can update quantity of items that they want to order.


### addtocart.html
If items have been added to cart, user sees this page.


### cart.html
User can view cart information here.


### addtoppings.html
Users can add toppings to relevant items in the cart.


### toppngsadded.html
When toppings have been added successfully, user sees this page.


### orderconfirm.html
User confirms his/her order here.


### orderplaced.html
When order has been successful, user will see this page.


### myorder.html
User can view his/her orders here.


### superuser.html
This is superuser's main page.


### manageorders.html
Superuser can view all the orders here.


### orderstatus_change.html
If superuser changes order status, he/she will see this page that update was successful.
