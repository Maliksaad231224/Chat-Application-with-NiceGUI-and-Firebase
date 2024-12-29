from datetime import datetime
from typing import List, Tuple
from uuid import uuid4

from nicegui import ui

messages: List[Tuple[str, str, str, str]] = []


@ui.refreshable
def chat_messages(own_id: str) -> None:
    if messages:
        for user_id, avatar, text, stamp in messages:
            ui.chat_message(text=text, stamp=stamp, avatar=avatar, sent=own_id == user_id)
    else:
        ui.label('No messages yet').classes('mx-auto my-36')
    ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')  # Scroll to the latest message


@ui.page('/')
async def main():
    def send() -> None:
        stamp = datetime.now().strftime('%X')
        messages.append((user_id, avatar, text.value, stamp))
        text.value = ''
        chat_messages.refresh()

    user_id = str(uuid4())
    avatar = f'https://robohash.org/{user_id}?bgset=bg2'

    # Add the CSS for the background and UI
    ui.add_css(r'''
        @keyframes move { 100% { transform: translate3d(0, 0, 1px) rotate(360deg); } }
        @keyframes flowBackground { 0% { background: linear-gradient(45deg, rgba(227,114,103,255), rgba(179,97,97,255), #034652, #05636f); background-position: 0 0; } 50% { background-position: 100% 100%; } 100% { background-position: 0 0; } }
        .background { position: fixed; width: 100vw; height: 100vh; animation: flowBackground 10s ease-in-out infinite; top: 0; left: 0; background: linear-gradient(to bottom, rgba(227,114,103,255), rgba(179,97,97,255), #034652, #05636f); overflow: hidden; z-index: -1; }
        .background span { width: 20vmin; height: 20vmin; border-radius: 20vmin; backface-visibility: hidden; position: absolute; animation: move; animation-duration: 45s; animation-timing-function: linear; animation-iteration-count: infinite; }
        .message-bar { height: 60px; padding: 0 15px; border: none; border-radius: 25px; background-color: white; font-size: 16px; width: 45%; margin: auto; display: block; }
        .logo { width: 50px; height: 50px; border-radius: 50%; }
        .footer { background: none; padding: 10px; position: fixed; bottom: 10px; left: 0; width: 100%; display: flex; align-items: center; gap: 10px; }
    ''')

    # Add background HTML to the page
    with ui.element('div').classes('background'):
        for _ in range(6):
            ui.element('span')
    ui.add_body_html('''<div id="particles-js" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0;"></div>
        <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
        <script>
            particlesJS("particles-js", {
                "particles": {
                    "number": {
                        "value": 200,
                        "density": { "enable": true, "value_area": 800 }
                    },
                    "color": { "value": "#e8e7df" },
                    "shape": { "type": "circle", "stroke": { "width": 0, "color": "#000000" } },
                    "opacity": {
                        "value": 0.5,
                        "random": false,
                        "anim": { "enable": true, "speed": 1, "opacity_min": 0.1, "sync": false }
                    },
                    "size": {
                        "value": 3,
                        "random": true,
                        "anim": { "enable": true, "speed": 40, "size_min": 0.1, "sync": false }
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
                        "attract": { "enable": false, "rotateX": 600, "rotateY": 1200 }
                    }
                },
                "interactivity": {
                    "detect_on": "window",
                    "events": {
                        "onhover": { "enable": true, "mode": "repulse" },
                        "onclick": { "enable": true, "mode": "push" }
                    }
                }
            });
        </script>''')
    # UI layout for the chat
    with ui.footer().classes('footer'):
            ui.image(avatar).classes('logo')
            text = ui.input(placeholder='Type your message here...').on('keydown.enter', send) \
            .props('label-color=white clearable input-class=text-white autocomplete=off spellcheck=false').classes('text-input').style(''' 
            height: 63px; padding: 6px 15px; border: 2px solid #fff; border-radius: 25px; color: white; background-color: transparent; font-size: 19px; width: 50%; margin: 0 auto 10px; display: block;
        ''')

    await ui.context.client.connected()  # chat_messages(...) uses run_javascript which is only possible after connecting
    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        chat_messages(user_id)


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(port=8007)
