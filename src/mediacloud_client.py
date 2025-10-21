"""
MediaCloud API Client - Standalone implementation without python library dependency
Based on the official MediaCloud python library structure
"""

import datetime as dt
import logging
from typing import Any, Dict, List, Optional, Union
import requests

logger = logging.getLogger(__name__)

VERSION = "standalone-1.0"


class MCException(Exception):
    """MediaCloud API Exception"""
    pass


class BaseApi:
    """Base API client for MediaCloud"""
    
    TIMEOUT_SECS = 60
    
    BASE_API_URL = "https://search.mediacloud.org/api/"
    
    USER_AGENT_STRING = f"mediacloud-standalone {VERSION}"
    
    def __init__(self, auth_token: Optional[str] = None):
        if not auth_token:
            logger.warning("No auth token provided - some API endpoints may not work")
        
        self._auth_token = auth_token
        
        self._session = requests.Session()
        
        if self._auth_token:
            self._session.headers.update({'Authorization': f'Token {self._auth_token}'})
        
        self._session.headers.update({'Accept': 'application/json'})
        self._session.headers.update({"User-Agent": self.USER_AGENT_STRING})
        
        self._session.headers.update({
            "Referer": "https://search.mediacloud.org/",
            "Origin": "https://search.mediacloud.org"
        })
    
    def user_profile(self) -> Dict:
        """Return basic info about the current user, including their roles"""
        return self._query('auth/profile')
    
    def version(self) -> Dict:
        """
        Returns dict with (at least):
        GIT_REV, now (float epoch time), version
        """
        return self._query('version')
    
    def _query(self, endpoint: str, params: Optional[Dict] = None, method: str = 'GET') -> Dict:
        """
        Centralize making the actual queries here for easy maintenance and testing of HTTP comms
        """
        endpoint_url = self.BASE_API_URL + endpoint
        
        try:
            if method == 'GET':
                r = self._session.get(endpoint_url, params=params, timeout=self.TIMEOUT_SECS)
            elif method == 'POST':
                r = self._session.post(endpoint_url, json=params, timeout=self.TIMEOUT_SECS)
            else:
                raise RuntimeError(f"Unsupported method of '{method}'")
            
            if r.status_code == 403:
                logger.warning(f"API access forbidden for endpoint: {endpoint}")
                raise MCException(f"Access forbidden - authentication or CSRF protection required")
            elif r.status_code == 401:
                logger.warning(f"API authentication required for endpoint: {endpoint}")
                raise MCException(f"Authentication required")
            elif r.status_code != 200:
                logger.error(f"API Server Error {r.status_code} for endpoint: {endpoint}")
                raise MCException(f"API Server Error {r.status_code}. Params: {params}")
            
            return r.json()
            
        except requests.exceptions.Timeout:
            logger.error(f"API request timeout for endpoint: {endpoint}")
            raise MCException(f"API request timeout")
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for endpoint: {endpoint}: {e}")
            raise MCException(f"API request failed: {e}")


class DirectoryApi(BaseApi):
    """API for accessing MediaCloud directory information"""
    
    PLATFORM_ONLINE_NEWS = "online_news"
    PLATFORM_YOUTUBE = "youtube"
    PLATFORM_TWITTER = "twitter"
    PLATFORM_REDDIT = "reddit"
    
    def collection(self, collection_id: int):
        """Get information about a specific collection"""
        return self._query(f'sources/collections/{collection_id}/', None)
    
    def collection_list(self, platform: Optional[str] = None, name: Optional[str] = None,
                        limit: Optional[int] = 0, offset: Optional[int] = 0, 
                        source_id: Optional[int] = None) -> Dict:
        """List collections with optional filtering"""
        params: Dict[Any, Any] = dict(limit=limit, offset=offset)
        if name:
            params['name'] = name
        if platform:
            params['platform'] = platform
        if source_id:
            params['source_id'] = source_id
        return self._query('sources/collections/', params)
    
    def source(self, source_id: int):
        """Get information about a specific source"""
        return self._query(f'sources/sources/{source_id}/', None)
    
    def source_list(self, platform: Optional[str] = None, name: Optional[str] = None,
                    collection_id: Optional[int] = None,
                    limit: Optional[int] = 0, offset: Optional[int] = 0) -> Dict:
        """List sources with optional filtering"""
        params: Dict[Any, Any] = dict(limit=limit, offset=offset)
        if collection_id:
            params['collection_id'] = collection_id
        if name:
            params['name'] = name
        if platform:
            params['platform'] = platform
        return self._query('sources/sources/', params)


