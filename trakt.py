# Trakt API Kit

import alfred
import json
import urllib, urllib2
import urlparse
import time

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


def parse_movie(item):
    parsed = {}
    parsed['type'] = 'movie'

    if 'imdb_id' in item:
        parsed['id'] = item['imdb_id']
    else:
        return None

    if 'url' in item:
        parsed['url'] = item['url']
    else:
        parsed['url'] = parsed['id']

    if 'title' in item:
        parsed['title'] = item['title']
    else:
        parsed['title'] = ''

    if 'tagline' in item:
        parsed['subtitle'] = item['tagline']
    elif 'overview' in item:
        parsed['subtitle'] = item['overview']
    else:
        parsed['subtitle'] = ''

    if 'year' in item:
        parsed['title'] += ' [' + str(item['year']) + ']'

    item['alfred'] = parsed
    return item

def parse_show(item):
    parsed = {}
    parsed['type'] = 'show'

    if 'imdb_id' in item:
        parsed['id'] = item['imdb_id']
    else:
        return None

    if 'url' in item:
        parsed['url'] = item['url']
    else:
        parsed['url'] = parsed['id']

    if 'title' in item:
        parsed['title'] = item['title']
    else:
        parsed['title'] = ''

    if 'tagline' in item:
        parsed['subtitle'] = item['tagline']
    elif 'overview' in item:
        parsed['subtitle'] = item['overview']
    else:
        parsed['subtitle'] = ''

    item['alfred'] = parsed
    return item

def parse_episode(episode):
    parsed = {}

    if 'show' in episode:
        episode['show'] = parse_show(episode['show'])
        parsed = episode['show']['alfred']

    if 'episode' in episode:
        if 'season' in episode['episode'] and 'episode' in episode['episode']:
            episode_nr = 'S' + str(episode['episode']['season']) + 'E' + str(episode['episode']['episode'])
        else:
            episode_nr = 'S?E?'

        parsed['id'] += episode_nr

        if 'title' in episode['episode']:
            parsed['subtitle'] = parsed['title']
            parsed['title'] = episode_nr + ' ' + episode['episode']['title']

        if 'url' in episode['episode']:
            parsed['url'] = episode['episode']['url']

        if 'first_aired' in episode['episode']:
            parsed['subtitle'] += ', aired: ' + time.strftime('%d %b %Y', time.localtime(episode['episode']['first_aired'])) 

        parsed['type'] = 'episode'
        episode['alfred'] = parsed
        return episode
    else:
        return None
