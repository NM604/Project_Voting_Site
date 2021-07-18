import datetime
from flask import render_template, request, redirect, url_for, jsonify, Flask, g, Blueprint
from . import db

bp = Blueprint("vote", "vote", url_prefix="")

def format_date(d):
  if d:
    d = datetime.datetime.strptime(d, '%Y-%m-%d')
    v = d.strftime("%a - %b %d, %Y")
    return v
  else:
    return None

@bp.route("/")   
def dashboard():
  return render_template("login.html")

@bp.route("/login", methods = ["GET", "POST"])
def login():
  conn = db.get_db()
  cursor = conn.cursor()
  status = None
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    lpass = cursor.execute("select pass from users where name = ?;", [username])
    rpass = lpass.fetchone()
    if rpass[0] != password:
      status = "Incorrect User Details, Try Again"
    else:
      return redirect(url_for("vote.home"), 302)
  return render_template("login.html",status=status, lpass=lpass, rpass=rpass[0])
    
@bp.route("/create")
def create():
  return render_template("create.html")

@bp.route("/createuser", methods=["POST"])
def createuser():
  conn = db.get_db()
  cursor = conn.cursor()
  username = request.form['username']
  password = request.form['password']
  cursor.execute("""insert into users (name, pass) values (?, ?);""", (username, password))
  conn.commit()
  return redirect(url_for("vote.dashboard"), 302)
  
@bp.route("/home")
def home():
  oby = ["id", "name", "created"]
  conn = db.get_db()
  cursor = conn.cursor()
  
  if oby[0] == request.args.get("order_by", "id"):
    order = request.args.get("order", "asc")
    if order == "asc":
      cursor.execute(f"select id, name, cdate, description from allpolls order by id")
    else:
      cursor.execute(f"select id, name, cdate, description from allpolls order by id desc")
  elif oby[1] == request.args.get("order_by", "name"):
    order = request.args.get("order", "asc")
    if order == "asc":
      cursor.execute(f"select id, name, cdate, description from allpolls order by name")
    else:
      cursor.execute(f"select id, name, cdate, description from allpolls order by name desc")
  elif oby[2] == request.args.get("order_by", "created"):
    order = request.args.get("order", "asc")
    if order == "asc":
      cursor.execute(f"select id, name, cdate, description from allpolls order by cdate")
    else:
      cursor.execute(f"select id, name, cdate, description from allpolls order by cdate desc")
  polls = cursor.fetchall()
  return render_template("home.html", polls=polls, order="desc" if order=="asc" else "asc")
  
@bp.route("/createpoll")
def createpoll():
  return render_template("makepoll.html")
