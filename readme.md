# Flask Chat App

This is a lightweight chat application built to practice Flask and SocketIO.
It allows users to create or join chat rooms using unique room codes, providing a minimalistic yet efficient platform for real-time communication.

## Features

- **Room Creation:** Users can create a new chat room that generates a unique code.
- **Join Room:** Users can join an existing chat room by entering its unique code.
- **Real-time Messaging:** Leveraging Flask-SocketIO for real-time messaging within chat rooms.
- **Session Management:** Manages user sessions to ensure that messages are sent and received by the correct user in the correct room.

## Technologies

- **Flask:** A micro web framework written in Python.
- **Flask-SocketIO:** Flask extension that provides WebSocket communications between clients and the server.
- **HTML & CSS:** For structuring and styling the web interface.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

- Python 3.x
- Flask
- Flask-SocketIO

You can install Flask and Flask-SocketIO using pip:

```sh
pip install Flask Flask-SocketIO
```

Clone the repository, navigate to the project directory, and run the application

```sh
python main.py
```

This will start the Flask server, and you should be able to access the application at http://127.0.0.1:5000/ on your browser.

## Future Improvements


Several features can improve the overall functionality, including user authentication, private rooms, persistent storage, a notification system, end-to-end
encryption, etc. A notable issue in the current version is the distortion of message timestamps upon page refresh. This occurs because message timestamps are
generated based on the receiver's local time when displayed, rather than being preserved from the sender's original message data.