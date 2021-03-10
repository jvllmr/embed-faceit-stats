from flask import Flask, send_file, abort, Response
import os, sqlite3, threading
from takescreenshot import take_screenshot
from datetime import datetime
app = Flask(__name__)

@app.route("/<name>")
def return_image(name):
    if sql.execute("select * from lastrefresh where name=?", (name,)).fetchone():
        entry = sql.execute("select * from lastrefresh where name=?", (name,)).fetchone()
        entrydate = entry[1]
        entryyear = entrydate.split(":")[0]
        entrymonth = entrydate.split(":")[1]
        entryday = entrydate.split(":")[2]
        now = datetime.now()
        if int(now.strftime("%d")) > int(entryday) or int(now.strftime("%m")) > int(entrymonth) or int(now.strftime("%Y")) > int(entryyear):
            scr_thread = threading.Thread(target=take_screenshot, args=(name,))
            scr_thread.start()
            sql.execute("insert into lastrefresh values (?,?)",(name,datetime.now().strftime("%Y:%m:%d")))
            sql.commit()
            return send_file(f"screenshots/{name}.png")
        if f"{name}.png" in os.listdir("screenshots"):
            return send_file(f"screenshots/{name}.png")
        else:
            abort(Response("This resource doesn't exist. Maybe it takes some time to be created..."))
    else:
        scr_thread = threading.Thread(target=take_screenshot, args=(name,))
        scr_thread.start()
        sql.execute("insert into lastrefresh values (?,?)",(name,datetime.now().strftime("%Y:%m:%d")))
        sql.commit()
        return abort(Response("This resource doesn't exist. Maybe it takes some time to be created..."))

@app.route("/")
def youre_wrong_here():
    abort(404)



if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    if not "screenshots" in os.listdir():
        os.mkdir("screenshots")
    if not "database.db" in os.listdir():
        sql = sqlite3.connect("database.db")
        sql.execute("create table lastrefresh (name text, date text)")
        sql.commit()
    else:
        sql = sqlite3.connect("database.db")
    server = pywsgi.WSGIServer(('', 5005), app, handler_class=WebSocketHandler)
    server.serve_forever()
