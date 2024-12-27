from uuid import uuid4
from nicegui import ui
import os

image_path = 'image/login-bg.png'

# Check if the background image exists, then apply it as a background
if os.path.exists(image_path):
    ui.image(image_path).style("position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;")
else:
    print("Error: Image not found at the specified path")

messages = []

@ui.refreshable
def chat_messages(own_id):
    for user_id, avatar, text in messages:
        ui.chat_message(avatar=avatar, text=text, sent=user_id==own_id)

@ui.page('/')
def index():
    def send():
        messages.append((user, avatar, text.value))
        chat_messages.refresh()
        text.value = ''

    user = str(uuid4())
    avatar = f'https://robohash.org/{user}?bgset=bg2'
    with ui.column().classes('w-full items-stretch'):
        chat_messages(user)

    with ui.footer().classes('bg-white'):
        with ui.row().classes('w-full items-center'):
            with ui.avatar():
                ui.image(avatar)
            text = ui.input(placeholder='message') \
                .props('rounded outlined').classes('flex-grow') \
                .on('keydown.enter', send)

ui.run()