import unittest

from fun.contentGeneratorAI import generate_original_libs, initiate_story


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_crazy_libs(self):
        story = generate_original_libs()
        # print(story.choices[0].text)
        print(story)
        self.assertEqual(True, True)

    def test_initiate_story(self):
        initial_story = initiate_story()
        print(initial_story)
        self.assertEqual(True, True)

    def test_tokenize(self):
        story = generate_original_libs()
        story.tokenize(story)
        print(story.nouns)
        self.assertEqual(True, True)

    def test_make_crazy_story(self):
        story = generate_original_libs()
        story.make_crazy(story, 'hello', 'world')
        self.assertEqual(True, True)

    def test_scratchpad(self):
        for i in range(5):
            if i == 3:
                break
            print(i)

if __name__ == '__main__':
    unittest.main()
