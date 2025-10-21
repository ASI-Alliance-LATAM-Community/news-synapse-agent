from typing import List, Dict, Any

TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "search_news",
            "description": "Search for news stories that promote nuanced thinking, bridge-building discourse, and challenge polarization. Designed to find content that transcends ideological divides, fosters complex non-binary thought, builds cultural bridges, and challenges stereotypes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for news stories. Can be topics, locations, themes, regions, cultures, medicine, etc. The tool will automatically enhance this with bridge-building and nuance-promoting terms."
                    },
                    "days_back": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 30,
                        "description": "Number of days back to search (default: 7)"
                    },
                    "max_stories": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 5,
                        "description": "Maximum number of stories to return (default: 5, max: 5)"
                    },
                    "collection_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "MediaCloud collection IDs to search within. If not provided, uses default US National Collection."
                    }
                },
                "required": ["query"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]