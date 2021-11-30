import unittest
class TestFoo(unittest.TestCase):
    def test_foo(self):
        t = foo('foo')
        self.assertEqual(t, 'FOO')

class DefaultWidgetSizeTestCase(unittest.TestCase):
    def test_default_widget_size(self):
        widget = Widget('The widget')
        r = widget.size()
        self.assertEqual(r, (50, 50))

class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget('The widget')
    def test_default_widget_size(self):
        self.assertEqual(self.widget.size(), (50,50))
    def test_widget_resize(self):
        self.widget.resize(100,150)
        self.assertEqual(self.widget.size(), (100,150))
    def tearDown(self):
        self.widget.dispose()

class TestStringMethods(unittest.TestCase):
    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
    with self.assertRaises(TypeError):
        s.split(2)
