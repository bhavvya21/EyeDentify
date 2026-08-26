import unittest

from eyedentify.app import EyeDentifyApp
from eyedentify.config import DEFAULTS
from eyedentify.core import Mode
from eyedentify.hardware import SimulatedHardware
from eyedentify.reading import SimulatedReader
from eyedentify.vision import SimulatedCamera, SimulatedDetector


class RecordingSpeaker:
    def __init__(self): self.messages = []
    def say(self, message): self.messages.append(message)


class AppTests(unittest.TestCase):
    def test_detect_mode_and_cooldown(self):
        speaker = RecordingSpeaker()
        app = EyeDentifyApp(DEFAULTS, SimulatedHardware(distance_m=1.5), SimulatedCamera(), SimulatedDetector(), SimulatedReader(), speaker, clock=lambda: 10.0)
        app.hardware.distance_m = lambda: 1.5
        app.tick(); app.tick()
        self.assertEqual(speaker.messages, ["Detection mode.", "person 2 steps away, to your right."])

    def test_switch_to_read_mode(self):
        speaker = RecordingSpeaker()
        hardware = SimulatedHardware(initial_mode=Mode.READ)
        app = EyeDentifyApp(DEFAULTS, hardware, SimulatedCamera(), SimulatedDetector(), SimulatedReader(), speaker, clock=lambda: 10.0)
        app.tick()
        self.assertEqual(speaker.messages, ["Reading mode.", "Caution: Wet Floor."])


if __name__ == "__main__":
    unittest.main()
