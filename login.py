from nicegui import ui
import requests
import base64
import os


def get_image(file):
    with open(file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Custom CSS for styling
def set_custom_css():
    image_path = 'image/login-bg.png'
    if os.path.exists(image_path):
        ui.image(image_path).style("position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;")
    else:
        print("Error: Image not found at the specified path")
    
    css = """
    @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500&display=swap");
    :root {
      --white-color: hsl(0, 0%, 100%);
      --black-color: hsl(0, 0%, 0%);
      --body-font: "Poppins", sans-serif;
      --h1-font-size: 1.75rem;
      --normal-font-size: 1rem;
      --small-font-size: .813rem;
      --font-medium: 500;
    }

    * {
      box-sizing: border-box;
      padding: 0;
      margin: 0;
    }

    body,
    input,
    button {
      font-size: var(--normal-font-size);
      font-family: var(--body-font);
    }

    body {
      color: var(--white-color);
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
      bac.
      kground-size: cover;
      background-position: center;
    }

    input,
    button {
      border: none;
      outline: none;
    }

    a {
      text-decoration: none;
    }

    img {
      max-width: 100%;
      height: auto;
    }

    /*=============== LOGIN ===============*/
    .login {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh; /* Full viewport height */
      width: 100%;
    }

    .login__form {
          background: rgba(255, 255, 255, 0.1);
            padding: 1rem; /* Increased padding */
            border-radius: 15px; /* More rounded corners */
            border: 2px solid #fff;
            width: 500px;
            max-width: 600px; /* Increased width */
            height: 500px;    /* Increased height */
            backdrop-filter: blur(8px);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
    }

    .login__title {
      text-align: center;
      font-size: var(--h1-font-size);
      font-weight: var(--font-medium);
      margin-bottom: 1rem;
    }

    .login__content,
    .login__box {
      display: grid;
    }

    .login__content {
      row-gap: 1.75rem;
      margin-bottom: 1.5rem;
    }

    .login__box {
      grid-template-columns: max-content 1fr;
      align-items: center;
      column-gap: .75rem;
      border-bottom: 2px solid var(--white-color);
    }

    .login__icon,
    .login__eye {
      font-size: 1.25rem;
    }

    .login__input {
      width: 100%;
      padding-block: .8rem;
      background: none;
      color: white !important; /* Force the text color to be white */
      position: relative;
      z-index: 1;
    }

    .login__box-input {
      position: relative;
    }

    .login__label {
      position: absolute;
      left: 0;
      top: 13px;
      font-weight: var(--font -medium);
      transition: top .3s, font-size .3s;
      color: white; /* Set the label text to white */
    }

    .login__eye {
      position: absolute;
      right: 0;
      top: 18px;
      z-index: 10;
      cursor: pointer;
    }

    .login__box:nth-child(2) input {
      padding-right: 1.8rem;
    }

    .login__check,
    .login__check-group {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .login__check {
      margin-bottom: 1.5rem;
    }

    .login__check-label,
    .login__forgot,
    .login__register {
      font-size: var(--small-font-size);
    }

    .login__check-group {
      column-gap: .5rem;
    }

    .login__check-input {
      width: 16px;
      height: 16px;
    }

    .login__forgot {
      color: var(--white-color);
    }

    .login__forgot:hover {
      text-decoration: underline;
    }

    .login__button {
      width: 100%;
      padding: 1rem;
      height:100%;
      border-radius: .5rem;
      background-color: var(--white-color);
      font-weight: var(--font-medium);
      cursor: pointer;
      margin-bottom: 2rem;
    }

    .login__register {
      text-align: center;
    }

    .login__register a {
      color: var(--white-color);
      font-weight: var(--font-medium);
    }

    .login__register a:hover {
      text-decoration: underline;
    }

    .login__input:focus + .login__label {
      top: -12px;
      font-size: var(--small-font-size);
    }

    .login__input:not(:placeholder-shown).login__input:not(:focus) + .login__label {
      top: -12px;
      font-size: var(--small-font-size);
    }

    /*=============== BREAKPOINTS ===============*/
    @media screen and (min-width: 576px) {
      .login__form {
        padding: 4rem 3rem 3.5rem;
        border-radius: 1.5rem;
      }
      .login__title {
        font-size: 4rem;
      }
    }
    """
    ui.add_head_html(f"<style>{css}</style>")

# Function to check user credentials
def check_user_credentials(username, password, users):
    for user in users:
        if user[0] == username and user[1] == password:
            return True
    return False

# Login function
def login():
    set_custom_css()  # Apply custom CSS

    with ui.card().classes('login__form'):
        ui.label('Login to Your Account').style('color: white; font-size: 2.2em; text-align: center;')

        username = ui.input('Username').classes('login__input').style('''
            width: 100%;
            margin-bottom: 10px;
            padding-left:10px;
            height:200px;
            border: 2px solid #fff;
            border-radius: 25px;
            color: white;
            background-color: transparent;
        ''').props('label-color=white clearable input-class=text-white autocomplete=off spellcheck=false')
       
        password = ui.input('Password', password=True).classes('login__input').style('''
            width: 100%;
         margin-bottom: 10px;
            padding-left:10px;
            border: 2px solid #fff;
                height:200px;
            border-radius: 25px;
            color: white;
            background-color: transparent;
        ''').props('label-color=white clearable input-class=text-white autocomplete=off spellcheck=false')
       

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

        ui.button('Login', on_click=handle_login).classes('login__button')

login()

# Run the NiceGUI app
ui.run(port=8005)