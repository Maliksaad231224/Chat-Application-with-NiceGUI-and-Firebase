from nicegui import ui
from login import login_page
from signin import signup_page
from chat import chat_app

@ui.page('/')
def home():
    return signup_page()
    
@ui.page('/login')
def login():
    return login_page()

@ui.page('/signin')
def signin():
    return signup_page()

@ui.page('/chatpage')
def chat():
    return chat_app()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(port=8000)