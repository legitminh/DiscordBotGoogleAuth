# cloudflared tunnel --url http://localhost:8000 
"""
Backup backend development build code:
    uvicorn backend:app --reload --host 0.0.0.0 --port 8000 
"""
from fastapi import FastAPI, Request
import uvicorn
# from pyngrok import ngrok
from pydantic import BaseModel
import logging
import json

# configure simple logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("supabase-receiver")

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "recieved data from supabase!!!"}


@app.post("/")
async def receive_root(request: Request):
    """
    Accept and log whatever Supabase (or any webhook) sends to POST /
    This prevents 405s and records headers / body so you can inspect the incoming request.
    """
    client = request.client.host if request.client else "unknown"
    method = request.method
    headers = dict(request.headers)

    # raw body
    body_bytes = await request.body()
    body_text = None
    parsed = None
    try:
        # try JSON first
        parsed = await request.json()
        body_text = json.dumps(parsed, ensure_ascii=False)
    except Exception:
        try:
            # fallback to plain text
            body_text = body_bytes.decode(errors="replace")
        except Exception:
            body_text = repr(body_bytes)
    print(f"Incoming request: method={method} client={client}")
    print(f"Headers: {json.dumps(headers, indent=2, ensure_ascii=False)}")
    print(f"Body (text): {body_text}")
    # logger.info("Incoming request: method=%s client=%s", method, client)
    # logger.info("Headers: %s", json.dumps(headers, indent=2, ensure_ascii=False))
    # logger.info("Body (text): %s", body_text)

    # return the parsed data so you can see it in caller (and Supabase gets 200)
    return {
        "received": True,
        "method": method,
        "client": client,
        "headers": headers,
        "body": parsed if parsed is not None else body_text
    }


@app.post("/newPosition")
def receive_event():
    return {"msg": "Position recieved!"}

if __name__ == "__main__":
    # public_url = ngrok.connect(8000)  # forwards port 8000
    # print("Public URL:", public_url)
    import os
    uvicorn.run(f"{os.path.basename(__file__).split('.')[0]}:app", host="0.0.0.0", port=8000, reload=True)