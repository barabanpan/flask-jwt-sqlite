Has NO cyclic imports! 
Application Factory pattern was used to avoid it.
(You can see how pretty run.py is now)

Runs like this:
FLASK_APP=run.py FLASK_DEBUG=1 flask run
(runs even with cyclic imports)

And like this:
python run.py

Use postman collection to 
register new users, 
login, 
logout, 
refresh expired jwt token, 
see list of users, 
delete all users 
and see secret info once logged in.
