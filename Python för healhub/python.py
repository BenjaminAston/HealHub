from bottle import route, run, template, redirect, static_file, request
import json

'''Retunerar en lista av titlar och artiklarna från filen: "wiki.json" '''
def get_info_from_file():
    try:
        with open("python för healhub/static/wiki.json", "r") as my_file:
            info = json.load(my_file)
        return info
    except FileNotFoundError:
        with open("static/wiki.json", "w") as my_file:
            json.dump([], my_file)
        return []

# Funktion som genererar ett unikt ID till nya "entries"
def create_id(info):
    """
    Retunerar en integer som representerar det nuvarande högsta id + 1 
    
    Retunerar
        int : det nuvarande högsta id + 1 
    """
    highest_id = 1
    for entry in info:
        if entry["id"] >= highest_id:
            highest_id = entry["id"] + 1
    return highest_id

# Route som tar en till huvud sidan (index)
@route("/")
def index():
    info = get_info_from_file()
    return template("python för healhub/views/index.html", info=info)

# Route som tar en till huvud.html
@route("/om-oss.html")
def serve_om_oss():
    return template("python för healhub/views/om-oss.html")
# Route som tar en till huvud.html
@route("/huvud.html")
def serve_huvud():
    return template("python för healhub/views/huvud.html")

# Route som tar en till vaxel.html (vänster axel)
@route("/vaxel.html")
def serve_vaxel():
    return template("python för healhub/views/vaxel.html")

# Route som tar en till haxel.html (höger axel)
@route("/haxel.html")
def serve_haxel():
    return template("python för healhub/views/haxel.html")

# Route som tar en till bröst.html
@route("/bröst.html")
def serve_bröst():
    return template("python för healhub/views/bröst.html")

# Route som tar en till varm.html (vänster arm)
@route("/varm.html")
def serve_varm():
    return template("python för healhub/views/varm.html")

# Route som tar en till harm.html (höger arm)
@route("/harm.html")
def serve_harm():
    return template("python för healhub/views/harm.html")

# Route som tar en till mage.html
@route("/mage.html")
def serve_mage():
    return template("python för healhub/views/mage.html")

# Route som tar en till vben.html (vänster ben)
@route("/vben.html")
def serve_vben():
    return template("python för healhub/views/vben.html")

# Route som tar en till hben.html (höger ben)
@route("/hben.html")
def serve_hben():
    return template("python för healhub/views/hben.html")

# Route som tar en till vhand.html (vänster hand)
@route("/vhand.html")
def serve_vhand():
    return template("python för healhub/views/vhand.html")

# Route som tar en till hhand.html (höger hand)
@route("/hhand.html")
def serve_hhand():
    return template("python för healhub/views/hhand.html")

# Route som tar en till vfot.html (vänster fot)
@route("/vfot.html")
def serve_vfot():
    return template("python för healhub/views/vfot.html")

# Route som tar en till hfot.html (höger fot)
@route("/hfot.html")
def serve_hfot():
    return template("python för healhub/views/hfot.html")

# Route till static CSS fil
@route("/python för healhub/static/css/<filename>")
def serve_css(filename):
    return static_file(filename, root="python för healhub/static/css")

# En till route till den andra CSS filen (style3.css)
@route("/python för healhub/static/css/style3.css")
def serve_css3():
    return static_file("style3.css", root="python för healhub/static/css")

# Route till kontakta oss.html
@route("/kontakta-oss")
def serve_kontakta_oss():
    return template("python för healhub/views/kontakta oss.html")

# Route till övningar.html
@route("/ovningar")
def serve_ovningar():
    return template("python för healhub/views/övningar.html")

# Route till tack.html
@route("/tack")
def serve_tack():
    return template("python för healhub/views/tack.html")

# Route till tipsa övningar.html
@route("/tipsa-ovningar")
def serve_tipsa_ovningar():
    return template("python för healhub/views/tipsa övningar.html")

# Route till Fysioterapeut.html
@route("/Fysioterapeut")
def serve_fysioterapeut():
    return template("python för healhub/views/Fysioterapeut.html")

@route("/Login")
def Login():
    return template("python för healhub/views/Login.html")

# Kör servern
if __name__ == "__main__":
    run(host="127.0.0.1", port=8080, debug=True)