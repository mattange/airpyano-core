from pahtlib import Path
from glob import iglob

from pygame.mixer import Sound

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
        return self._dict[key]
    
    def initialize(self):
        self._sounds = {i: Sound(f) for i, f in enumerate(self.files)}
        self._is_initialised = True
    
    @property
    def volume(self) -> float:
        return self._volume
    @volume.setter
    def volume(self, value: float):
        if self._is_initialised:
            for sound in self._sounds.items():
                sound.set_volume(value)
        else:
            raise RuntimeError("The interface was not initialised before volume was set.")