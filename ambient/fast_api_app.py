"""Ambient FastAPI server that keeps the expense agent available for requests."""

from fastapi import FastAPI, Request, HTTPException
import json
import base64
from monitoring.logger import logger
from agent import agent_system

app = FastAPI(
    title="ExpenseShield-AI API",
    description="Ambient AI agent for expense approval",
    version="1.0.0",
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agent": "ExpenseShield-AI",
        "version": "1.0.0",
    }


@app.post("/trigger/pubsub")
async def handle_pubsub(request: Request):
    try:
        body = await request.body()
        if not body:
            raise HTTPException(status_code=400, detail="Empty request body")

        try:
            data = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            data = {"message": {"data": body.decode("utf-8")}}

        if isinstance(data, dict):
            message = data.get("message", {})
            if isinstance(message, dict):
                encoded_data = message.get("data", "")
                if isinstance(encoded_data, str) and encoded_data:
                    try:
                        decoded_bytes = base64.b64decode(encoded_data)
                        expense = json.loads(decoded_bytes.decode("utf-8"))
                    except Exception:
                        if isinstance(data.get("message", {}).get("data"), dict):
                            expense = data["message"]["data"]
                        else:
                            expense = data
                else:
                    expense = data
            else:
                expense = data
        else:
            expense = data

        logger.info(f"Received expense: {expense}")
        result = await agent_system.process(expense)

        logger.info(f"Processing result: {result}")

        return {"status": "processed", "result": result}

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Run with:
# uvicorn ambient.fast_api_app:app --reload --port 8880
