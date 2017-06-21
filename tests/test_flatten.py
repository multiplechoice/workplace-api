from app import flatten


def test_list_of_lists():
    # flatten returns an iterable so we need to convert it to a list
    # the method only removes one level of nesting
    assert list(flatten([[1], [2], [3]])) == [1, 2, 3]
    assert list(flatten([[[1]], [2], [3]])) == [[1], 2, 3]
    # but multiple levels can be removed, but only when the depth is equivalent
    assert list(flatten(flatten([[[1]], [[2]], [[3]]]))) == [1, 2, 3]
