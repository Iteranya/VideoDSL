from src.module import VideoModule
from src.compiler import compile
# -------------------------------------------------------
# This is the Example of a Single File Script
# -------------------------------------------------------

# So like, a standalone script will compile into a single script
# Think of it like a single 100k words word document.
# If that your style, this is how you do it

from characters import Hikarin # Import characters you've defined in characters.py
vm = VideoModule()
h = Hikarin
storyName = "Testing" # This will be the name of the Json File

def video():
    vm.start()
    vm.background("end.png")
    vm.play_music("mice.ogg")
    vm.time(5.0)
    vm.show(h,"normal")
    vm.speak(h,"This is the part where I gaze at your soul for an indefinite amount of time","line.ogg")
    vm.time(5.0)
    vm.finish()
    return vm.dialogueDict


def main():compile(storyname=storyName,script=video()) 
if __name__ == "__main__":
    main() 