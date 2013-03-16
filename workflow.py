# Trakt API Kit

# -----------------------------------------------------------------------------
# "THE NERD-WARE LICENSE" (Revision 1): <dev.git@lc3dyr.de> wrote this file.
# As long as you retain this notice you can do whatever you want with this
# stuff. If we meet some day, and you think this stuff is worth it, you can buy
# me a beer, mate or some food in return [Franz Greiling]
# -----------------------------------------------------------------------------

# by laerador (Franz Greiling)

import alfred
import trakt
import plistlib
import os, sys

def save_key(key):
    """
    Saves the API Key in a plist
    """
    t = trakt.Trakt(key)
    save = t.search_movies('Bier')
    if 'status' in save and save['status'] == "failure":
        return save['error']
    else:
        write_config({'apikey': key})
        return "Succesfully saved Key."

def write_config(dic={}):
    file = open(alfred.work(False) + '/config.plist', 'w')
    plistlib.writePlist(dic, file)

def read_key():
    """
    Reads the API Key from plist
    """
    if os.path.isfile(alfred.work(False) + '/config.plist'):
        file = open(alfred.work(False) + '/config.plist', 'r')
        pl = plistlib.readPlist(file)
        if 'apikey' in pl:
            return pl['apikey']
    print(alfred.xml([alfred.Item(
        attributes={
            'uid': 'error',
            'arg': 'error',
            'valid': 'no'},
        title="No Trakt API-Key Provided",
        subtitle="Please add a Trakt API-Key with `trakt apikey key`",
        icon='icon.png')]))
    sys.exit()

def parse_movie(movie):
    if 'imdb_id' in movie:
        movie_id = movie['imdb_id']
    else:
        movie_id = 'error'

    if 'url' in movie:
        movie_arg = movie['url']
    else:
        movie_arg = movie_id

    if 'title' in movie:
        movie_title = movie['title']
    else:
        movie_title = 'title'

    if 'tagline' in movie:
        movie_subtitle = movie['tagline']
    elif 'overview' in movie:
        movie_subtitle = movie['overview']
    else:
        movie_subtitle = 'subtitle'

    return alfred.Item(
        attributes={
            'uid': movie_id,
            'arg': movie_arg,
            'autocomplete': movie_id},
        title=movie_title,
        subtitle=movie_subtitle,
        icon='icon.png')

def parse_show(show):
    return parse_movie(show)

def parse_episode(episode):
    if 'show' in episode:
        if 'title' in episode['show']:
            show_name = episode['show']['title']
        else:
            show_name = 'title'

        if 'imdb_id' in episode['show']:
            uid = episode['show']['imdb_id']
        else:
            uid = 'error'

        if 'url' in episode['show']:
            arg = episode['show']['url']
    else:
        show_name = 'title'
        uid = 'error'

    if 'episode' in episode:
        if 'season' in episode['episode'] and 'episode' in episode['episode']:
            episode_nr = 'S' + str(episode['episode']['season']) + 'E' + str(episode['episode']['episode'])
        else:
            episode_nr = 'S?E?'

        uid += episode_nr

        if 'title' in episode['episode']:
            episode_name = episode['episode']['title']

        if 'url' in episode['episode']:
            arg = episode['episode']['url']
    else:
        episode_nr = 'S?E?'
        episode_name = 'name'
        if not arg:
            arg = uid

    return alfred.Item(
            attributes={
                'uid': uid,
                'arg': arg,
                'autocomplete': uid},
            title=show_name + ' ' + episode_nr,
            subtitle=episode_name,
            icon='icon.png')

def search(query, scope):
    tr = trakt.Trakt(api_key=read_key())

    items = []

    if 'movies' in scope:
        results = tr.search_movies(query)
        for result in results:
            items.append(parse_movie(result))

    if 'shows' in scope:
        results = tr.search_shows(query)
        for result in results:
            items.append(parse_show(result))

    if 'episodes' in scope:
        results = tr.search_episodes(query)
        for result in results:
            items.append(parse_episode(result))

    if not items:
        items.append(alfred.Item(
            attributes={
                'uid': 'trakt_no_results',
                'arg': '',
                'valid': 'no'},
            title="Nothing found",
            subtitle="D'oh! We didn't find any matches for your search!",
            icon='icon.png'))

    return alfred.xml(items)


def query(query, scope=['movies','shows','episodes']):
    """
    Analyses query Data and Forwards it to appropriate handler
    """
    if query[:2] == 'tt':
        return 'tt'
    else:
        return search(query, scope)
