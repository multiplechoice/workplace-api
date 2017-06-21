from app import valid_date


def test_valid_date():
    assert valid_date('2017-01-01')
    assert valid_date('2017-02-28')


def test_invalid_date():
    assert not valid_date('2017-02-29')
    assert not valid_date('2017-06-31')


def test_mangled_input():
    assert not valid_date('fgyhjbnvhgjknbvhg')
    assert not valid_date('01-01-01')
    assert not valid_date(None)
    assert not valid_date('')
    assert not valid_date('2017-06-21T15:02:32.322340')
    assert not valid_date("Robert'); DROP TABLE Students;--")
