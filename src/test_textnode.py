import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_url(self):
        node = TextNode("test node here", TextType.ITALIC)
        
        self.assertEqual(node.url, None)
        
    def test_textTypeDiff(self):
        node = TextNode("This is a text node", TextType.BOLD, "URL OF DOOM")
        node2 = TextNode("This is a text node", TextType.ITALIC, "URL OF DOOM")
        
        self.assertNotEqual(node, node2)
        
    def test_textDiff(self):
        node = TextNode("This is a text node", TextType.BOLD, "URL OF DOOM")
        node2 = TextNode("This is also a text node, but it's different", TextType.BOLD, "URL OF DOOM")
        
        self.assertNotEqual(node, node2)
        
    def test_textText(self):
        node = TextNode("this is a text node", TextType.TEXT)
        htmlNode = text_node_to_html_node(node)
        
        self.assertEqual(htmlNode.tag, None)
        self.assertEqual(htmlNode.value, "this is a text node")
        
        
    def test_textBold(self):
        node = TextNode("this is a bold node", TextType.BOLD)
        htmlNode = text_node_to_html_node(node)
        
        self.assertEqual(htmlNode.tag, "b")
        self.assertEqual(htmlNode.value, "this is a bold node")
        
    def test_textItalic(self):
        node = TextNode("this is an italic node", TextType.ITALIC)
        htmlNode = text_node_to_html_node(node)
        
        self.assertEqual(htmlNode.tag, "i")
        self.assertEqual(htmlNode.value, "this is an italic node")
        
        
    def test_textCode(self):
        node = TextNode("this is a code node", TextType.CODE)
        htmlNode = text_node_to_html_node(node)
        
        self.assertEqual(htmlNode.tag, "code")
        self.assertEqual(htmlNode.value, "this is a code node")
        
    def test_textLink(self):
        node = TextNode("this is a link node", TextType.LINK, "URL_OF_DOOM")
        htmlNode = text_node_to_html_node(node)
        
        self.assertEqual(htmlNode.tag, "a")
        self.assertEqual(htmlNode.props, {"href": "URL_OF_DOOM"})
        
    def test_textImage(self):
        node = TextNode("this is an image node", TextType.IMAGE, "IMAGE_URL")
        htmlNode = text_node_to_html_node(node)
        
        self.assertEqual(htmlNode.tag, "img")
        self.assertEqual(htmlNode.props, {"src": "IMAGE_URL", "alt": "this is an image node"})
        
    def test_textNoMatch(self):
        node = TextNode("this is an unmatched node", None, "URL_I_GUESS")
        
        
        with self.assertRaises(ValueError) as htmlNode:
            text_node_to_html_node(node)
        self.assertIn("no text type matches", str(htmlNode.exception))
        
    def test_textMismatch(self):
        node = TextNode("this is an mismatched node", TextType.TEXT, "URL_I_GUESS")
        htmlNode = text_node_to_html_node(node)
        
        self.assertEqual(htmlNode.tag, None)
        self.assertEqual(htmlNode.value, "this is an mismatched node")
        #self.assertEqual(htmlNode.url, None)
        
        
        
        
        
        


if __name__ == "__main__":
    unittest.main()