from bottle import route, run, template, redirect, static_file, request
import json

#Function to read data from "wiki.json"
def get_info_from_file():
    try:
        with open("python för healhub/static/wiki.json", "r") as my_file:
            info = json.load(my_file)
        return info
    except FileNotFoundError:
        with open("static/wiki.json", "w") as my_file:
            json.dump([], my_file)
        return []

#Function to generate a unique ID for new entries
def create_id(info):
    highest_id = 1
    for entry in info:
        if entry["id"] >= highest_id:
            highest_id = entry["id"] + 1
    return highest_id

#Route to serve the index page
@route("/")
def index():
    info = get_info_from_file()
    return template("python för healhub/views/index.html", info=info)

#Route to serve static CSS files
@route("/python för healhub/static/css/<filename>")
def serve_css(filename):
    return static_file(filename, root="python för healhub/static/css")

#Additional route to serve the second CSS file (style3.css)
@route("/python för healhub/static/css/style3.css")
def serve_css3():
    return static_file("style3.css", root="python för healhub/static/css")

#Route to handle saving new entries
@route("/save/", method="POST")
def save_info():
    title = request.forms.get("title")
    article = request.forms.get("article")

    info = get_info_from_file()
    id = create_id(info)

    info.append({
        "title": title,
        "article": article,
        "id": id
    })

    with open("static/wiki.json", "w") as my_file:
        json.dump(info, my_file, indent=4)

    redirect("/")

#Run the server
if __name__ == "__main__":
    run(host="127.0.0.1", port=8080, debug=True)