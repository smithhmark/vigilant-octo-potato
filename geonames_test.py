import io

import pytest

import geonames

@pytest.fixture()
def first_data_line():
    return "3039154	El Tarter	El Tarter	Ehl Tarter,Эл Тартер	42.57952	1.65362	P	PPL	AD		02				1052		1721	Europe/Andorra	2012-11-03"

@pytest.fixture()
def first_5_data_lines():
    return """3039154	El Tarter	El Tarter	Ehl Tarter,Эл Тартер	42.57952	1.65362	P	PPL	AD		02				1052		1721	Europe/Andorra	2012-11-03
3039163	Sant Julià de Lòria	Sant Julia de Loria	San Julia,San Julià,Sant Julia de Loria,Sant Julià de Lòria,Sant-Zhulija-de-Lorija,sheng hu li ya-de luo li ya,Сант-Жулия-де-Лория,サン・ジュリア・デ・ロリア教区,圣胡利娅-德洛里亚,圣胡利娅－德洛里亚	42.46372	1.49129	P	PPLA	AD		06				8022		921	Europe/Andorra	2013-11-23
3039604	Pas de la Casa	Pas de la Casa	Pas de la Kasa,Пас де ла Каса	42.54277	1.73361	P	PPL	AD		03				2363	2050	2106	Europe/Andorra	2008-06-09
3039678	Ordino	Ordino	Ordino,ao er di nuo,orudino jiao qu,Ордино,オルディノ教区,奥尔迪诺	42.55623	1.53319	P	PPLA	AD		05				3066		1296	Europe/Andorra	2009-12-11
3040051	les Escaldes	les Escaldes	Ehskal'des-Ehndzhordani,Escaldes,Escaldes-Engordany,Les Escaldes,esukarudesu=engorudani jiao qu,lai sai si ka er de-en ge er da,Эскальдес-Энджордани,エスカルデス＝エンゴルダニ教区,萊塞斯卡爾德-恩戈爾達,萊塞斯卡爾德－恩戈爾達	42.50729	1.53414	P	PPLA	AD		08				15853		1033	Europe/Andorra	2008-10-15
"""

@pytest.fixture()
def sample_file(first_5_data_lines):
    return io.StringIO(first_5_data_lines)

@pytest.fixture()
def sample_raw_record():
    return {
            'geonameid': '3039154',
            'name': 'El Tarter',
            'asciiname': 'El Tarter',
            'alternatenames': 'Ehl Tarter,Эл Тартер',
            'latitude': '42.57952',
            'longitude': '1.65362',
            'feature_class': 'P',
            'feature_code': 'PPL',
            'country_code': 'AD',
            'cc2': '',
            'admin1_code': '02',
            'admin2_code': '',
            'admin3_code': '',
            'admin4_code': '',
            'population': '1052',
            'elevation': '',
            'dem': '1721',
            'timezone': 'Europe/Andorra',
            'modification_date': '2012-11-03',
            }

def test_parse_docs_for_fieldnames():
    fields = geonames.parse_docs_for_fieldnames()
    assert len(fields) == 19
    assert fields[0] == "geonameid"
    assert fields[-4] == 'elevation'

def test_parse_line_raw(first_data_line):
    result = geonames.parse_line_raw(first_data_line)
    assert "geonameid" in result
    assert "elevation" in result
    assert result['geonameid'] == "3039154"
    assert result['elevation'] == ''
    assert "modification_date" in result
    assert "country_code" in result

def test_read_file_raw(sample_file):
    results = geonames.read_file_raw(sample_file)
    assert len(results) == 5

def test_slice_geo_data(sample_raw_record):
    input = [sample_raw_record]
    result = geonames.slice_geo_data(input)
    assert len(result) == 1
    assert len(result[0]) == 2
    assert "latitude" in result[0]
    assert "longitude" in result[0]
    assert isinstance(result[0]["longitude"], float)
    assert isinstance(result[0]["latitude"], float)
