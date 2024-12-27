from nicegui import ui
import signin
import login

# Custom CSS for styling
def set_custom_css():
    css = """
    <style>
        /* Change the background color of the button container */
        .navbar-container {
            background-color: #2C3E50;  /* Dark blue-gray background */
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Style the buttons */
        .navbar-container button {
            background-color: #3498DB;  /* Blue button color */
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Hover effect on buttons */
        .navbar-container button:hover {
            background-color: #2980B9;  /* Darker blue on hover */
        }
        
        /* Style the navbar header */
        .navbar-header {
            color: white !important;
            font-family: "Arial", sans-serif;
            font-size: 24px;
            text-align: center;
        }
    </style>
    """
    ui.add_head_html(css)

# Session state to track the current page
current_page = 'home'

# Navigation function
def navigate(page):
    global current_page
    current_page = page

# Home page layout
def home_page():
    set_custom_css()  # Apply custom CSS

    # Header
    ui.label('Welcome to the Chat Sphere!').style('font-size: 2em; text-align: center; color: white;')

    # Button container with 3 columns for Home, Login, Signup buttons
    with ui.row().classes('navbar-container'):
        ui.button('Home', on_click=lambda: navigate('home')).style('width: 100%; max-width: 150px;')
        ui.button('Login', on_click=lambda: navigate('login')).style('width: 100%; max-width: 150px;')
        ui.button('Signup', on_click=lambda: navigate('signup')).style('width: 100%; max-width: 150px;')

    # Show the appropriate page based on navigation
    if current_page == 'login':
        login.login_page()
    elif current_page == 'signup':
        signin.signup_page()

# Run the app
ui.page('/', home_page)
ui.run()
