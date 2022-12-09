#
# Created on Thu Dec 08 2022
#
# Copyright (c) 2022 js-on
#
import contextlib
import importlib
import json
import sys
import os


def output(stdout: str = None, stderr: str = None, rc: int = 0):
    if stdout:
        sys.stdout.write(stdout)
    if stderr:
        sys.stderr.write(stderr)
    exit(rc)


def parse_args(args: dict, types: dict):
    for k, t in types.items():
        if k in args:
            try:
                if not isinstance(args[k], t):
                    args[k] = t(args[k])
            except Exception:
                output(
                    stderr=f"Type mismatch for {k}. Expected {t} but got {type(args[k])}")


def main():
    fpath = sys.argv[1]
    if not os.path.exists(fpath):
        output(stderr=f"File '{fpath}' does not exist", rc=1)

    try:
        payload = sys.argv[2] or r"{}"
        json.loads(payload)
        if isinstance(payload, str):
            payload = json.loads(payload)
    except Exception as e:
        output(stderr="Invalid JSON passed to runner.", rc=1)

    folder = '/'.join(fpath.split('/')[:-1])
    modname = fpath.split("/")[-1].split(".")[0]
    sys.path.insert(1, folder)
    try:
        module = importlib.import_module(modname)
    except Exception:
        output(stderr="Could not import module.", rc=1)

    with contextlib.suppress(Exception):
        # Quit and stderr of types are not matching
        parse_args(payload, module.__types)

    try:
        data = module.run(payload)
        if data[0]:
            output(stdout=str(data[0]), rc=0)
        elif data[1]:
            output(stderr=str(data[1]), rc=1)
    except Exception as e:
        output(
            stderr=f"Something went wrong running the module. {repr(e)}", rc=1)


if __name__ == "__main__":
    main()
