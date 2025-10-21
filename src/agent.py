import json
import requests
import asyncio
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

MEDIACLOUD_API_KEY = os.getenv("MEDIACLOUD_API_KEY", "")
news_bridge = NewsBridge(api_key=MEDIACLOUD_API_KEY)

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
        ctx.logger.debug(f"[CALL] Function={func_name!r}, Raw args={args!r}")
        
        if func_name == "search_news":
            query = args.get("query")
            days_back = args.get("days_back", 7)
            max_stories = min(args.get("max_stories", 5), 5)
            
            max_retries = 3
            retry_delay = 2
            
            for attempt in range(max_retries):
                try:
                    result = news_bridge.search_nuanced_news(query, days_back, max_stories)
                        
                    result = result[:5]
                    
                    result = serialize_datetime_objects(result)
                    
                    json.dumps(result)
                    
                    ctx.logger.info(f"[RESULT] {func_name} returned {len(result)} stories")
                    return result
                    
                except Exception as e:
                    error_msg = str(e).lower()
                    if ("429" in error_msg or "rate limit" in error_msg) and attempt < max_retries - 1:
                        ctx.logger.warning(f"Rate limit hit, retrying in {retry_delay}s (attempt {attempt + 1}/{max_retries})")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2 
                        continue
                    else:
                        raise e
        else:
            raise ValueError(f"Unsupported function call: {func_name}")

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
            "max_tokens": 8192,
        }
        
        ctx.logger.info(f"[DEBUG] Making API request with {len(tools)} tools")

        max_api_retries = 2
        api_retry_delay = 1
        resp = None
        
        for api_attempt in range(max_api_retries):
            try:
                resp = requests.post(
                    f"{ASI1_BASE_URL}/chat/completions",
                    headers=ASI1_HEADERS,
                    json=payload,
                    timeout=30
                )
                
                if resp.status_code == 500:
                    ctx.logger.warning(f"ASI1 API returned 500 error (attempt {api_attempt + 1}/{max_api_retries})")
                    if api_attempt < max_api_retries - 1:
                        await asyncio.sleep(api_retry_delay)
                        api_retry_delay *= 2
                        continue
                    else:
                        break
                elif resp.status_code == 200:
                    break
                else:
                    break
                    
            except requests.exceptions.Timeout:
                ctx.logger.warning(f"ASI1 API request timed out (attempt {api_attempt + 1}/{max_api_retries})")
                if api_attempt < max_api_retries - 1:
                    await asyncio.sleep(api_retry_delay)
                    continue
                else:
                    ctx.logger.error("[ERROR] ASI1 API request timed out after retries")
                    return "I'm experiencing technical difficulties with the AI service (Request Timeout). Please try again in a moment."
            except requests.exceptions.RequestException as e:
                ctx.logger.error(f"[ERROR] ASI1 API request failed: {e}")
                return f"I'm experiencing technical difficulties with the AI service ({str(e)}). Please try again in a moment."
        
        if resp is None:
            return "I'm experiencing technical difficulties with the AI service. Please try again in a moment."
        
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
                    "max_tokens": 8192,
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
        
        if not tool_calls:
            natural_payload = {
                "model": "asi1-mini",
                "messages": [system_message, initial_message],
                "temperature": 0.7,
                "max_tokens": 8192,
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
                    ctx.logger.info(f"[RESULT] {func_name} result: {len(result) if isinstance(result, (list, dict)) else 'unknown'} stories found")
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
            "max_tokens": 8192,
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
    ctx.logger.info("✅ NewsBridge initialized successfully with MediaCloud Search API")


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