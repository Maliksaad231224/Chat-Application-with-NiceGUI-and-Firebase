#!/usr/bin/env python3
from google.generativeai import GenerativeModel
from uuid import uuid4
from nicegui import ui
import google.generativeai as genai
from google.generativeai.types.generation_types import StopCandidateException

# Gemini API Key (replace with your actual key)
GOOGLE_API_KEY = "AIzaSyCS3BW1hhPOSX6OmGqYu-tIMKj7UniLMZw"

# Configure the Gemini API with the provided API key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

messages = []

# UI for displaying chat messages
@ui.refreshable
def chat_messages() -> None:
    if messages:
        for message in messages:
            ui.chat_message(text=message['text'], stamp=message['stamp'], avatar=message['avatar_url'], sent=message['author'] == 'user')
    else:
        ui.label('No messages yet').classes('mx-auto my-36')
    ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')

# Main UI page setup
@ui.page('/')
async def main():
    def send() -> None:
        question = text.value
        text.value = ''  # Clear the input field

        # Add the user message to the list
        user_message = {
            'author': 'user',
            'text': question,
            'stamp': '',
            'avatar_url': f'https://robohash.org/{uuid4()}?bgset=bg2'
        }
        messages.append(user_message)
        chat_messages.refresh()  # Refresh UI to display user's message

        try:
            # Convert the message history to the expected format for the API
            formatted_history = [{'parts': [{'text': msg['text']}] } for msg in messages]

            # Send the question to Gemini model and retrieve the response
            response = model.start_chat(history=formatted_history).send_message(question)
            
            # Add the bot's response to the message list
            bot_message = {
                'author': 'bot',
                'text': response.text,
                'stamp': '',
                'avatar_url': f'https://robohash.org/bot?bgset=bg2'
            }
            messages.append(bot_message)
        except StopCandidateException:
            # Handle the case where the model cannot generate a response
            bot_message = {
                'author': 'bot',
                'text': 'Sorry, I could not generate a response.',
                'stamp': '',
                'avatar_url': f'https://robohash.org/bot?bgset=bg2'
            }
            messages.append(bot_message)

        chat_messages.refresh()  # Refresh UI to display bot's response

    # Input field for the user
    ui.add_css(r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}')
    
    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            text = ui.input(placeholder='Type your message...').on('keydown.enter', send) \
                .props('rounded outlined input-class=mx-3').classes('flex-grow')
        ui.markdown('Chat with Gemini powered by [Google Generative AI](https://cloud.google.com/ai)') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary')

    await ui.context.client.connected()  # Ensure UI is connected before running JavaScript
    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        chat_messages()

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(port=8007)
