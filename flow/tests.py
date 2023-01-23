import responses
from django.test import TestCase
from jinja2 import Environment

from flow.models import Node
from flow.nodes import ALL_NODE_MAP
from flow.nodes.base import NodeContext
from flow.nodes.github_loopkup import GithubLookupNodeHandler


class JinjaTest(TestCase):

    def testBoolean(self):
        env = Environment()
        expr = env.compile_expression('foo == 42')
        flag = expr(foo=23)
        self.assertFalse(flag)
        flag = expr(foo=42)
        self.assertTrue(flag)

    def testProperty(self):
        env = Environment()
        expr = env.compile_expression('foo.bar')
        result = expr(foo=dict(bar=1))
        self.assertEqual(result, 1)
        self.assertTrue(type(result) == int)


class GithubLookupTest(TestCase):

    @responses.activate
    def test_lookup(self):
        """
        mock request
        :return:
        """
        user = "ZhangBohan"
        url = f"https://api.github.com/users/{user}"
        responses.add(responses.GET, url, json={'login': user}, status=200)
        result = GithubLookupNodeHandler().handle(Node(), NodeContext(user='ZhangBohan'))
        self.assertEqual(result['login'], 'ZhangBohan')


class NodeTest(TestCase):
    def test_get_node_by_name(self):
        node = ALL_NODE_MAP['github-lookup']
        self.assertEqual(node, GithubLookupNodeHandler)


class CeleryTest(TestCase):

    def test_celery(self):
        from flow.tasks import add
        result = add.delay(1, 2)
        self.assertEqual(3, result.get())
