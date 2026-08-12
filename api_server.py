import json
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def bypass_ngrok_interceptor(request: Request, call_next):
    response = await call_next(request)
    response.headers["ngrok-skip-browser-warning"] = "true"
    response.headers["X-Ngrok-Skip-Browser-Warning"] = "true"
    return response

@app.post("/chat/completions")
async def vapi_chat_endpoint(request: Request):
    """
    OpenAI-compliant streaming endpoint to handle custom voice chat.
    Sends text segments chunk-by-chunk to guarantee a stable phone connection.
    """
    try:
        body = await request.json()
        print("📥 Incoming Request Payload from Vapi Framework:", json.dumps(body))
    except Exception:
        pass

    async def response_generator():
        reply_text = (
            "Thanks for checking out BizStack Perks! Our system dashboard is fully live and "
            "running local terminal workflows. How can I help you scale your business operations today?"
        )
        words = reply_text.split()
        
        # 1. Stream individual text tokens to feed the voice engine instantly
        for i, word in enumerate(words):
            chunk = {
                "id": "chatcmpl-bizstackbot",
                "object": "chat.completion.chunk",
                "choices": [{
                    "delta": {
                        "role": "assistant",
                        "content": word + " "
                    },
                    "index": 0,
                    "finish_reason": None
                }]
            }
            yield f"data: {json.dumps(chunk)}\n\n"
            await asyncio.sleep(0.05)  # Natural pacing to secure stable audio buffering

        # 2. Emit clean, empty stopping block to signify data closure safely
        stop_chunk = {
            "id": "chatcmpl-bizstackbot",
            "object": "chat.completion.chunk",
            "choices": [{
                "delta": {},
                "index": 0,
                "finish_reason": "stop"
            }]
        }
        yield f"data: {json.dumps(stop_chunk)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(response_generator(), media_type="text/event-stream")

@app.post("/vapi/webhook")
async def vapi_webhook_endpoint(request: Request):
    try:
        payload = await request.json()
        print("📊 Telephony Status Event Received:", json.dumps(payload))
    except Exception:
        pass
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
