from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

# Initialize Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app)

rooms = {}

# Method to generate a unique code
def generate_unique_code(length):
    code = "".join(random.choices(ascii_uppercase, k=length))
    if code in rooms:
        return generate_unique_code(length)
    return code

# Home route
@app.route("/", methods=["GET", "POST"])
def home():
    # Clear any existing session data
    session.clear()

    # Extract form data
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        # Validate name input
        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        # If joining a room, validate the room code
        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)

        room = code
        # If creating a room, generate a unique code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}

        # If joining a room and the room does not exist, return an error
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)

        # If joining a room and the room exists, join the room
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    # Render the home page for GET requests
    return render_template("home.html")


# Room route
@app.route("/room")
def room():
    # Make sure the user cannot access the room without a session
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))
    return render_template("room.html", code=room, messages=rooms[room]["messages"])


# Message event
@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "message": data["data"]
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}") # Debugging


# Connect event
@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return

    # Join the room
    join_room(room)
    send({"name": name, "message": "has joined the room."}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} has joined the room {room}.") # Debugging


# Disconnect event
@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name": name, "message": "has left the room."}, to=room)
    print(f"{name} has left the room {room}.") # Debugging


if __name__ == "__main__":
    socketio.run(app, debug=True)
