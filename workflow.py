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
import os, sys

def save_key(key):
    t = trakt.Trakt(key)
    save = t.search_movies('Bier')
    if 'status' in save and save['status'] == "failure":
        return save['error']
    else:
        alfred.config.set(apikey=key)
        return "Succesfully saved Key."

def read_key():
    key = alfred.config.get('apikey')
    
    if key:
        return key
    else:
        alfred.exitWithFeedback(title="No Trakt API-Key provided",
                subtitle="Please add a Trakt API-Key with `trakt apikey [key]`")

def search(query, scope):
    tr = trakt.Trakt(api_key=read_key())

    items = []

    if 'movies' in scope:
        results = tr.search_movies(query)
        for result in results:
            items.append(trakt.parse_movie(result))

    if 'shows' in scope:
        results = tr.search_shows(query)
        for result in results:
            items.append(trakt.parse_show(result))

    if 'episodes' in scope:
        results = tr.search_episodes(query)
        for result in results:
            items.append(trakt.parse_episode(result))

    items = filter(None, items)

    if not items:
        alfred.exitWithFeedback(title="Nothing found", subtitle="D'oh! We didn't find any matches for your search!")

    fb = alfred.Feedback()
    for item in items:
        fb.addItem(title=item['alfred']['title'],
                subtitle=item['alfred']['subtitle'],
                autocomplete=item['alfred']['id'],
                arg=item['alfred']['url'])
    fb.output()

def query(query, scope=['movies','shows','episodes']):
    """
    Analyses query Data and Forwards it to appropriate handler
    """
    return search(query, scope)
