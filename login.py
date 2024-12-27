from nicegui import ui
import requests
import base64



# Background image setup (NiceGUI requires custom CSS for styling)
def set_background():
    
    css = f"""
    <style>
    body {{
        
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;
    }}
    h1, h3 {{
        color: white !important;
    }}
    .nicegui-button {{
        background-color: blue;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
    }}
    .nicegui-input {{
        color: black;
    }}
    .nicegui-textarea {{
        color: white;
        border: 1px solid #333;
        border-radius: 5px;
    }}
    p {{
        color: white !important;
        font-family: "Times New Roman", Times, serif;
        font-size: 1.3em;
    }}
    .container {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background: rgba(0, 0, 0, 0.7);
        border: 3px solid #0078D4;
        border-radius: 10px;
        padding: 30px;
        margin-top: 20px;
    }}
    </style>
    """
    ui.add_head_html(css)

# Function to check user credentials
def check_user_credentials(username, password, users):
    for user in users:
        if user[0] == username and user[1] == password:
            return True
    return False

# Login function
def login():
    set_background()  # Apply background and custom styling

    with ui.card().classes('container'):

        ui.label('Welcome to Chat Sphere').style('color: white; font-size: 2em; text-align: center;')
        ui.label('Login to Your Account').style('color: white; font-size: 1.5em; text-align: center;')

        username = ui.input(placeholder='Username').style('width: 100%; max-width: 350px;').classes('nicegui-input')
        password = ui.input(placeholder='Password', password=True).style('width: 100%; max-width: 350px;').classes('nicegui-input')

        def handle_login():
            urll = "http://127.0.0.1:8004/"
            response = requests.get(urll)
            if response.status_code == 200:
                data = response.json()
                users = data['users']
                if check_user_credentials(username.value, password.value, users):
                    ui.notify('Login successful!', type='positive')
                else:
                    ui.notify('Incorrect username or password.', type='negative')
            else:
                ui.notify('Unable to fetch data', type='error')

        # Login button with centered text
        ui.button('Login', on_click=handle_login).style('margin-top: 20px; width: 35%; max-width: 350px;').classes('nicegui-button')

login()
# Run the NiceGUI app
ui.run(port=8005)