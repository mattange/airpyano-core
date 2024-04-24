from pathlib import Path
from glob import iglob

from pygame import mixer

class SoundsIterface():

    def __init__(self, name: str, root_dir: Path, pathname: str = '*'):
        self.name = name
        self.root_dir = root_dir
        self.files = sorted([f for f in iglob(pathname, root_dir=root_dir)])
        self._volume = 1.
        self._is_initialised = False

    def __len__(self):
        return len(self.files)

    def __getitem__(self, key):
        if self._is_initialised:
            return self._sounds[key]
        else:
            raise RuntimeError("The interface was not initialised before retrieving a Sound object.")
    
    def initialise(self, mixer: mixer):
        if mixer.get_init() is None:
            mixer.init()
        self._sounds = {i: mixer.Sound(self.root_dir / f) for i, f in enumerate(self.files)}
        self._is_initialised = True
    
    @property
    def volume(self) -> float:
        return self._volume
    @volume.setter
    def volume(self, value: float):
        if self._is_initialised:
            for sound in self._sounds.values():
                sound.set_volume(value)
        else:
            raise RuntimeError("The interface was not initialised before volume was set.")