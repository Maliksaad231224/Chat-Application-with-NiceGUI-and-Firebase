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
      background-size: cover;
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
      background-color: hsla(0, 0%, 10%, .1);
      border: 2px solid var(--white-color);
      padding: 2.5rem 2rem; /* Increased padding */
      border-radius: 1rem;
      backdrop-filter: blur(8px);
      width: 100%;
      max-width: 600px; /* Increased the max width */
      height: 400px; /* Increased height */
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
       width: 80%; /* Adjust width to make it less wide */
    padding: 0.8rem; /* Decrease padding to make the button shorter */
    border-radius: 0.5rem; /* Keep the rounded corners */
    background-color: var(--white-color);
    font-weight: var(--font-medium);
    cursor: pointer;
    margin-top: 1.5rem; /* Add top margin to move the button lower */
    margin-bottom: 1rem; /* Adjust bottom margin */
    font-size: 1rem; /* Adjust font size */
    text-align: center; /* Center text in the button */
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
    
            .text-input-wrapper {
            display: flex;
            align-items: center;
            width: 80%;
            margin-bottom: 10px;
            border: 2px solid #fff;
            border-radius: 25px;
            background-color: transparent;
            color:white;
       }

        .text-input-wrapper img {
            width: 20px;
            height: 20px;
            margin-left: 10px;
            color:white;
        }
        .text-input username{
            color = white;
        }
        .text-input-wrapper input {
            flex: 1;
            color:white;
            border: none;
            outline: none;
            padding-left: 10px;
            background-color: transparent;
            color: white;
            font-size: 1rem;
            border-radius: 25px;
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
        ui.label('Login to Your Account').style('color: white; font-size: 1.2em; text-align: center;')

        username = ui.input(placeholder='Username').classes('text-input').style('''
            width: 100%;
            margin-bottom: 10px;
            padding-left:10px;
            border: 2px solid #fff;
            border-radius: 25px;
            color: white;
        ''').props('label-color=cyan-8 clearable input-class=text-white')
        password = ui.input(placeholder='Password', password=True, password_toggle_button=True).classes('text-input').style('''
            width: 100%;
            margin-bottom: 10px;
            padding-left:10px;
            border: 2px solid #fff;
            border-radius: 25px;
            color: white;
            box-sizing: border-box; 
        ''').props('label-color=cyan-8 clearable input-class=text-white')

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