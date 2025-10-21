import json
import requests
from uuid import uuid4
from datetime import datetime, timezone, date

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
from news_bridge import NewsBridge
from tools import TOOLS as tools

def serialize_datetime_objects(obj):
    """Convert datetime and date objects to strings for JSON serialization"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, date):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: serialize_datetime_objects(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [serialize_datetime_objects(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return serialize_datetime_objects(obj.__dict__)
    else:
        return obj

load_dotenv()

ASI1_API_KEY = os.getenv("ASI1_API_KEY")

if not ASI1_API_KEY:
    raise RuntimeError("ASI1_API_KEY not set. Add it to your environment or .env")

ASI1_BASE_URL = "https://api.asi1.ai/v1"
ASI1_HEADERS = {
    "Authorization": f"Bearer {ASI1_API_KEY}",
    "Content-Type": "application/json",
}

MEDIACLOUD_API_KEY = os.getenv("MEDIACLOUD_API_KEY")
MEDIACLOUD_COLLECTION_IDS = [34412234]
news_bridge = NewsBridge(api_key=MEDIACLOUD_API_KEY, collection_ids=MEDIACLOUD_COLLECTION_IDS) if MEDIACLOUD_API_KEY else None

philosophical_framework = PhilosophicalFramework()
cultural_bridge = CulturalBridgeBuilder()
dialogue_facilitator = DialogueFacilitator()

NEWS_TOOL_NAMES = {
    "search_news"
}

def format_error_response(error: Exception) -> str:
    """Format error messages for user display"""
    error_str = str(error)
    return (
        "⚠️ An error occurred while processing your request:\n\n"
        f"{error_str}\n\n"
        "You can try:\n"
        "1. Waiting a few moments and trying again\n"
        "2. Checking your internet connection\n"
        "3. Verifying the request parameters"
    )

async def call_news_tool(func_name: str, args: dict, ctx: Context):
    """Call news search tools using NewsBridge"""
    try:
        if not news_bridge:
            raise ValueError("MediaCloud API key not configured. Please set MEDIACLOUD_API_KEY in your environment.")
        
        ctx.logger.debug(f"[CALL] Function={func_name!r}, Raw args={args!r}")
        
        if func_name == "search_news":
            query = args.get("query")
            days_back = args.get("days_back", 7)
            max_stories = min(args.get("max_stories", 5), 5)
            collection_ids = args.get("collection_ids")
            
            if collection_ids:
                original_ids = news_bridge.collection_ids
                news_bridge.collection_ids = collection_ids
                try:
                    result = news_bridge.search_nuanced_news(query, days_back, max_stories)
                finally:
                    news_bridge.collection_ids = original_ids
            else:
                result = news_bridge.search_nuanced_news(query, days_back, max_stories)
                
            result = result[:5]
            
            result = serialize_datetime_objects(result)
        else:
            raise ValueError(f"Unsupported function call: {func_name}")
            
        ctx.logger.info(f"[RESULT] {func_name} returned {len(result)} stories")
        return result

    except Exception as e:
        ctx.logger.error(f"News tool call failed for {func_name}: {e}")
        raise ValueError(f"Failed to fetch news data: {e}")

def _text_msg(text: str) -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=text)],
    )

async def process_query(query: str, ctx: Context) -> str:
    try:
        philosophical_analysis = cultural_bridge.generate_philosophical_inquiry(query)
        enhanced_query = f"{query}\n\n--- PHILOSOPHICAL ANALYSIS ---\n{philosophical_analysis}"
        
        initial_message = {"role": "user", "content": enhanced_query}
        
        system_content = philosophical_framework.get_critical_thinking_prompt()
        system_message = {"role": "system", "content": system_content}
        
        payload = {
            "model": "asi1-mini",
            "messages": [system_message, initial_message],
            "tools": tools,
            "tool_choice": "auto",
            "temperature": 0.7,
            "max_tokens": 4096,
        }
        
        ctx.logger.info(f"[DEBUG] Making API request with {len(tools)} tools")

        resp = requests.post(
            f"{ASI1_BASE_URL}/chat/completions",
            headers=ASI1_HEADERS,
            json=payload,
        )
        
        if resp.status_code != 200:
            ctx.logger.error(f"[ERROR] ASI1 API error: {resp.status_code} - {resp.text}")
            if resp.status_code == 500:
                ctx.logger.info("[FALLBACK] Trying request without tools due to server error")
                
                if any(keyword in query.lower() for keyword in ["search", "find", "news", "stories", "article", "media", "latest", "recent"]):
                    ctx.logger.info("[FALLBACK] Detected news request, calling tool directly")
                    try:
                        search_query = query.lower().replace("search news about", "").replace("find stories about", "").replace("search", "").replace("news", "").strip()
                        if not search_query:
                            search_query = query
                        
                        manual_result = await call_news_tool("search_news", {"query": search_query}, ctx)
                        
                        if manual_result:
                            formatted_response = "I found these relevant news stories for you:\n\n"
                            for i, story in enumerate(manual_result, 1):
                                if isinstance(story, dict):
                                    title = story.get('title', 'No Title')
                                    url = story.get('url', 'No URL')
                                    publish_date = story.get('publish_date', 'Unknown date')
                                    media_name = story.get('media_name', 'Unknown source')
                                    
                                    formatted_response += f"**{i}. {title}**\n"
                                    formatted_response += f"- **Source:** {media_name}\n"
                                    formatted_response += f"- **Date:** {publish_date}\n"
                                    formatted_response += f"- **Link:** {url}\n\n"
                            
                            return formatted_response
                        else:
                            return "I searched for news but couldn't find relevant stories at this time. Please try again with different keywords."
                    except Exception as e:
                        ctx.logger.error(f"[FALLBACK] Direct news search failed: {e}")
                
                fallback_payload = {
                    "model": "asi1-mini",
                    "messages": [system_message, initial_message],
                    "temperature": 0.7,
                    "max_tokens": 4096,
                }
                fallback_resp = requests.post(
                    f"{ASI1_BASE_URL}/chat/completions",
                    headers=ASI1_HEADERS,
                    json=fallback_payload,
                )
                if fallback_resp.status_code == 200:
                    fallback_json = fallback_resp.json()
                    return fallback_json["choices"][0]["message"]["content"]
                else:
                    ctx.logger.error(f"[ERROR] Fallback request also failed: {fallback_resp.status_code} - {fallback_resp.text}")
            
            return f"I'm experiencing technical difficulties with the AI service (Error {resp.status_code}). Please try again in a moment."
        
        resp.raise_for_status()
        response_json = resp.json()
        
        ctx.logger.info(f"[DEBUG] API response received successfully")

        model_msg = response_json["choices"][0]["message"]
        tool_calls = model_msg.get("tool_calls", [])
        messages_history = [system_message, initial_message, model_msg]
        
        ctx.logger.info(f"[DEBUG] Tool calls found: {len(tool_calls)}")
        if tool_calls:
            for i, tool_call in enumerate(tool_calls):
                ctx.logger.info(f"[DEBUG] Tool call {i+1}: {tool_call['function']['name']}")
        
        content = model_msg.get("content", "")
        if any(marker in content for marker in ["tool▁calls▁begin", "tool_calls_begin", "｜tool▁call▁begin｜", "tool_call_begin", "<｜tool", "tool▁sep｜"]):
            ctx.logger.error(f"[ERROR] Model returned raw tool syntax: {content}")
            if any(keyword in query.lower() for keyword in ["search", "find", "news", "stories", "article", "media", "latest", "recent", "china", "usa", "latam"]):
                ctx.logger.info("[FALLBACK] Manually triggering news search due to raw tool syntax")
                try:
                    search_query = query.lower().replace("please search news about", "").replace("search news about", "").replace("find stories about", "").replace("search", "").replace("news", "").replace("about", "").strip()
                    if not search_query:
                        search_query = query
                    
                    ctx.logger.info(f"[FALLBACK] Using search query: '{search_query}'")
                    manual_result = await call_news_tool("search_news", {"query": search_query}, ctx)
                    
                    if manual_result:
                        formatted_response = "I found these relevant news stories for you:\n\n"
                        for i, story in enumerate(manual_result, 1):
                            if isinstance(story, dict):
                                title = story.get('title', 'No Title')
                                url = story.get('url', 'No URL')
                                publish_date = story.get('publish_date', 'Unknown date')
                                media_name = story.get('media_name', 'Unknown source')
                                
                                formatted_response += f"**{i}. {title}**\n"
                                formatted_response += f"- **Source:** {media_name}\n"
                                formatted_response += f"- **Date:** {publish_date}\n"
                                formatted_response += f"- **Link:** {url}\n\n"
                        
                        return formatted_response
                    else:
                        return "I searched for news but couldn't find relevant stories at this time. Please try again with different keywords."
                except Exception as e:
                    ctx.logger.error(f"[FALLBACK] Manual tool call failed: {e}")
            
            return "I apologize, but there was an issue with processing your request. Please try rephrasing your question or try again."

        if not tool_calls:
            natural_payload = {
                "model": "asi1-mini",
                "messages": [system_message, initial_message],
                "temperature": 0.7,
                "max_tokens": 4096,
            }
            
            natural_response = requests.post(
                f"{ASI1_BASE_URL}/chat/completions",
                headers=ASI1_HEADERS,
                json=natural_payload,
            )
            natural_response.raise_for_status()
            natural_response_json = natural_response.json()
            return natural_response_json["choices"][0]["message"]["content"]

        for tool_call in tool_calls:
            func_name = tool_call["function"]["name"]
            arguments = json.loads(tool_call["function"]["arguments"] or "{}")
            tool_call_id = tool_call["id"]

            try:
                if func_name in NEWS_TOOL_NAMES:
                    ctx.logger.info(f"[CALL] Calling news tool: {func_name} with args: {arguments}")
                    result = await call_news_tool(func_name, arguments, ctx)
                    ctx.logger.info(f"[RESULT] {func_name} result: {len(result)} stories found")
                else:
                    raise ValueError(f"Unsupported tool: {func_name}")

                content_to_send = json.dumps(result)

            except Exception as e:
                ctx.logger.error(f"Tool execution failed for {func_name}: {e}")
                content_to_send = json.dumps(
                    {"error": format_error_response(e), "status": "failed", "tool": func_name}
                )

            messages_history.append(
                {"role": "tool", "tool_call_id": tool_call_id, "content": content_to_send}
            )

        final_payload = {
            "model": "asi1-mini",
            "messages": messages_history,
            "temperature": 0.7,
            "max_tokens": 4096,
        }
        final_response = requests.post(
            f"{ASI1_BASE_URL}/chat/completions",
            headers=ASI1_HEADERS,
            json=final_payload,
        )
        final_response.raise_for_status()
        return final_response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        ctx.logger.error(f"Error processing query: {e}")
        return f"An error occurred: {e}"


agent = Agent(name="agi-hackathon-agent", port=8001, mailbox=True)
chat_proto = Protocol(spec=chat_protocol_spec)


@agent.on_event("startup")
async def _startup(ctx: Context):
    ctx.logger.info("🚀 Starting AGI Hackathon Agent - Cultural Bridge Builder")
    if news_bridge:
        ctx.logger.info("✅ NewsBridge initialized successfully")
    else:
        ctx.logger.warning("❌ NewsBridge not initialized - MEDIACLOUD_API_KEY missing")


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
                response_text = await process_query(item.text, ctx)
                ctx.logger.info(f"Response text: {response_text}")
                response = ChatMessage(
                    timestamp=datetime.now(timezone.utc),
                    msg_id=uuid4(),
                    content=[TextContent(type="text", text=response_text)],
                )
                await ctx.send(sender, response)
            else:
                ctx.logger.info(f"Got unexpected content from {sender}")
    except Exception as e:
        ctx.logger.error(f"Error handling chat message: {str(e)}")
        error_response = ChatMessage(
            timestamp=datetime.now(timezone.utc),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=f"An error occurred: {str(e)}")],
        )
        await ctx.send(sender, error_response)


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
    agent.run()