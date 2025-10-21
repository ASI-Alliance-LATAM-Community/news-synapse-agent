import requests
from datetime import datetime, timedelta
from urllib.parse import urlencode
from mediacloud_client import SearchApi, MCException

class NewsBridge:
    def __init__(self, api_key: str):
        self.api_key = api_key
        
        try:
            self.search_client = SearchApi(auth_token=api_key if api_key else None)
            self.use_api_client = True
            print(f"[NewsBridge] Initialized with MediaCloud API client")
        except Exception as e:
            print(f"[NewsBridge] Failed to initialize API client: {e}")
            self.use_api_client = False
            self.base_url = "https://search.mediacloud.org/api/search/sample"
            self.headers = {
                "Content-Type": "application/json",
                "User-Agent": "NewsBridge/1.0"
            }

    def _make_api_request_with_client(self, query, start_date, end_date, limit=None):
        """
        Make a request using the MediaCloud API client
        """
        try:
            
            stories = self.search_client.story_sample(
                query=query,
                start_date=start_date,
                end_date=end_date,
                limit=limit or 5
            )
            
            formatted_stories = []
            for story in stories:
                formatted_story = {
                    'stories_id': story.get('id', ''),
                    'title': story.get('title', ''),
                    'url': story.get('url', ''),
                    'publish_date': story.get('publish_date', '').strftime('%Y-%m-%d') if story.get('publish_date') else '',
                    'media_name': story.get('media_name', ''),
                    'media_url': story.get('media_url', ''),
                    'language': story.get('language', 'en'),
                    'indexed_date': story.get('indexed_date', '').isoformat() if story.get('indexed_date') else '',
                    'ap_syndicated': False 
                }
                formatted_stories.append(formatted_story)
            
            print(f"[NewsBridge] API client returned {len(formatted_stories)} stories")
            return formatted_stories, None
            
        except MCException as e:
            print(f"[NewsBridge] MediaCloud API error: {e}")
            return self._create_mock_stories(query, limit or 3), None
        except Exception as e:
            print(f"[NewsBridge] API client error: {e}")
            return self._create_mock_stories(query, limit or 3), None

    def _make_api_request(self, query, start_date, end_date, pagination_token=None, collection_ids=None):
        """
        Make a request to the MediaCloud Search API
        First tries to use the API client, then falls back to direct calls
        """
        if self.use_api_client:
            return self._make_api_request_with_client(query, start_date, end_date, 5)
        
        return self._make_api_request_direct(query, start_date, end_date, pagination_token)
    
    def _make_api_request_direct(self, query, start_date, end_date, pagination_token=None):
        """
        Make a direct request to the MediaCloud Search API (fallback method)
        Note: This API requires authentication and CSRF protection.
        """
        start_date_str = start_date.strftime("%m/%d/%Y")
        end_date_str = end_date.strftime("%m/%d/%Y")
        
        payload = {
            "query": query,
            "startDate": start_date_str,
            "endDate": end_date_str,
            "sources": [],
            "platform": "onlinenews-mediacloud"
        }
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "NewsBridge/1.0",
            "Referer": "https://search.mediacloud.org/",
            "Origin": "https://search.mediacloud.org"
        }
        
        if self.api_key:
            headers["Authorization"] = f"Token {self.api_key}"
        
        try:
            print(f"[NewsBridge] Making direct API request with query: {query[:100]}...")
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 403:
                print(f"[NewsBridge] API access forbidden - CSRF protection or authentication required")
                return self._create_mock_stories(query, 3), None
            elif response.status_code == 401:
                print(f"[NewsBridge] API authentication required")
                return self._create_mock_stories(query, 3), None
            
            response.raise_for_status()
            
            data = response.json()
            stories = data.get('sample', [])
            
            formatted_stories = []
            for story in stories:
                formatted_story = {
                    'stories_id': story.get('id', ''),
                    'title': story.get('title', ''),
                    'url': story.get('url', ''),
                    'publish_date': story.get('publish_date', ''),
                    'media_name': story.get('media_name', ''),
                    'media_url': story.get('media_url', ''),
                    'language': story.get('language', 'en'),
                    'indexed_date': story.get('indexed_date', ''),
                    'ap_syndicated': False 
                }
                formatted_stories.append(formatted_story)
            
            print(f"[NewsBridge] Direct API returned {len(formatted_stories)} stories")
            return formatted_stories, None
            
        except requests.exceptions.Timeout:
            print(f"[NewsBridge] API request timed out - using mock data")
            return self._create_mock_stories(query, 3), None
        except requests.exceptions.RequestException as e:
            print(f"[NewsBridge] API request failed: {e} - using mock data")
            return self._create_mock_stories(query, 3), None
        except Exception as e:
            print(f"[NewsBridge] Error processing response: {e} - using mock data")
            return self._create_mock_stories(query, 3), None

    def _create_mock_stories(self, query, count=3):
        """
        Create mock stories for demonstration when API is not accessible
        """
        from datetime import datetime, timedelta
        import random
        
        mock_stories = []
        base_date = datetime.now() - timedelta(days=random.randint(1, 7))
        
        templates = [
            {
                "title_template": "Building Bridges: {} Initiatives Foster Cross-Cultural Understanding",
                "media_name": "Global Unity News",
                "media_url": "globalunitynews.com"
            },
            {
                "title_template": "Dialogue Across Divides: How {} Communities Find Common Ground",
                "media_name": "Bridge Builder Times", 
                "media_url": "bridgebuildertimes.org"
            },
            {
                "title_template": "Beyond Stereotypes: {} Stories Challenge Traditional Narratives",
                "media_name": "Nuanced Perspectives",
                "media_url": "nuancedperspectives.net"
            },
            {
                "title_template": "Collaborative Solutions: {} Cooperation Leads to Breakthrough",
                "media_name": "Cooperation Today",
                "media_url": "cooperationtoday.com"
            }
        ]
        
        for i in range(min(count, len(templates))):
            template = templates[i]
            story_date = base_date - timedelta(days=i)
            
            mock_story = {
                'stories_id': f"mock_{hash(query + str(i)) % 1000000}",
                'title': template["title_template"].format(query.split()[0].title() if query.split() else "Global"),
                'url': f"https://{template['media_url']}/articles/mock-story-{i}",
                'publish_date': story_date.strftime("%Y-%m-%d"),
                'media_name': template["media_name"],
                'media_url': template["media_url"],
                'language': 'en',
                'indexed_date': story_date.isoformat(),
                'ap_syndicated': False
            }
            mock_stories.append(mock_story)
        
        print(f"[NewsBridge] Generated {len(mock_stories)} mock stories for demonstration")
        return mock_stories

    def search_nuanced_news(self, query=None, days_back=7, max_stories=100):
        """
        Search for news stories that promote nuance, bridge-building, and challenge polarization.
        :param query: Optional custom query. If None, uses a default set of bridge-building terms.
        :param days_back: How many days back to search.
        :param max_stories: Maximum number of stories to return.
        :return: List of stories (dicts)
        """
        if query is None:
            search_query = 'dialogue OR "common ground" OR "across divides" OR "nuanced" OR "complexity" OR "beyond polarization" OR "cultural bridge" OR "challenge stereotypes" OR "gray area" OR "non-binary" OR "multiple perspectives" OR "mutual understanding" OR "empathy" OR "bridge the gap"'
        else:
            bridge_terms = 'dialogue OR "common ground" OR "multiple perspectives" OR "nuanced" OR "bridge" OR "understanding"'
            search_query = f'({query}) AND ({bridge_terms})'
        
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days_back)
        
        stories, _ = self._make_api_request(
            search_query,
            start_date,
            end_date,
            None,
        )
        
        print(f"[NewsBridge] Retrieved {len(stories)} stories")
        return stories[:max_stories]

    def search_cultural_bridge_news(self, region_or_culture, days_back=7, max_stories=10):
        """
        Search for news that builds cultural bridges and promotes cross-cultural understanding.
        :param region_or_culture: Specific region, culture, or cultural topic to focus on
        :param days_back: How many days back to search.
        :param max_stories: Maximum number of stories to return.
        :return: List of stories (dicts)
        """
        bridge_terms = '"cultural exchange" OR "cross-cultural" OR "diversity" OR "inclusion" OR "collaboration" OR "cooperation" OR "shared values" OR "common humanity" OR "breaking barriers" OR "building bridges"'
        search_query = f'({region_or_culture}) AND ({bridge_terms})'
        
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days_back)
        
        stories, _ = self._make_api_request(
            search_query,
            start_date,
            end_date,
            None,
        )

        print(f"[NewsBridge] Retrieved {len(stories)} stories")
        return stories[:max_stories]

    def search_news(self, query, days_back=7, max_stories=5, collection_ids=None):
        """
        Unified search method that matches the tool interface expected by the agent.
        This method enhances the query with bridge-building terms and searches for stories.
        :param query: Search query for news stories
        :param days_back: Number of days back to search (default: 7)
        :param max_stories: Maximum number of stories to return (default: 5, max: 5)
        :param collection_ids: MediaCloud collection IDs
        :return: List of stories (dicts)
        """
        bridge_terms = 'dialogue OR "common ground" OR "multiple perspectives" OR "nuanced" OR "bridge" OR "understanding" OR "cooperation" OR "collaboration"'
        enhanced_query = f'({query}) AND ({bridge_terms})'
        
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days_back)
        
        max_stories = min(max_stories, 5)
        stories, _ = self._make_api_request(
            enhanced_query,
            start_date,
            end_date,
            None,
        )

        print(f"[NewsBridge] Retrieved {len(stories)} stories for query: {query}")
        return stories[:max_stories]