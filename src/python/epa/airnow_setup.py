from typing import List
import sys
import os
import yaml

from nsaph.util.shapes import install


def setup(args: List[str]):
    f = ".airnow.yaml"
    api_key = "api key"
    shapes = "shapes"
    if os.path.isfile(f):
        cfg = yaml.safe_load(f)
    else:
        cfg = dict()
    if api_key not in cfg:
        if len(args) < 1:
            raise ValueError("No AirNow API Key is provided")
    if len(sys.argv) > 0:
        cfg[api_key] = args[0]
    if shapes in cfg:
        for shape in cfg[shapes]:
            if not os.path.isfile(shape):
                raise ValueError("Shape file {} does not exist.".format(shape))
    else:
        dest = "shapes"
        shps = install(dest)
        cfg[shapes] = shps
        # [os.path.abspath(shape) for shape in shps]
    with open(f, "wt") as out:
        yaml.safe_dump(cfg, out)
    print("All Done")


if __name__ == '__main__':
    setup(sys.argv[1:])
