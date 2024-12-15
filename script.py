# Import necessary libraries
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn
import threading
import streamlit as st

# FastAPI App
app = FastAPI()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: #ECE5DD;
        }

        .chat-container {
            max-width: 400px;
            margin: 30px auto;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .chat-header {
            background-color: #075E54;
            color: #FFF;
            padding: 15px;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
        }

        .chat-messages {
            flex-grow: 1;
            padding: 10px;
            overflow-y: auto;
            background-color: #FFFFFF;
        }

        .chat-messages ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
        }

        .chat-messages li {
            margin: 10px 0;
            padding: 10px;
            border-radius: 20px;
            max-width: 75%;
            word-wrap: break-word;
        }

        .chat-messages li.sent {
            background-color: #DCF8C6;
            align-self: flex-end;
            margin-left: auto;
        }

        .chat-messages li.received {
            background-color: #FFF;
            border: 1px solid #ECE5DD;
            align-self: flex-start;
        }

        .chat-footer {
            background-color: #F6F6F6;
            padding: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .chat-footer input {
            flex-grow: 1;
            border: 1px solid #DDD;
            border-radius: 20px;
            padding: 10px 15px;
            outline: none;
        }

        .chat-footer button {
            background-color: #25D366;
            color: #FFF;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
        }

        .chat-footer button:hover {
            background-color: #20B85D;
        }

        .chat-footer button:active {
            background-color: #1B9E52;
        }

        ::-webkit-scrollbar {
            width: 5px;
        }

        ::-webkit-scrollbar-thumb {
            background-color: #888;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background-color: #555;
        }

    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">Chat</div>
        <div class="chat-messages" id="messages">
            <ul></ul>
        </div>
        <div class="chat-footer">
            <input type="text" id="messageText" placeholder="Type a message..." autocomplete="off" />
            <button onclick="sendMessage(event)">💬</button>
        </div>
    </div>

    <script>
        var client_id = Date.now();
        var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);

        ws.onmessage = function(event) {
            var messages = document.querySelector('#messages ul');
            var message = document.createElement('li');
            message.textContent = event.data;
            if (event.data.includes("Client #" + client_id)) {
                message.classList.add('sent');
            } else {
                message.classList.add('received');
            }
            messages.appendChild(message);
            messages.scrollTop = messages.scrollHeight;
        };

        function sendMessage(event) {
            var input = document.getElementById("messageText");
            if (input.value.trim() !== "") {
                ws.send(input.value);
                input.value = '';
            }
            event.preventDefault();
        }
    </script>
</body>
</html>
"""

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try: 
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} has left the chat")

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

thread = threading.Thread(target=run_fastapi, daemon=True)
thread.start()
st.components.v1.html(html, height=600)
