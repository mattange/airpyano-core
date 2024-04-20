from pathlib import Path

from ...core.sounds_interface import SoundsIterface

local_folder = Path(__file__)
sounds_folder = local_folder / "source"
beet_box = SoundsIterface("beet_box", sounds_folder, '*.wav')
