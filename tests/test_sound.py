
def test_single_sound():
    from airpyano.sounds.beet_box import beet_box
    from pygame import mixer
    import time

    mixer.init()
    beet_box.initialise(mixer)
    
    beet_box[0].play()
    time.sleep(5)
    beet_box[1].play()

    assert(True)
