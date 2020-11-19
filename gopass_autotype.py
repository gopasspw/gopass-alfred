#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import time
from os.path import expanduser

home = expanduser("~")
my_env = os.environ.copy()
my_env['PATH'] = '/usr/local/bin:{}'.format(my_env['PATH'])

special_autotype_handlers = {
    ":tab": lambda: do_stroke(48),
    ":space": lambda: do_stroke(49),
    ":enter": lambda: do_stroke(36),
    ":delay": lambda: time.sleep(1)
}

def get_additional_autotype_handlers_filename():
    base_path = os.getenv("XDG_CONFIG", home)
    return '{base_path}/{filename}'.format(base_path = base_path, filename = ".gopass_autotype_handlers.json")

def load_additional_autotype_handlers_config():
    handlers_path = get_additional_autotype_handlers_filename()
    if os.path.exists(handlers_path):
        with open(handlers_path) as f:
            return json.load(f)
    else:
        return {}

def execute_additional_autotype_handler(command):
    command_result = os.popen(command).read()
    print(command + " > " + str(command_result))
    do_type(command_result)

def load_additional_autotype_handlers():
    config = load_additional_autotype_handlers_config()
    return {k: lambda: execute_additional_autotype_handler(v) for k, v in config.items()}


def all_autotype_handlers():
    additional = load_additional_autotype_handlers()
    return {**additional, **special_autotype_handlers}

def do_type(to_type):
    os.system(f"echo 'tell application \"System Events\" to keystroke \"{to_type}\"' | osascript")


def do_stroke(stroke):
    os.system(f"echo 'tell application \"System Events\" to key code \"{stroke}\"' | osascript")


def get_gopass_data_for(query):
    return subprocess.run(["gopass", "show", "-f", query], stdout=subprocess.PIPE, env=my_env).stdout.decode("utf-8")


def parse_gopass_data(data):
    lines = data.split("\n")
    password = lines[0]
    non_empty_lines = list(filter(lambda line: len(line) > 0, lines))
    lines_splitted = map(lambda line: line.split(": "), non_empty_lines[1:])
    lines_with_two_items = filter(lambda elements: len(elements) == 2, lines_splitted)
    items_dict = {item[0]: item[1] for item in lines_with_two_items}
    items_dict["pass"] = password
    return items_dict


def autotype(items, field):
    autotype = items.get(field)
    handlers = all_autotype_handlers()
    if autotype is None:
        return
    to_type = autotype.split(" ")
    for word in to_type:
        handler = handlers.get(word)
        if handler is None:
            mapped = items.get(word)
            do_type(word if mapped is None else mapped)
        else:
            handler()


def autotype_list(path, parsed):
    return [
        {
            "uid": result,
            "title": result,
            "subtitle": path,
            "arg": f"{path} {result}",
            "autocomplete": result
        } for result in parsed.keys()
    ]


action = sys.argv[1]
path = sys.argv[2].split(" ")

data = get_gopass_data_for(path[0])
parsed = parse_gopass_data(data)
autotype_action = "autotype" if len(path) == 1 else path[1]

if action == 'list':
    print(json.dumps({'items': autotype_list(path[0], parsed)}))
elif action == 'autotype':
    autotype(parsed, autotype_action)
