from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    message_counter = 0
    try:
        while True:
            data = await websocket.receive_text()
            try:
                request_data = json.loads(data)
                user_message = request_data.get("message", "")
            except:
                continue
            message_counter += 1
            response_data = {
                "number": message_counter,
                "message": user_message
            }
            await websocket.send_text(json.dumps(response_data))
    except Exception as e:
        print(f"WebSocket closed: {e}")
