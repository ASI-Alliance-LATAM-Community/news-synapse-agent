import json
import venv
import requests
from uuid import uuid4
from datetime import datetime, timezone

from uagents_core.contrib.protocols.chat import (
    chat_protocol_spec,
    ChatMessage,
    ChatAcknowledgement,
    TextContent,
    StartSessionContent,
)
from uagents import Agent, Context, Protocol

import os
from dotenv import load_dotenv
from philosophical_framework import PhilosophicalFramework
from cultural_bridge import CulturalBridgeBuilder, DialogueFacilitator

load_dotenv()

ASI1_API_KEY = os.getenv("ASI1_API_KEY")
ASI1_BASE_URL = "https://api.asi1.ai/v1"
ASI1_HEADERS = {
    "Authorization": f"Bearer {ASI1_API_KEY}" if ASI1_API_KEY else "",
    "Content-Type": "application/json",
}

philosophical_framework = PhilosophicalFramework()
cultural_bridge = CulturalBridgeBuilder()
dialogue_facilitator = DialogueFacilitator()

def _text_msg(text: str) -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=text)],
    )

async def process_query(query: str, ctx: Context):
    try:
        philosophical_analysis = cultural_bridge.generate_philosophical_inquiry(query)
        
        user_message = {"role": "user", "content": f"{query}\n\n--- PHILOSOPHICAL ANALYSIS ---\n{philosophical_analysis}"}
        
        system_content = philosophical_framework.get_critical_thinking_prompt()
        
        system_message = {
            "role": "system",
            "content": system_content,
        }

        payload = {
            "model": "asi1-mini",
            "messages": [system_message, user_message],
            "temperature": 0.7,
            "max_tokens": 4096,
        }

        resp = requests.post(
            f"{ASI1_BASE_URL}/chat/completions",
            headers=ASI1_HEADERS,
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        response_json = resp.json()
        model_msg = response_json["choices"][0]["message"]

        return model_msg["content"]

    except Exception as e:
        ctx.logger.error(f"Error processing query: {e}")
        return f"An error occurred: {e}"


agent = Agent(name="agi-hackathon-agent", port=8001, mailbox=True)
chat_proto = Protocol(spec=chat_protocol_spec)


@agent.on_event("startup")
async def _startup(ctx: Context):
    ctx.logger.info(
        f"🚀 Starting"
    )

@chat_proto.on_message(model=ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    try:
        ack = ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc), acknowledged_msg_id=msg.msg_id
        )
        await ctx.send(sender, ack)

        for item in msg.content:
            if isinstance(item, StartSessionContent):
                ctx.logger.info(f"Got a start session message from {sender}")
                continue
            elif isinstance(item, TextContent):
                ctx.logger.info(f"Got a message from {sender}: {item.text}")
                result = await process_query(item.text, ctx)

                response_text = (
                    result if isinstance(result, str) else json.dumps(result)
                )
                await ctx.send(sender, _text_msg(response_text))
            else:
                ctx.logger.info(f"Got unexpected content from {sender}")
    except Exception as e:
        ctx.logger.error(f"Error handling chat message: {str(e)}")
        await ctx.send(sender, _text_msg(f"An error occurred: {str(e)}"))


@chat_proto.on_message(model=ChatAcknowledgement)
async def handle_chat_acknowledgement(
    ctx: Context, sender: str, msg: ChatAcknowledgement
):
    ctx.logger.info(
        f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}"
    )
    if msg.metadata:
        ctx.logger.info(f"Metadata: {msg.metadata}")


agent.include(chat_proto)

if __name__ == "__main__":
    agent.run()(venv)  # type: ignore