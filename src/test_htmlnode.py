import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


#def __init__(self, paraTag = None, paraValue = None, paraChild = None, paraProps = None):


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(
            "p",
            "the tag is supposed to be a paragraph tag",
            {
                "href": "the site",
            }
        )
        
        node2 = HTMLNode(
            "p",
            "the tag is supposed to be a paragraph tag",
            {
                "href": "the site",
            }
        )
        
        self.assertEqual(node.tag, node2.tag)
        
    def test_unimplemented(self):
        node = HTMLNode(
            "p",
            "the tag is supposed to be a paragraph tag",
            paraProps = {
                "href": "the site",
            }
        )
        
        self.assertRaises(NotImplementedError, node.to_html)
        
        
        
    def test_HTMLTypeDiff(self):
        node = HTMLNode(
            "p",
            "the tag is supposed to be a paragraph tag",
            paraProps = {
                "href": "the_site",
            }
        )
        
        self.assertEqual(" href=\"the_site\"", node.props_to_html())
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        
        
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href": "thesiteishere",})
        
        
        self.assertEqual(node.to_html(), "<a href=\"thesiteishere\">Hello, world!</a>")
        
        
        
    # PARENT NODE TESTS
    def test_emptyParent(self):
        node = ParentNode("a", [])
        
        self.assertRaises(ValueError, node.to_html)
        
    def test_mixedChildNodes(self):
        node = ParentNode("p", [
            LeafNode("a", "Hello, world!", {"href": "thesiteishere",}),
            LeafNode("p", "Hello, paragraph world!",),
            LeafNode(None, "Hello, no tag world! "),
            ]
        )
        
        self.assertEqual('<p><a href="thesiteishere">Hello, world!</a><p>Hello, paragraph world!</p>Hello, no tag world! </p>', node.to_html())
        
        
    def test_parentNoTag(self):
        node = ParentNode(None, [LeafNode("a", "Hello, world!", {"href": "thesiteishere",})])
        
        self.assertRaises(ValueError, node.to_html)
        
        
    def test_parentNoChildren(self):
        node = ParentNode("a", None)
        
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertIn("no children for the parent", str(context.exception))
        
        
    def test_parentProps(self): 
        node = ParentNode("div", [
            LeafNode("p", "Hello!"),
            ],
            {"class": "container"}
        )
        
        self.assertEqual('<div class="container"><p>Hello!</p></div>', node.to_html())
        
        
    def test_parentWithParent(self): 
        childNode = LeafNode("span", "child")
        parentNode = ParentNode("div", [childNode])
        
        self.assertEqual("<div><span>child</span></div>", parentNode.to_html())
        
    def test_parentWithManyParent(self):
        grandchildNode = LeafNode("b", "grandchild")
        childNode = ParentNode("span", [grandchildNode])
        parentNode = ParentNode("div", [childNode])
        
        self.assertEqual(
            "<div><span><b>grandchild</b></span></div>",
            parentNode.to_html(),
        )
        
    def test_parentWithChild(self): 
        node = ParentNode("div", [
            LeafNode("p", "Hello!"),
            ],
        
        )
        
        self.assertEqual("<div><p>Hello!</p></div>", node.to_html())
        
        
    def test_differentParentTags(self):
        node = ParentNode("h2", [
            LeafNode("p", "Hello!"),
            ],
        )
        
        self.assertEqual("<h2><p>Hello!</p></h2>", node.to_html())
        
        
        
    
        
        


if __name__ == "__main__":
    unittest.main()