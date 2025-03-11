# LAN Chat App

This is a LAN Chat Application built using Flask. It allows users to join a chat room, send messages, and upload files.

## Project Structure

```
LAN Chat App/
├── app.py
├── chat_env/
│   ├── pyvenv.cfg
│   ├── bin/
│   ├── include/
│   └── lib/
├── templates/
│   └── index.html
├── uploads/
│   └── <uploaded_files>
└── README.md
```

## Setup

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd LAN Chat App
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv chat_env
    source chat_env/bin/activate  # On Windows use `chat_env\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install flask werkzeug
    ```

## Running the Application

1. Start the Flask application:
    ```sh
    python app.py
    ```

2. Open your web browser and navigate to `http://0.0.0.0:5505` to access the chat application.

## Features

- **Join Chat**: Users can join the chat room by providing a username.
- **Send Messages**: Users can send messages to the chat room.
- **Upload Files**: Users can upload files to the server.
- **Download Files**: Users can download files from the server.
- **Preview Files**: Users can preview uploaded files.
- **Active Users**: View the list of active users in the chat room.

## Routes

- `/` - Home page (chat room)
- `/join` - Join the chat room
- `/leave` - Leave the chat room
- `/send_message` - Send a message
- `/get_messages` - Get all messages
- `/get_active_users` - Get the list of active users
- `/upload_file` - Upload a file
- `/download/<filename>` - Download a file
- `/preview/<filename>` - Preview a file

## Configuration

- **UPLOAD_FOLDER**: Directory where uploaded files are stored (`uploads`)
- **ALLOWED_EXTENSIONS**: Set of allowed file extensions for upload
- **MAX_CONTENT_LENGTH**: Maximum allowed file size (10GB)

## License

This project is licensed under the MIT License.
