# vigilant-octo-potato
Indexing the world

## Overview
Computational geometry is fun, so in order to play with it, I have this project. I've previously don't done some plane-geometry work, like line-sweeps, convex-hulls, and kd-trees so the focus here will be on diving more into spherical data, ie, geospacial.

Initial objectives:
 1. find fun geospacial data
    1. http://download.geonames.org/export/dump/ has a lot of data, we'll focus on http://download.geonames.org/export/dump/cities1000.zip for now
 1. Implement some interesting search/indexing behaviors
    1. K-nearest neighbors is a classic
    1. Finding a city by name
    1. layer in some data filtering...
       1. country limits
       1. continent limits
       1. data augmentations... population, literacy rate, GDP, State sponsors of terrorism
    1. bounding regions?
       1. Box?
       1. Convex-hulls on a sphere?
 1. expose capability as a service, probably via flask
 
## Conciderations
### Learning opportunities
Given that the motivation for this task is not PURELY self-driven, how much should I make use of the eco system?

Perhaps, I should start with using lots of existing tools then code my own against interfaces for learning.
#### Distribution
I usually use CPython, but using the Andaoconda distribution would give me some additional tools, like a built-ing kdtree...

##### Virtual envs
I setup my virtual env this way:
```shell
$ conda create --name octo
$ conda install -n octo pip
$ conda install --file requirements.txt
```


### Data
The data seems fairly clean, though there are a variety of characters in non-latin alphabets, so UTF support will be more important than normal.
 
Provided data is in tab-separated text files dumped from some store.
 
Sources of data augmentations have not been identified, and are currently low priority
 
### Storage
What, if any, cold-start penalties are permitted?
 
Should I just find a geo-enabled data-store and load? PostGIS?
 
### Service
After some libraries pass unit tests, some API (probably RESTful) needs to be imagined and developed.

not using a virtual environment, the anaconda python runs this fine...

```shell
$ python load_db.py
$ FLASK_APP=service.py python -m flask run
```

endpoints:
 * ```/cities``` ...
 * ```/cities/<geonameid>```
 * ```/cities/<geonameid>/nearest/<k nearest neighbors>```
 * ```/cities?name=<name to search for>```
 * ```/cities?partial_name=<name fragment to search for>```
