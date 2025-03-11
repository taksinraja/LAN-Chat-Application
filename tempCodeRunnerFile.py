from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# Upload folder configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx',
    'mp4', 'webm', 'avi', 'mov', 'mkv', '3gp', 'flv'
}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 * 1024  # 10GB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_video_file(filename):
    video_extensions = {'mp4', 'webm', 'avi', 'mov', 'mkv', '3gp', 'flv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in video_extensions

# File upload route
@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'})
    
    file = request.files['file']
    username = request.form.get('username')
    message = request.form.get('message', '')
    
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        saved_filename = timestamp + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], saved_filename))
        
        file_type = filename.rsplit('.', 1)[1].lower()
        is_video = is_video_file(filename)
        
        messages.append({
            'type': 'file',
            'username': username,
            'message': message,
            'filename': saved_filename,
            'original_filename': filename,
            'file_type': file_type,
            'is_video': is_video,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
        
        return jsonify({'status': 'success', 'filename': filename})
    
    return jsonify({'status': 'error', 'message': 'File type not allowed'})

# File download route
@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True,
            download_name=filename.split('_', 2)[2]  # Remove timestamp prefix
        )
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Store messages and active users
messages = []
active_users = set()

# Root route add kiya hai
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/join', methods=['POST'])
def join_chat():
    username = request.form.get('username')
    is_refresh = request.form.get('is_refresh') == 'true'  # Check if it's a page refresh
    
    if username in active_users:
        if is_refresh:  # If it's a refresh, allow same user
            return jsonify({'status': 'success'})
        return jsonify({'status': 'error', 'message': 'Username already taken!'})
    
    active_users.add(username)
    
    # Only add system message if it's not a refresh
    if not is_refresh:
        messages.append({
            'type': 'system',
            'message': f'{username} has joined the chat!',
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
    
    return jsonify({'status': 'success'})

@app.route('/leave', methods=['POST'])
def leave_chat():
    username = request.form.get('username')
    is_refresh = request.form.get('is_refresh') == 'true'
    
    if username in active_users:
        active_users.remove(username)
        
        # Only add system message if it's not a refresh
        if not is_refresh:
            messages.append({
                'type': 'system',
                'message': f'{username} has left the chat!',
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })
    
    return jsonify({'status': 'success'})

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message')
    username = data.get('username')
    reply_to = data.get('replyTo')
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    message_data = {
        'id': len(messages),  # Simple ID generation
        'username': username,
        'message': message,
        'timestamp': timestamp,
        'type': 'message'
    }
    
    if reply_to:
        message_data['replyTo'] = reply_to
    
    messages.append(message_data)
    
    return jsonify({'status': 'success'})

@app.route('/get_messages')
def get_messages():
    return jsonify(messages)

@app.route('/get_active_users')
def get_active_users():
    return jsonify(list(active_users))

@app.route('/preview/<filename>')
def preview_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        return send_file(file_path)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5505, debug=True) 