class SearchApi(BaseApi):
    """API for searching MediaCloud content"""
    
    PROVIDER = "onlinenews-mediacloud"
    
    def _prep_default_params(self, query: str, start_date: dt.date, end_date: dt.date,
                             collection_ids: Optional[List[int]] = None, source_ids: Optional[List[int]] = None,
                             platform: Optional[str] = None):
        """Prepare default parameters for search queries"""
        params: Dict[Any, Any] = dict(
            start=start_date.isoformat(), 
            end=end_date.isoformat(), 
            q=query,
            platform=(platform or self.PROVIDER)
        )
        if source_ids and len(source_ids):
            params['ss'] = ",".join([str(sid) for sid in source_ids])
        if collection_ids and len(collection_ids):
            params['cs'] = ",".join([str(cid) for cid in collection_ids])
        return params
    
    def story_count(self, query: str, start_date: dt.date, end_date: dt.date, 
                    collection_ids: Optional[List[int]] = None,
                    source_ids: Optional[List[int]] = None, platform: Optional[str] = None) -> int:
        """Get total count of stories matching the query"""
        params = self._prep_default_params(query, start_date, end_date, collection_ids, source_ids, platform)
        results = self._query('search/total-count', params)
        return results['count']
    
    def story_count_over_time(self, query: str, start_date: dt.date, end_date: dt.date,
                              collection_ids: Optional[List[int]] = None, source_ids: Optional[List[int]] = None,
                              platform: Optional[str] = None) -> List[Dict]:
        """Get story counts over time for the query"""
        params = self._prep_default_params(query, start_date, end_date, collection_ids, source_ids, platform)
        results = self._query('search/count-over-time', params)
        for d in results['count_over_time']['counts']:
            d['date'] = dt.date.fromisoformat(d['date'][:10])
        return results['count_over_time']['counts']
    
    def story_list(self, query: str, start_date: dt.date, end_date: dt.date, 
                   collection_ids: Optional[List[int]] = None,
                   source_ids: Optional[List[int]] = None, platform: Optional[str] = None,
                   expanded: Optional[bool] = None, pagination_token: Optional[str] = None,
                   sort_order: Optional[str] = None,
                   page_size: Optional[int] = None) -> tuple[List[Dict], Optional[str]]:
        """Get list of stories matching the query with pagination support"""
        params = self._prep_default_params(query, start_date, end_date, collection_ids, source_ids, platform)
        if expanded:
            params['expanded'] = 1
        if pagination_token:
            params['pagination_token'] = pagination_token
        if sort_order:
            params['sort_order'] = sort_order
        if page_size:
            params['page_size'] = page_size
        results = self._query('search/story-list', params)
        self._dates_str2objects(results['stories'])
        return results['stories'], results['pagination_token']
    
    def _dates_str2objects(self, stories: List[Dict]):
        """Convert date strings to datetime objects in place"""
        for s in stories:
            s['publish_date'] = dt.date.fromisoformat(s['publish_date'][:10]) if s['publish_date'] else None
            s['indexed_date'] = dt.datetime.fromisoformat(s['indexed_date']) if s['indexed_date'] else None
    
    def story_sample(self, query: str, start_date: dt.date, end_date: dt.date, 
                     collection_ids: Optional[List[int]] = None,
                     source_ids: Optional[List[int]] = None, platform: Optional[str] = None,
                     limit: Optional[int] = None, expanded=False) -> List[Dict]:
        """Get a sample of stories matching the query"""
        params = self._prep_default_params(query, start_date, end_date, collection_ids, source_ids, platform)
        if limit:
            params['limit'] = limit
        
        fields = ['indexed_date', 'publish_date', 'id', 'language', 'media_name', 'media_url', 'title', 'url']
        if expanded:
            fields.append('text')
        params['fields'] = fields
        
        results = self._query('search/sample', params)
        self._dates_str2objects(results['sample'])
        return results['sample']
    
    def story(self, story_id: str) -> Dict:
        """Get a specific story by ID"""
        params = dict(storyId=story_id, platform=self.PROVIDER)
        results = self._query('search/story', params)
        return results['story']
    
    def words(self, query: str, start_date: dt.date, end_date: dt.date, 
              collection_ids: Optional[List[int]] = None,
              source_ids: Optional[List[int]] = None, platform: Optional[str] = None,
              limit: Optional[int] = None) -> List[Dict]:
        """Get top words from stories matching the query"""
        params = self._prep_default_params(query, start_date, end_date, collection_ids, source_ids, platform)
        if limit:
            params['limit'] = limit
        results = self._query('search/words', params)
        return results['words']
    
    def sources(self, query: str, start_date: dt.date, end_date: dt.date, 
                collection_ids: Optional[List[int]] = None,
                source_ids: Optional[List[int]] = None, platform: Optional[str] = None,
                limit: Optional[int] = None) -> List[Dict]:
        """Get top sources from stories matching the query"""
        params = self._prep_default_params(query, start_date, end_date, collection_ids, source_ids, platform)
        if limit:
            params['limit'] = limit
        results = self._query('search/sources', params)
        return results['sources']
    
    def languages(self, query: str, start_date: dt.date, end_date: dt.date, 
                  collection_ids: Optional[List[int]] = None,
                  source_ids: Optional[List[int]] = None, platform: Optional[str] = None,
                  limit: Optional[int] = None) -> List[Dict]:
        """Get language distribution from stories matching the query"""
        params = self._prep_default_params(query, start_date, end_date, collection_ids, source_ids, platform)
        if limit:
            params['limit'] = limit
        results = self._query('search/languages', params)
        return results['languages']


def create_search_api(auth_token: Optional[str] = None) -> SearchApi:
    """Create a SearchApi instance with optional authentication"""
    return SearchApi(auth_token)


def create_directory_api(auth_token: Optional[str] = None) -> DirectoryApi:
    """Create a DirectoryApi instance with optional authentication"""
    return DirectoryApi(auth_token)