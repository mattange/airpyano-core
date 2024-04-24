import pkgutil
import importlib
from argparse import ArgumentParser, ArgumentTypeError

from pygame import mixer

from .. import sounds as snd
from ..core.sounds_interface import SoundsIterface

MIN_LENGTH = 50 # used this as random meaningful number
MAX_LENGTH = 390 # should not be superior to MAX_DISTANCE - MIN_DISTANCE

MIN_DISTANCE = 10 # should not be inferior to the minimum distance of the sensor
MAX_DISTANCE = 400 # max distance of the sensor

def pyano_length(arg):
    try:
        f = int(arg)
    except ValueError:    
        raise ArgumentTypeError("Length must be an integer number")
    if f < MIN_LENGTH or f > MAX_LENGTH:
        raise ArgumentTypeError("Length must be < " + str(MAX_LENGTH) + "and > " + str(MIN_LENGTH))
    return f

def pyano_start(arg):
    try:
        f = int(arg)
    except ValueError:    
        raise ArgumentTypeError("Start must be an integer number")
    if f < MIN_DISTANCE:
        raise ArgumentTypeError("Start must be > " + str(MIN_DISTANCE))
    return f

def main():

    argparser = ArgumentParser(prog="pyano")
    argparser.add_argument("-s","--sounds",
                           type=str,
                           choices=[mi.name for mi in pkgutil.iter_modules(snd.__path__)],
                           required=True,
                           help="The sounds package to use.")
    argparser.add_argument("-n","--interface-name",
                           type=str,
                           required=False,
                           help="The sounds interface name to use, inside the sounds package specified. If not provided, defaults to the sounds package name.")
    argparser.add_argument("--length",
                           type=pyano_length,
                           required=False,
                           default=100,
                           help="The maximum length to use for the airpyano from its start, in cm. Defaults to 100.")
    argparser.add_argument("--start",
                           type=pyano_start,
                           required=False,
                           default=10,
                           help="The minimum start distance from the sensor to use for the airpyano, in cm. Defaults to 10.")
    argparser.add_argument("--channels",
                           type=int,
                           required=False,
                           default=8,
                           help="The number of mixer channels to use for the airpyano. Defaults to 8.")
    
    args = argparser.parse_args()

    length = args.length
    start = args.start
    if length + start > MAX_DISTANCE:
        raise RuntimeError(f'Length + start cannot be > {MAX_DISTANCE}')
    
    min_distance = float(start)
    max_distance = float(length + start)

    sounds_module_name = args.sounds
    sounds_module_full_name = "airpyano.sounds." + sounds_module_name
    sounds_module = importlib.import_module(sounds_module_full_name)

    sounds_interface_name = args.interface_name
    if sounds_interface_name is None:
        sounds_interface_name = sounds_module_name
    
    sounds = getattr(sounds_module, sounds_interface_name)

    if not isinstance(sounds, SoundsIterface):
        raise RuntimeError(f'Interface {sounds_interface_name} is not of type SoundsInterface')
    
    pyano_key_width = (max_distance - min_distance) / len(sounds)

    channels = args.channels
    mixer.init()
    mixer.set_num_channels(channels)
    sounds.initialise(mixer)

    print(f'this sounds package has {len(sounds)} sounds')
    print(f'the width of each key is {pyano_key_width}')
    print('ready to play')
    import time
    for i in range(len(sounds)):
        print(i)
        sounds[i].play()
        time.sleep(0.5)
