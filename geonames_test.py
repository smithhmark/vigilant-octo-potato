
import geonames
import pytest

@pytest.fixture()
def first_data_line():
    return "3039154	El Tarter	El Tarter	Ehl Tarter,Эл Тартер	42.57952	1.65362	P	PPL	AD		02				1052		1721	Europe/Andorra	2012-11-03"



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

