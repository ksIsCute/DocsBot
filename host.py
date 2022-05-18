import json, requests, random, string, flask, time, datetime
from threading import Thread
from flask import Flask, render_template, request, redirect
from datetime import timedelta

app = Flask('', static_url_path="/static")

onlinesince = time.time()
serverarray=["server1", "server2", "theEpicDuckServer", "Gamer Server"]
currentversion = "1.0"

@app.route("/channelpick", methods=["GET", "POST"])
def channelpick():
  with open("json/data.json", "r") as f:
    data = json.load(f)
  if request.args:
    if "lang" in request.args:
      language = request.args.get('lang')
    else:
      language = "en"
    server = request.args.get('server')
    with open("json/data.json", "r") as f:
      data = json.load(f)
    if request.method == "POST":
      channel = request.form.get('channelid')
      message = request.form.get('message')
      if len(message) == 0:
        return "Please input an actual message!"
      if server.lower() in [x.lower() for x in data['Docs']['server']['servers']]:
        with open("json/data.json", "r") as f:
          data = json.load(f)
        with open("json/data.json", "w") as f:
          data[server.capitalize()]['sendable']['message'] = message
          data[server.capitalize()]['sendable']['channel'] = channel
          json.dump(data, f, indent=2)
        index = [i for i, s in enumerate(data[server.capitalize()]['channels']) if channel in s]
        return render_template("sent.html", servername=server, messagesent=message, channelname=[s for s in data[server.capitalize()]['channels'] if any(xs in s for xs in channel)][int('%s' % ''.join(map(str, index)))].split(" - ")[0], lang=language, pserver=data[server.capitalize()]['id'], pchannel=channel)
      else:
        return render_template("pickchannel.html", channels=data[server.capitalize()]['channels'], error="Please pick a valid server!", lang=language)
    else:
      with open("json/data.json", "r") as f:
        data = json.load(f)
    return render_template("pickchannel.html", channels=data[server.capitalize()]['channels'], lang=language)
  else:
    return render_template("pickchannel.html", error="You dont have the server arg within this url! Please change that!", lang=language)

@app.route("/", methods=["GET", "POST"])
def home():
  requests.post("https://flaskmsgsendthing.ksiscute.repl.co/asjwahye7823yh38hf7348hfsdyqwys8chSAYQWYH")
  
  if request.args:
    language = request.args.get('lang')
  else:
    language = "en"
  with open("json/data.json", "r") as f:
    data = json.load(f)
  
  if request.method == "POST":
    server = request.form.get('server')
    
    if server.lower() in [x.lower() for x in data['Docs']['server']['servers']]:
      if len(server) == 0:
        return "Server index is empty! Please give a valid server!"
      else:  
        return redirect(f"https://flaskmsgsendthing.ksiscute.repl.co/channelpick?server={server.capitalize()}")
      
    else:
      return "Server invalid!"
  return render_template("index.html", servers=data['Docs']['server']['servers'], servercount=data['Docs']['server']['count'], usercount=data['Docs']['users'], lang=language, totalvisits=data['visits'], version=currentversion, checkver=str(data.get('version')), uptime=str(datetime.timedelta(seconds=int(round(time.time() - onlinesince)))))

code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
prefixarray = ["d!", "docs!", "doc!", "D!"]
@app.route("/maindashboard", methods=["GET", "POST"])
def mdb():
  with open("json/prefixes.json", "r") as f:
    data = json.load(f)
  try:
    uname = request.args.get("username")
    lang = request.args.get("lang")
    userid = request.args.get("userid")
    code = request.args.get("code")
    sname = request.args.get("servername")
    serverid = request.args.get("serverid")
  except:
    return redirect("https://flaskmsgsendthing.ksiscute.repl.co/dashboard")
  link = requests.get(url=f"https://api.revolt.chat/servers/{serverid}", headers={"x-session-token": "wK4XdZfvQrc4mA_DhwHcxtCLcj5OOLf4dtO7uOu0AzHxjWONviF0D6-Ue98N4qUk"})
  sid = link.json()["_id"]
  for arg in request.args:
    print(arg)
    print(request.args.get(arg))
  if request.method == "POST":
    prefix = request.form.get("addprefix")
    dprefix = request.form.get("delprefix")
    if len(prefix) > 0:
      if prefix in data[sid]["prefixes"]:
        return render_template("maindb.html", username=uname, lang=lang, code=code, uid=userid, sname=sname, notice=f"That prefix already exists!", parray=data[sid]["prefixes"])
      else:
        with open("json/prefixes.json", "w") as f:
          data[sid]["prefixes"].append(prefix)
          json.dump(data, f, indent=2)
        return render_template("maindb.html", username=uname, lang=lang, code=code, uid=userid, sname=sname, notice=f"Added prefix <strong>{prefix}</strong> to your new list of {len(data[sid]['prefixes'])} prefix(es)", parray=data[sid]['prefixes'])
        
    if len(dprefix) > 0:
      if len(data[sid]["prefixes"]) == 1:
        return render_template("maindb.html", username=uname, lang=lang, code=code, uid=userid, sname=sname, notice=f"You must have at least 1 prefix at all times!", parray=data[sid]['prefixes'])
      if dprefix in data[sid]["prefixes"]:
        with open("json/prefixes.json", "w") as f:
          data[sid]["prefixes"].remove(dprefix)
          json.dump(data, f, indent=2)
        return render_template("maindb.html", username=uname, lang=lang, code=code, uid=userid, sname=sname, notice=f"Removed prefix <strong>{dprefix}</strong> to your new list of {len(data[sid]['prefixes'])} prefix(es)", parray=data[sid]['prefixes'])
      else:
        return render_template("maindb.html", username=uname, lang=lang, code=code, uid=userid, sname=sname, notice=f"That prefix doesnt exist! Please make sure you have the correct capitalization!", parray=data[sid]['prefixes'])
    else:
      return render_template("maindb.html", username=uname, lang=lang, code=code, uid=userid, sname=sname, notice=f"You need to provide valid form information!", parray=data[sid]["prefixes"])
  
  return render_template("maindb.html", username=uname, lang=lang, code=code, uid=userid, sname=sname, notice="", parray=data[sid]["prefixes"])

