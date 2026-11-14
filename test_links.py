from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import unittest


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        self.links.extend(value for key, value in attrs if key in ('href', 'src') and value)


class LinkTests(unittest.TestCase):
    def test_all_local_navigation_and_images_resolve(self):
        root = Path(__file__).parent
        for file in root.rglob('*.html'):
            parser = LinkParser()
            parser.feed(file.read_text(encoding='utf-8'))
            for link in parser.links:
                parsed = urlsplit(link)
                if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith('/'):
                    continue
                with self.subTest(page=str(file.relative_to(root)), link=link):
                    self.assertTrue((file.parent / unquote(parsed.path)).is_file())


if __name__ == '__main__':
    unittest.main()
