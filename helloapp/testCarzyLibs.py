import unittest

from helloapp.crazyLibs import generate_crazy_libs, initiate_story


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_crazy_libs(self):
        story = generate_crazy_libs()
        # print(story.choices[0].text)
        print(story)
        self.assertEqual(True, True)

    def test_initiate_story(self):
        initial_story = initiate_story()
        print(initial_story)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