@app.route("/mainframe", methods=["GET", "POST"])
def maindash():
  if request.args:
    uname = request.args.get("username")
    lang = request.args.get("lang")
    userid = request.args.get("userid")
    code = request.args.get("code")
  else:
    return redirect("https://flaskmsgsendthing.ksiscute.repl.co/dashboard")
    
  for arg in request.args:
    print(arg)
  if request.method == "POST":
    link = requests.get(url=f"https://api.revolt.chat/servers/{request.form.get('server')}", headers={"x-session-token": "wK4XdZfvQrc4mA_DhwHcxtCLcj5OOLf4dtO7uOu0AzHxjWONviF0D6-Ue98N4qUk"})
    print(link.json())
    return redirect(f"https://flaskmsgsendthing.ksiscute.repl.co/maindashboard?lang=en&servername={link.json()['name']}&serverid={link.json()['_id']}&userid={userid}&username={uname}&code={code}")
  
  return render_template("mainframe.html", username=uname, lang=lang, code=code, uid=userid)

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
  if request.args:
    lang = request.args.get("lang")
  else:
    lang = "en"
  if request.method == "POST":
    userid = request.form.get("userid")
    link = requests.get(url=f"https://api.revolt.chat/users/{userid}", headers={"x-session-token": "wK4XdZfvQrc4mA_DhwHcxtCLcj5OOLf4dtO7uOu0AzHxjWONviF0D6-Ue98N4qUk"})
    try:
      if link.json()['bot']:
        return render_template("dashboard.html", error="That account is a bot! Please use a non bot account, like YOUR user id!")
    except:
      if code in link.json()['status']['text']:
        return redirect(f"https://flaskmsgsendthing.ksiscute.repl.co/mainframe?lang=en&userid={userid}&username={link.json()['username']}&code={code}")
      else:
        print(link.json()['status']['text'])
        return render_template("dashboard.html", lang=lang, error=f"Please input your 10 character code:\n \"{code}\" \nin your revolt status by right clicking your avatar in the top left!")
  return render_template("dashboard.html", lang=lang, error=f"Your 10 character code for your Revolt status is:\n \"{code}\"")

@app.route("/asjwahye7823yh38hf7348hfsdyqwys8chSAYQWYH", methods=["GET", "POST"])
def versioncheck():
  with open("json/data.json", "r") as f:
    data = json.load(f)
  if request.method == "POST":
    with open("json/data.json", "w") as f:
      data['visits'] += 1
      json.dump(data, f, indent=2)
  return str(data.get('version'))

@app.route("/embed", methods=["GET", "POST"])
def embedmaker():
  if request.args:
    title = request.args.get("title")
    color = request.args.get("color")
    description = request.args.get("description")
    link = request.args.get("link")
    image = request.args.get("image")
    if image in ['', 'none']:
      setimage = "/static/images/noimage.png"
    else:
      setimage = f"/static/embimg/{''.join(request.access_route[0].split('.')[1:])}.png"
    if not color:
      color = "FFFFFF"
    return render_template("embed.html", embtitle=title, embdesc=description, embcolor=color.replace("#", ""), emblink=link, embimage=setimage)
  if request.method == "POST":
    title = request.form.get("embedtitle")
    desc = request.form.get("embeddesc")
    color = request.form.get("embedcolor")
    link = request.form.get("titlelink")
    givenimage = flask.request.files.get('embedimg', '')
    givenimage.save(f"static/embimg/{''.join(request.access_route[0].split('.')[1:])}.png")
    image = ""
    if not givenimage:
      image = "none"
    else:
      image = f"/static/embimg/{''.join(request.access_route[0].split('.')[1:])}.png"
    if not link:
      link = "https://flaskmsgsendthing.ksiscute.repl.co"
    return redirect(f"https://flaskmsgsendthing.ksiscute.repl.co/embed?title='{title}'&description='{desc}'&color='{color}'&link='{link}'&image='{image}'")
  return render_template("makeembed.html")

@app.route("/ccp")
def ccp():
  if request.args:
    lang = request.args.get("lang")
  else:
    lang = "en"
  return render_template("ccp.html", lang=lang)

def startup():
  app.run("0.0.0.0", port=5000, debug=False) # change if needed

def run():
  t = Thread(target=startup)
  t.start()