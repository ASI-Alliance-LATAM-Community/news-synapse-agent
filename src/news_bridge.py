import mediacloud.api
import os
from datetime import datetime, timedelta

class NewsBridge:
    def __init__(self, api_key: str, collection_ids=None):
        self.api_key = api_key
        self.collection_ids = collection_ids or []
        self.mc_search = mediacloud.api.SearchApi(self.api_key)

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
        all_stories = []
        pagination_token = None
        more_stories = True
        while more_stories and len(all_stories) < max_stories:
            page, pagination_token = self.mc_search.story_list(
                search_query,
                start_date=start_date,
                end_date=end_date,
                collection_ids=self.collection_ids,
                pagination_token=pagination_token
            )
            all_stories += page
            more_stories = pagination_token is not None and len(all_stories) < max_stories
            
        print(f"[NewsBridge] Retrieved {len(all_stories)}")
        return all_stories[:max_stories]

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
        all_stories = []
        pagination_token = None
        more_stories = True
        while more_stories and len(all_stories) < max_stories:
            page, pagination_token = self.mc_search.story_list(
                search_query,
                start_date=start_date,
                end_date=end_date,
                collection_ids=self.collection_ids,
                pagination_token=pagination_token
            )
            all_stories += page
            more_stories = pagination_token is not None and len(all_stories) < max_stories

        print(f"[NewsBridge] Retrieved {len(all_stories)}")
        print(all_stories)
        return all_stories[:max_stories]