#!/usr/bin/python3

import subprocess
from functools import reduce
import json
import sys
import os
import signal

last_cmd = 'ish_last_cmd'


def signal_handler(_sig, _frame):
    print("")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def resolve_param(entry, index):
    return entry[index]


def resolve_args(_, index):
    if len(sys.argv) > index:
        return sys.argv[index]
    return None


def resolve_static(_, param):
    return param


resolvers = {
    "param": resolve_param,
    "arg": resolve_args,
    "static": resolve_static
}


def get_entries(query):
    result_list = subprocess.check_output(query['cmd'])

    str_list = [x.decode('utf-8') for x in result_list.splitlines()]
    return [' '.join(x.split()).split(' ') for x in str_list]


def cal_width(entries):
    entry_len = len(entries[0])
    widths = reduce(lambda a, b: mx_width(a, b), entries, [0] * entry_len)
    return widths


def mx_width(widths, entry):
    for idx, ele in enumerate(entry):
        widths[idx] = max(widths[idx], len(ele) + 2)

    return widths


def generate_format_string(entries, alignments):
    widths = cal_width(entries)
    fmt = [f"{{{idx}:{alignments[idx]}{widths[idx]}}}" for idx in range(len(entries[0]))]
    return " ".join(fmt)


def show_list(entries, alignments):
    fmt = generate_format_string(entries, alignments)
    for entry in entries:
        print(fmt.format(*entry))


def resolve_format(entry, fmt_list):
    resolved = ""
    for fmt in fmt_list:
        if type(fmt) is str:
            resolved += (fmt + ' ')
        else:
            value = resolvers[fmt['type']](entry, fmt['param'])
            if value is None:
                return value

            resolved += value
            if fmt.get('post_space', True):
                resolved += ' '

    return resolved.strip()


def run_command(entry, command_params):
    msg_fmt = command_params['msg_fmt']
    cmd_fmt = command_params['cmd_fmt']

    print(resolve_format(entry, msg_fmt))

    cmd = resolve_format(entry, cmd_fmt)
    print("Executing " + cmd)

    subprocess.call(cmd.split(' '))

    with open(last_cmd, 'w') as ish_last:
        ish_last.write(cmd)


def filter_entry(entry, runner_config):
    if "filter" in runner_config:
        filter_params = runner_config['filter']
        value = resolve_format(entry, filter_params['value'])
        if value is None:
            return True

        column = resolve_format(entry, filter_params['column'])

        return value in column
    return True


def main(command):
    runner_config = json.load(open(os.path.join(os.environ['ISH_RUN_SCRIPTS'], f"{command}.json")))
    entries = get_entries(runner_config['query'])
    filtered = [entry for entry in entries if filter_entry(entry, runner_config)]

    if len(filtered) == 0:
        print("No results found. Exiting")
        exit(0)

    enumerated_list = [[str(idx)] + entry for idx, entry in enumerate(filtered)]
    alignments = [''] * len(enumerated_list[0])

    alignments[0] = '>'  # Set alignment for entry index

    show_list(enumerated_list, alignments)

    while True:
        selection = -1
        print(runner_config["task"])
        input1 = input("Select entry: ").strip()
        if len(input1) > 0:
            selection = int(input1)

        if 0 <= selection < len(filtered):
            run_command(filtered[selection], runner_config['run_cmd'])
            break
        else:
            print(f"Select value between 0 and {len(filtered) - 1}")


if __name__ == '__main__':
    main(sys.argv[1])
