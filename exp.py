from uuid import uuid4
from nicegui import ui
import os

# Path to the background image
image_path = 'image/login-bg.png'

# Check if the background image exists and apply it as a background
if os.path.exists(image_path):
    ui.image(image_path).style("position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;")
else:
    print("Error: Image not found at the specified path")

# Initialize an empty list to store chat messages
messages = []

# Define a function to render chat messages with dynamic class binding
@ui.refreshable
def chat_messages(own_id):
    with ui.scrollable().style('height: 400px; overflow-y: auto; margin-bottom: 60px;'):
        for user_id, avatar, text in messages:
            message_class = 'sent' if user_id == own_id else 'received'
            with ui.row().classes(f'chat-message {message_class}').style('margin-bottom: 10px; padding: 10px;'):
                ui.image(avatar).classes('avatar')
                ui.label(text).classes('message-content')

# Main page for the app
@ui.page('/')
def index():
    def send():
        # Add the message to the list with the current user, avatar, and text
        messages.append((user, avatar, text.value))
        # Refresh the chat messages
        chat_messages.refresh()
        # Clear the text input field after sending the message
        text.value = ''

    # Create a unique user ID and avatar
    user = str(uuid4())
    avatar = f'https://robohash.org/{user}?bgset=bg2'

    # Create the main chat layout
    with ui.column().classes('w-full items-stretch'):
        # Display the chat messages for the current user
        chat_messages(user)

    # Create the footer with the message input field
    with ui.footer().classes('bg-white p-4 shadow-md'):
        with ui.row().classes('w-full items-center justify-between'):
            with ui.avatar().style('width: 40px; height: 40px; margin-right: 10px'):
                ui.image(avatar)
            # Create an input field for the message
            text = ui.input(placeholder='Type your message...') \
                .props('rounded outlined') \
                .classes('flex-grow') \
                .on('keydown.enter', send) \
                .style('border-radius: 20px; padding: 10px; font-size: 16px;')

    # Inject styles for the chat messages
    ui.html("""
    <style scoped>
        /* Background and layout */
        body {
            font-family: 'Arial', sans-serif;
        }

        .chat-message {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            font-size: 14px;
            max-width: 80%;
            border-radius: 8px;
            background-color: #f0f0f0;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .sent {
            justify-content: flex-end;
            background-color: #d0e8f4;
        }

        .received {
            justify-content: flex-start;
            background-color: #f0f0f0;
        }

        .avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 10px;
        }

        .message-content {
            color: #555;
            padding: 5px 10px;
            border-radius: 8px;
        }

        /* Footer input styling */
        .footer {
            background-color: #ffffff;
            padding: 10px;
            border-top: 1px solid #ddd;
        }

        .input-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
    </style>
    """)

# Run the application
ui.run()
