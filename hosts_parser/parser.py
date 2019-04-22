import argparse
import time
from collections import Counter
from itertools import islice
from os import path

# Five minutes as default edge time to look for
DEFAULT_MILLISECONDS_EDGE_TIME = 300000


def parse_input_line(line):
    """Parses an input line.

    Args:
      line: string line from input.
    Returns:
      tuple with timestamp and hosts. If line is not valid None.
    """
    row = line.split()
    if len(row) < 3:
        return None
    timestamp = int(row[0])
    return timestamp, row[1:]


def find_host_lines_in_time(file_path, init_time, end_time, selected_host):
    """Finds lines in input with the selected_host between the timestamps.

    Args:
      file_path: path to input file
      init_time: start of the valid period of time
      end_time: end of the valid period of time
      selected_host: name of hosts to find
    Returns:
      list of lines found
    """
    lines_found = []
    with open(file_path) as input_file:
        for line in input_file:
            try:
                timestamp, hosts = parse_input_line(line)
                if (selected_host in hosts and
                    init_time <= timestamp <= end_time):
                    lines_found.append((timestamp, hosts[0], hosts[1]))
                if timestamp > end_time + DEFAULT_MILLISECONDS_EDGE_TIME:
                    break
            except TypeError:
                continue
    return lines_found


def review_lines_in_slice(file_path, init_line=0, selected_host=None):
    """Finds lines in input with the selected_host between the timestamps.

    Args:
      file_path: path to input file
      init_line: line from which input will be process
      selected_host: name of hosts to find
    Returns:
      number of last line readed, list of connection from selected_host,
      list of connection to selected_host and hosts counter with the hosts seen
      in the readed lines.
    """
    connections_from = []
    connections_to = []
    host_counter = Counter()
    last_line = init_line
    with open(file_path) as input_file:
        for line in islice(input_file, init_line, None):
            try:
                timestamp, hosts = parse_input_line(line)
                host_counter.update(hosts)
                if selected_host == hosts[0]:
                    connections_from.append((timestamp, hosts[0], hosts[1]))
                if selected_host == hosts[1]:
                    connections_to.append((timestamp, hosts[0], hosts[1]))
            except TypeError:
                continue
            last_line += 1
    return (last_line, connections_from, connections_to, host_counter)


def show_lines(lines):
    """ Prints lines of hosts connections """
    for line in lines:
        print('{}: {} -> {}'.format(*line))


def show_counter(counter, n_top=5):
    """ Prints n_top hosts with the most reference with format """
    top_hosts = counter.most_common(n_top)
    print('Top {} hosts seen the most'.format(n_top))
    for host in top_hosts:
        print('Host {}: {} conn'.format(*host))


def follow_option_loop(file_path, selected_host, period=600):
    """ Keeps reading from input file forever

    Args:
      file_path: path to input file
      selected_host: name of hosts to find
      period: number of seconds to wait before processing the file again
    """
    last_line = 0
    while True:
        last_line, connections_from, connections_to, host_counter = \
            review_lines_in_slice(file_path, last_line, selected_host)
        if len(host_counter) > 0:
            print('Connections to host {} found: {}'.format(
                selected_host, len(connections_to)))
            show_lines(connections_to)
            print('Connections from host {} found: {}'.format(
                selected_host, len(connections_from)))
            show_lines(connections_from)
            show_counter(host_counter)
        else:
            print('No new lines found')
        time.sleep(period)


def main(file_path, init_time, end_time, selected_host, follow_option, period):
    """ Main method of the script. This encapsulates the option of the
        script logics
    """
    if init_time is not None and end_time is not None:
        lines_found = find_host_lines_in_time(
            file_path, init_time, end_time, selected_host)
        show_lines(lines_found)
        return

    elif follow_option:
        try:
            follow_option_loop(file_path, selected_host, period)
        except KeyboardInterrupt:
            return

    else:
        last_line, connections_from, connections_to, host_counter = \
            review_lines_in_slice(file_path, 0, selected_host)
        show_counter(host_counter)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Parser a hosts log file')
    parser.add_argument('-i', '--input-file', dest='file_path', metavar='PATH',
        action='store', help='path to the file to parse', required=True)
    parser.add_argument('--init-time', dest='init_time', metavar='TIME',
        type=int, action='store',
        help='time from which to look up lines in the file')
    parser.add_argument('--end-time', dest='end_time', metavar='TIME',
        type=int, action='store',
        help='time until which to look up lines in the file')
    parser.add_argument('--host', dest='selected_host', metavar='HOST',
        type=str, action='store', help='host to look up for in the file')
    parser.add_argument('-f', '--follow', dest='follow_option',
        action='store_true', help='show as the file increase every period')
    parser.add_argument('--period', dest='period', metavar='SEG',
        type=int, action='store', default=600,
        help='seconds between checking the file. only works with follow')

    args = parser.parse_args()

    if not path.isfile(args.file_path):
        raise FileNotFoundError()

    main(
        args.file_path,
        args.init_time,
        args.end_time,
        args.selected_host,
        args.follow_option,
        args.period
    )
