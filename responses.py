

_html = """<HTML><HEAD><?HEAD><BODY>{}</BODY><?HTML>"""

def index_page():
    content = """This is a simple api for exploring the <a href="http://www.geonames.org">geonames</a> <a href="http://download.geonames.org/export/dump">data</a>, specificially the cities1000 data, which is cities with population of greater than or equal to 1000 people.

<p>
The api is rooted at /cities endpoints include:
<ul>
    <li>/cities/&ltgeonameid&gt</li>
    <li>/cities/&ltgeonameid&gt/nearest/&ltk&gt</li>
    <li>/cities?name=&ltname to search for&gt</li>
    <li>/cities?partial_name=&ltname fragment to search for&gt</li>
</ul>
</p>
<p>Here are some examples to get you started:
<ul>
    <li><a href="/cities/5391959">/cities/5391959</a> will take you to the local entry to San Francisco, CA, USA</li>
    <li><a href="/cities/5391959/nearest/3">/cities/5391959/nearest/3</a> will return a list of the three cities closest to San Francisco. Note, this will include San Francisco as the closest location to itself.</li>
    <li><a href="/cities?name=Oakland">/citie?name=Oakland</a> will produce a list of cities named Oakland</li>
</ul>
</p>

"""
    return _html.format(content)


def _city_desc(city, link_to_city_page=True):
    link_content = """
<ul>
    <li><em>Name</em>: {name}</li>
    <li><em>geonameid</em>: <a href="/cities/{geonameid}">{geonameid}</a></li>
    <li><em>Latitude</em>: {latitude}</li>
    <li><em>Longitude</em>: {longitude}</li>
</ul>"""
    nolink_content = """
<ul>
    <li><em>Name</em>: {name}</li>
    <li><em>geonameid</em>: {geonameid}</li>
    <li><em>Latitude</em>: {latitude}</li>
    <li><em>Longitude</em>: {longitude}</li>
</ul>"""
    if link_to_city_page:
        return link_content.format(**city)
    else:
        return nolink_content.format(**city)

def city_desc_page(city):
    return _html.format(_city_desc(city, False))

def city_list_page(cities):
    content = """<ol><li>{}</li></ol>"""

    tmp = "</li><li>".join([_city_desc(cc) for cc in cities])
    return _html.format(content.format(tmp))

def distances_page(distances):
    content = """<ol><li>{}</li></ol>"""

    _deet = """<ul>
<li><em>Distance:</em> {dist}</li>
<li><em>geonameid:</em> <a href="/cities/{geonameid}">{geonameid}</a></li>
</ul>"""
    tmp = "</li><li>".join([_deet.format(**dc) for dc in distances])
    return _html.format(content.format(tmp))


