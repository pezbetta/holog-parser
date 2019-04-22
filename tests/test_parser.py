from distutils import dir_util
from pytest import fixture
import os

from hosts_parser.parser import parse_input_line, find_host_lines_in_time, \
    review_lines_in_slice


@fixture
def datadir(tmpdir, request):
    '''
    Fixture responsible for finding files to be use in testing and
    moving all to a temporary directory.
    '''
    filename = request.module.__file__
    test_dir = str(os.path.join(os.path.dirname(filename), 'files'))

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


def test_parse_input_line():
    assert parse_input_line('1565647212986 Tyreonna Rehgan ') == \
        (1565647212986, ['Tyreonna', 'Rehgan'])

def test_parse_empty_line():
    assert(parse_input_line(' ') is None)


def test_find_lines_in_time_for_server(datadir):
    lines = find_host_lines_in_time(
        datadir.join('input_text.txt'),
        1565647204351,
        1565647313867,
        'Heera'
    )
    assert(len(lines) == 4)


def test_find_lines_in_time_for_server_with_empty_lines(datadir):
    lines = find_host_lines_in_time(
        datadir.join('input_text_empty_lines.txt'),
        1565647204351,
        1565647313867,
        'Heera'
    )
    assert(len(lines) == 4)


def test_find_lines_in_time_for_server_fyodor(datadir):
    lines = find_host_lines_in_time(
        datadir.join('input-file-10000.txt'),
        1565647328946,
        1565715048655,
        'Fyodor'
    )
    assert(len(lines) == 2)


def test_review_lines_in_slice(datadir):
    last_line, connections_from, connections_to, host_counter = \
        review_lines_in_slice(datadir.join('input_text.txt'), init_line=5)
    assert(last_line == 15)
    assert(connections_from == [])
    assert(connections_to == [])
    assert(host_counter.get('Heera') == 3)


def test_review_lines_in_slice_from_end_of_file(datadir):
    last_line0, connections_from, connections_to, host_counter = \
        review_lines_in_slice(datadir.join('input_text.txt'), init_line=10)
    last_line1, connections_from, connections_to, host_counter = \
        review_lines_in_slice(datadir.join('input_text.txt'), init_line=last_line0)
    assert(last_line1 == last_line0)
    assert(len(host_counter) == 0)


def test_review_lines_in_slice_with_host(datadir):
    last_line, connections_from, connections_to, host_counter = \
        review_lines_in_slice(
            datadir.join('input_text.txt'), init_line=0, selected_host='Heera')
    assert(last_line == 15)
    assert(connections_from[0] == (1565647228897, 'Heera', 'Eron'))
    assert(connections_to[0] == (1565647264445, 'Jil', 'Heera'))
    assert(host_counter.get('Heera') == 4)
