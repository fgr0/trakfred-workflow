# Trakfred Workflow
This is an [Alfred v2][] Workflow to search and (soon) control [Trakt.tv][]

## What it does
At the moment, Trakfred allows you to search Trakt and open the result in a Browser. To see, what is planned, look at the Roadmap.

__It is quite slow at the moment, thanks to the not-so-good-Trakt-Servers__

## How to use
For this to work, you need Alfred v2 and the Powerpack.

Download the workflow [here][] and double-click to install. Now you can use the following commands:

- `trakt` searches the entire Trakt Database for Movies, Shows and Episodes
- `movies`, `shows` and `episodes` only search for Movies, Shows or Episodes
- `trakt apikey [key]` adds your API-Key to Trakt

### Adding your API-Key to Trakfred
To be able to access the Trakt API, Trakfred needs your Trakt API-Key. You can find that key on the Trakt homepage under __Profile__ > __Settings__ > __API__ 

Open Alfred, type `trakt apikey 0000000` (replace 00000000 with your own API-Key)  and hit enter.

## Roadmap
* Enable an IMDB-Workflow-Style Submenu
* Use User-Authentication to enable 'Mark as Seen' etc.
* Use Developer-API-Key to enable checkings

## Version
* 0.2.0:    Rewrite of the Codebase and switch to [JinnLynn's alfred-python][JinnLynn]
* 0.1.0:    First release

## Dependencies:
This project relys on [JinnLynn's][JinnLynn] Alfred-Framework, which is licenced under the MIT Licence. His code is included in this repository in the _Alfred_-Folder

[JinnLynn]: https://github.com/JinnLynn/alfred-python
[Alfred v2]: http://www.alfredapp.com/
[Trakt.tv]: http://trakt.tv/
[here]: https://github.com/laerador/trakfred-workflow/raw/master/trakfred.alfredworkflow
