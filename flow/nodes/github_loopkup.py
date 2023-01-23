import requests
import logging

from flow.exceptions import NodeException
from flow.models import Node, Flow
from flow.nodes.base import ActionNodeHandler, NodeContext

logger = logging.getLogger(__name__)


class GithubLookupNodeHandler(ActionNodeHandler):

    def handle(self, node: Node, context: NodeContext):
        user = context.get("user")
        url = f"https://api.github.com/users/{user}"
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"Failed to get user {user} from github. status: {response.status_code}, response: {response.text}")
            raise NodeException("User not found")
        return response.json()

    def save(self, flow: Flow, node: Node):
        pass    # do nothing temporarily


