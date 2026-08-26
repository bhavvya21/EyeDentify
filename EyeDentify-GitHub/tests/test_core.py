import unittest

from eyedentify.core import Detection, horizontal_position, meters_to_steps, navigation_message


class CoreTests(unittest.TestCase):
    def test_direction_boundaries(self):
        self.assertEqual(horizontal_position(0.1), "to your left")
        self.assertEqual(horizontal_position(0.5), "in front")
        self.assertEqual(horizontal_position(0.9), "to your right")

    def test_steps_are_human_friendly(self):
        self.assertEqual(meters_to_steps(0.2, 0.75), 1)
        self.assertEqual(meters_to_steps(1.5, 0.75), 2)
        self.assertIsNone(meters_to_steps(None, 0.75))

    def test_navigation_message(self):
        detection = Detection("person", 0.9, 0.7, 0.0, 0.9, 1.0)
        self.assertEqual(navigation_message(detection, 1.5, 0.75, 0.34), "person 2 steps away, to your right.")


if __name__ == "__main__":
    unittest.main()
