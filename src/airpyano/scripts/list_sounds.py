import pkgutil
from .. import sounds as snd

def main():

    names = [mi.name for mi in pkgutil.iter_modules(snd.__path__)]
    print('The available sound modules are:')
    for name in names:
        print(f'    - {name}')
