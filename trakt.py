# Trakt API Kit

import alfred
import json
import urllib, urllib2
import urlparse

class Trakt(object):
    api_base_url = "http://api.trakt.tv/"
    def __init__(self,
            api_key):
        self.api_key = api_key

    def search_movies(self, query):
        return self._callAPI(query, api_url='search/movies.json')

    def search_episodes(self, query):
        return self._callAPI(query, api_url='search/episodes.json')

    def search_shows(self, query):
        return self._callAPI(query, api_url='search/shows.json')

    def _callAPI(self,
            query,
            api_url):
        url = urlparse.urljoin(self.api_base_url, api_url + '/' + self.api_key + '/' + urllib.quote_plus(query))
        request = urllib2.Request(url)
        try:
            return json.load(urllib2.urlopen(request))
        except urllib2.HTTPError, err:
            if err.code == 401:
                return json.load(err)

