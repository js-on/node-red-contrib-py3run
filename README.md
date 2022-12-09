# node-red-contrib-py3run
Simple node for interacting with Python scripts.

## Installation
- Install package `node-red-contrib-py3run`
- Create folder `/data/python` in your container and store `runner.py` there

## How does it work?
**py3run** invokes a runner script */data/python/runner.py* which tries to import your custom Python script and pass the arguments over. Possible errors will be handled and returned to the three outputs stdout, stderr and rc (return code).

## Usage
Insert a `py3run` node to your flow. Put a function node in front of it to craft the required payload. Or use the node inputs to pass path and args.

Passing no arguments to Python is possible as well. Simply leave *msg.payload.args* or the corresponding input empty. 

The path to the Python script cannot be empty.

## NodeRed function node
```js
msg = {
    payload: {
        path: "/data/python/sample.py",
        args: {
            "a": 1,
            "b": 2
        }
    }
}
return msg;
```

## Python
Put your Python script in any location you want (change it in *msg.payload.path* accordingly). I'd recommend to use a subfolder in /data (like /data/python) and make sure it's mounted to the host system. The script needs to follow a simple structure:

```py
# function name must be run
# function must take exactly one argument `payload` which holds the arguments passed from NodeRed
def run(payload: dict) -> list:
    # Extract values by accessing the key name you used in the payload
    a = payload.get("a")
    b = payload.get("b")
    # Do some basic checks to make sure your data has the correct type / format
    if not a or not b:
        # Error, therefore return None for stdout and an error message for stderr
        return [None, "Either a or b is missing"]
    elif type(a) not in [float, int] or type(b) not in [float, int]:
        # Error, therefore return None for stdout and an error message for stderr
        return [None, "Either a or b is not numeric"]
    
    # return your result in stdout and None for stdout.
    return [a+b, None]
```

If you wanna get rid of checking the input types, you can use the *__types* object in your custom script to map your argument names to a desired type. The runner will check the types at runtime by trying to cast the incoming values to the type if the desired type and incoming type are mismatching. If it fails, you'll get a message on stderr and the script won't run.

```py
# object name must be __types
# object must contain a key (the name of your argument) and the desired type.
__types = {
    "a": int,
    "b": int
}

# same as in first example
def run(payload: dict) -> dict:
    a = payload.get("a")
    b = payload.get("b")
    # But without further checks since runner will check for int or try to cast.
    # Be aware, passing floats to this script will lead to wrong results since they will be converted to int
    return [a+b, None]
```

## Python modules
It is possible to get pip3 running in a NodeRed container, but it's not recommended though.
- Run bash as root inside the container: `docker exec -u root -it <container name> /bin/bash`
- Install py3-pip via apk: `apk install py3-pip`
- Switch back to normal user: `su node-red` or `docker exec -it <container name> /bin/bash`
- Install any module you want: `pip3.10`

> Not every library might work, especially if there are dependencies to any linked libraries (like libvosk.so for the vosk module)


## TODO
- ~~Make payload configurable via frontend by editing the custom nodes UI part (input for path and JSON)~~
- Add modules (like in function setup) where you can enter Python modules which then will be tried to install
- ~~Add var *__types* to custom scripts to define the expected input type. The runner will then be able to do a pre-check of the arguments to save work in the custom script.~~

## Contribute
Please report bugs or send a pull request and I try to fix, review and merge asap. 