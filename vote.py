import datetime
from flask import render_template, request, redirect, url_for, jsonify, Flask, g, Blueprint
from . import db

bp = Blueprint("vote", "vote", url_prefix="")

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
    cursor.execute("select pass from users where name = %s;", (username,))
    lpass = cursor.fetchone()
    if lpass[0] != password:
      status = "Incorrect User Details, Try Again"
    else:
      cursor.execute("select id from users where name = %s;", (username,))
      owner = cursor.fetchone()
      oid = owner[0]
      return redirect(url_for("vote.home", oid=oid), 302)
  return render_template("login.html",status=status, lpass=lpass)
    
@bp.route("/create")
def create():
  return render_template("create.html")

@bp.route("/createuser", methods=["POST"])
def createuser():
  conn = db.get_db()
  cursor = conn.cursor()
  username = request.form['username']
  password = request.form['password']
  cursor.execute("""insert into users (name, pass) values (%s, %s);""", (username, password))
  conn.commit()
  return redirect(url_for("vote.dashboard"), 302)
  
@bp.route("/home/<oid>")
def home(oid):
  oby = ["id", "name", "created"]
  conn = db.get_db()
  cursor = conn.cursor()
  
  d = datetime.datetime.now().strftime("%Y-%m-%d")
  cursor.execute("""
  delete from allpolls
  where (%s-cdate)>=7""",(d,))
  
  oid = oid
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
  return render_template("home.html", oid=oid, polls=polls, order="desc" if order=="asc" else "asc")
  
@bp.route("/createpoll/<oid>")
def createpoll(oid):
  oid = oid
  return render_template("makepoll.html", oid=oid)

@bp.route("/makepoll/<oid>", methods=["POST"])
def makepoll(oid):
   itemname = []
   itemdesc = [] 
   
   conn = db.get_db()
   cursor = conn.cursor()
   
   pollname = request.form['pollname']
   polldesc = request.form['polldesc']
   pollowner = oid
   polldate = datetime.datetime.now().strftime("%d/%m/%Y")
   
   cursor.execute("""insert into allpolls (name, oid, cdate, description) values (%s, %s, %s, %s);""", (pollname, pollowner, polldate, polldesc))
   
   cursor.execute("""select id from allpolls where name = %s;""", (pollname,))
   pollid = cursor.fetchone()
   pid = pollid[0]
   
   conn.commit()
   
   return redirect(url_for("vote.createentry", oid=oid, pid=pid), 302)

@bp.route("/createentry/<oid>/<pid>")
def createentry(oid, pid):
  oid = oid
  pid = pid
  return render_template("makeentry.html", oid=oid, pid=pid)
  
@bp.route("/makeentry/<oid>/<pid>", methods=["GET", "POST"])
def makeentry(oid, pid):
  status = 'n'
  oid = oid
  pid = pid
  
  conn = db.get_db()
  cursor = conn.cursor()
  
  if request.method == 'POST':
  
    itemname = request.form['itemname']
    itemdesc = request.form['itemdesc']
    cursor.execute("""insert into poll (item, votes, own, description, pid) values (%s, %s, %s, %s, %s);""", (itemname, 0, oid, itemdesc, pid))
    conn.commit()
  
    status = request.form['status']
    
    if status == 'y' or status == 'Y':
      return redirect(url_for("vote.home", oid=oid), 302)
    elif status == 'n' or status == 'N':
      return redirect(url_for("vote.makeentry", oid=oid, pid=pid), 302)

  return redirect(url_for("vote.createentry", oid=oid, pid=pid), 302)
  
@bp.route("/pollinfo/<pid>/<oid>")
def pollinfo(pid, oid):
  pid = pid
  oid = oid
  oby = ["id", "name"]
  conn = db.get_db()
  cursor = conn.cursor()
  
  if oby[0] == request.args.get("order_by", "id"):
    order = request.args.get("order", "asc")
    if order == "asc":
      cursor.execute("""select id, item, description from poll where pid = %s order by id ;""", (pid,))
    else:
      cursor.execute("""select id, item, description from poll where pid = %s order by id desc;""", (pid,))
  elif oby[1] == request.args.get("order_by", "name"):
    order = request.args.get("order", "asc")
    if order == "asc":
      cursor.execute("""select id, item, description from poll where pid = %s  order by item;""", (pid,))
    else:
      cursor.execute("""select id, item, description from poll where pid = %s  order by item desc;""", (pid,))
      
  polls = cursor.fetchall()
  return render_template("info.html", pid=pid, polls=polls, oid=oid, order="desc" if order=="asc" else "asc")
  
@bp.route("/pollresult/<pid>/<oid>", methods=["POST"])
def result(pid, oid):
  conn = db.get_db()
  cursor = conn.cursor()
  pid = pid
  oid = oid
  choice = request.form['choice']
  
  cursor.execute("""
  update poll
  set votes = votes + 1
  where id = %s and own = %s and pid = %s;""", (choice, oid, pid))
  
  conn.commit()
  return redirect(url_for("vote.homewr", oid=oid), 302)
  
@bp.route("/homewr/<oid>")
def homewr(oid):
  oby = ["id", "name", "created"]
  conn = db.get_db()
  cursor = conn.cursor()
  
  d = datetime.datetime.now().strftime("%d/%m/%Y")
  cursor.execute("""
  delete from allpolls
  where (%s-cdate)>=7""",(d,))
  
  oid = oid
  
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
  
  
  cursor.execute(f"select p.item, p.votes, p.pid from poll p, allpolls a where p.pid = a.id order by p.votes")
  result = cursor.fetchall()
  
  return render_template("homewr.html", oid=oid, result=result, polls=polls, order="desc" if order=="asc" else "asc")
    


























