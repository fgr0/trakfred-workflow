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

def get_image_url_by_size(images, size='small'):
    sizes = {
        'poster': {
            'small': '-138',
            'medium': '-300',
            'uncompressed': ''},
        'fanart': {
            'small': '-218',
            'medium': '-940',
            'uncompressed': ''},
        'episodes': {
            'small': '-218',
            'medium': '-218',
            'uncompressed': ''},
        'banners': {
            'small': '',
            'medium': '',
            'uncompressed': ''}}

    if 'poster' in images:
        url = images['poster']
        pos = url.rfind('.')
        url2 = url[:pos] + sizes['poster'][size] + url[pos:]
    elif 'fanart' in images:
        url = images['fanart']
        pos = url.rfind('.')
        url2 = url[:pos] + sizes['fanart'][size] + url[pos:]
    elif 'banner' in images:
        url = images['banner']
        pos = url.rfind('.')
        url2 = url[:pos] + sizes['banner'][size] + url[pos:]
    elif 'episode' in images:
        url = images['episode']
        pos = url.rfind('.')
        url2 = url[:pos] + sizes['episode'][size] + url[pos:]
    else:
        return ''

    if url2 == 'http://slurm.trakt.us/images/poster-small-138.jpg':
        return ''
    else:
        return url2


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

    if 'year' in item:
        parsed['year'] = str(item['year'])
        parsed['title'] += ' (' + str(item['year']) + ')'

    if 'ratings' in item:
        parsed['rating'] = str(item['ratings']['percentage']) + '%'
    else:
        parsed['rating'] = ''

    if 'genres' in item:
        parsed['genres'] = ' '.join(item['genres'])

    if 'images' in item:
        parsed['images'] = item['images']
    
    parsed['subtitle'] = ', '.join(filter(bool, ['[Movie]', parsed['rating'], parsed['genres']]))

    item['alfred'] = parsed
    return item

def parse_show(item):
    parsed = {}
    parsed['type'] = 'show'

    if 'imdb_id' in item and item['imdb_id']:
        parsed['id'] = item['imdb_id']
    elif 'tvdb_id' in item:
        parsed['id'] = 'tvdb' + str(item['tvdb_id'])
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

    if 'year' in item:
        parsed['year'] = str(item['year'])

    if 'ratings' in item:
        parsed['rating'] = str(item['ratings']['percentage']) + '%'
    else:
        parsed['rating'] = ''

    if 'genres' in item:
        parsed['genres'] = ' '.join(item['genres'])

    if 'images' in item:
        parsed['images'] = item['images']

    parsed['subtitle'] = ', '.join(filter(bool, ['[Show]', parsed['rating'], parsed['year'], parsed['genres']]))

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

        if 'ratings' in episode['episode']:
            parsed['rating'] = str(episode['episode']['ratings']['percentage']) + '%'
        else:
            parsed['rating']

        if 'first_aired' in episode['episode']:
            parsed['subtitle'] = ', '.join(filter(bool, [
                    '[Episode]',
                    parsed['rating'],
                    parsed['subtitle'],
                    'aired: ' + time.strftime('%d %b %Y', time.localtime(episode['episode']['first_aired'])),
                    parsed['genres']
                ]))

        parsed['type'] = 'episode'
        episode['alfred'] = parsed
        return episode
    else:
        return None
