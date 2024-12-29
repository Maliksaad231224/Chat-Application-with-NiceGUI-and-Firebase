from datetime import datetime
from typing import List, Tuple
from uuid import uuid4
from nicegui import ui

messages: List[Tuple[str, str, str, str]] = []


# This function handles the chat page.
def chat_app():
    @ui.refreshable
    def chat_messages(own_id: str) -> None:
        if messages:
            for user_id, avatar, text, stamp in messages:
                ui.chat_message(text=text, stamp=stamp, avatar=avatar, sent=own_id == user_id)
        else:
            ui.label('No messages yet').classes('mx-auto my-36')
        ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')  # Scroll to the latest message

    def send() -> None:
        stamp = datetime.now().strftime('%X')
        messages.append((user_id, avatar, text.value, stamp))
        text.value = ''
        chat_messages.refresh()

    user_id = str(uuid4())
    avatar = f'https://robohash.org/{user_id}?bgset=bg2'

    # Add the CSS for the background and UI
    ui.add_css(r'''
    @keyframes move {
        100% {
            transform: translate3d(0, 0, 1px) rotate(360deg);
        }
    }

    .background {
        position: fixed;
        width: 100vw;
        height: 100vh;
        top: 0;
        left: 0;
        background: linear-gradient(to bottom, #eb6f61, rgba(4, 123, 131, 255)); /* Gradient Background */
        overflow: hidden;
        z-index: -1;
    }

    .background span {
        width: 20vmin;
        height: 20vmin;
        border-radius: 20vmin;
        backface-visibility: hidden;
        position: absolute;
        animation: move;
        animation-duration: 45s;
        animation-timing-function: linear;
        animation-iteration-count: infinite;
    }

    .background span:nth-child(1) {
        color:rgb(54, 101, 163);
        top: 29%;
        left: 50%;
        animation-duration: 43s;
        animation-delay: -32s;
        transform-origin: -10vw -20vh;
        box-shadow: 40vmin 0 5.582692717129818vmin currentColor;
    }
    .background span:nth-child(2) {
        color:rgb(221, 106, 106);
        top: 77%;
        left: 85%;
        animation-duration: 20s;
        animation-delay: -42s;
        transform-origin: 22vw -17vh;
        box-shadow: 40vmin 0 5.185934412044379vmin currentColor;
    }
    .background span:nth-child(3) {
        color:rgb(212, 233, 235);
        top: 1%;
        left: 87%;
        animation-duration: 17s;
        animation-delay: -41s;
        transform-origin: 1vw -20vh;
        box-shadow: -40vmin 0 5.636897113325926vmin currentColor;
    }
    .background span:nth-child(4) {
        color:rgb(163, 4, 52);
        top: 5%;
        left: 92%;
        animation-duration: 16s;
        animation-delay: -36s;
        transform-origin: -12vw -20vh;
        box-shadow: -40vmin 0 5.516657450968793vmin currentColor;
    }
    .background span:nth-child(5) {
        color:rgb(181, 152, 231);
        top: 52%;
        left: 13%;
        animation-duration: 25s;
        animation-delay: -9s;
        transform-origin: 2vw -12vh;
        box-shadow: -40vmin 0 5.444425787919456vmin currentColor;
    }
    .background span:nth-child(6) {
        color:rgb(255, 104, 58);
        top: 84%;
        left: 9%;
        animation-duration: 44s;
        animation-delay: -41s;
        transform-origin: -10vw 10vh;
        box-shadow: 40vmin 0 5.626623067703448vmin currentColor;
    }

    .message-bar {
        height: 60px; /* Height for better alignment */
        padding: 0 15px; /* Center text */
        border: none; /* Remove outline */
        border-radius: 25px; /* Fully rounded corners */
        background-color: white; /* Neutral background for better visibility */
        font-size: 16px; /* Better readability */
        width: 45%; /* Adjust the width to be smaller (e.g., 70% of the parent container) */
        margin: auto; /* Centers the message bar horizontally */
        display: block; /* Ensure the element behaves like a block-level element */
    }

    .logo {
        width: 50px;
        height: 50px;
        border-radius: 50%;
    }

    .footer {
        background: none;
        padding: 10px;
        position: fixed;
        bottom: 10px; /* Adds space from the bottom of the screen */
        left: 0;
        width: 100%;
        display: flex;
        align-items: center; /* Align logo and input box vertically */
        gap: 10px;
    }
    ''')

    # Add background HTML and particles container to the page
    with ui.element('div').classes('background'):
        for _ in range(6):
            ui.element('span')

    # Add particles.js script and initialization
    ui.add_body_html('''<div id="particles-js" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0;"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS("particles-js", {
            "particles": {
                "number": {
                    "value": 200,
                    "density": {
                        "enable": true,
                        "value_area": 800
                    }
                },
                "color": {
                    "value": "#e8e7df"
                },
                "shape": {
                    "type": "circle",
                    "stroke": {
                        "width": 0,
                        "color": "#000000"
                    }
                },
                "opacity": {
                    "value": 0.5,
                    "random": false,
                    "anim": {
                        "enable": true,
                        "speed": 1,
                        "opacity_min": 0.1,
                        "sync": false
                    }
                },
                "size": {
                    "value": 3,
                    "random": true,
                    "anim": {
                        "enable": true,
                        "speed": 40,
                        "size_min": 0.1,
                        "sync": false
                    }
                },
                "line_linked": {
                    "enable": true,
                    "distance": 150,
                    "color": "#dedbcf",
                    "opacity": 0.4,
                    "width": 3
                },
                "move": {
                    "enable": true,
                    "speed": 6,
                    "direction": "none",
                    "random": false,
                    "straight": false,
                    "out_mode": "out",
                    "bounce": false,
                    "attract": {
                        "enable": false,
                        "rotateX": 600,
                        "rotateY": 1200
                    }
                }
            },
            "interactivity": {
                "detect_on": "window",
                "events": {
                    "onhover": {
                        "enable": true,
                        "mode": "repulse"
                    },
                    "onclick": {
                        "enable": true,
                        "mode": "push"
                    }
                }
            }
        });
    </script>
    ''')

    # UI layout for the chat interface
    with ui.footer().classes('footer'):
        ui.image(avatar).classes('logo')
        text = ui.input(placeholder='Type your message here...').on('keydown.enter', send) \
            .props('rounded').classes('message-bar')

    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        chat_messages(user_id)

# Set up the /chat route
@ui.page('/chat')
def chat():
    return chat_app()


# Run the app
if __name__ == "__main__":
    ui.run(port=8000)
