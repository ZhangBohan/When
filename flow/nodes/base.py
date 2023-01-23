from abc import ABC

from flow.models import Node, Flow


class NodeContext(dict):
    pass


class NodeHandler(object):
    """
    Base class for all node handlers.
    """

    def handle(self, node: Node, context: NodeContext):
        """
        Handle the node.
        """
        raise NotImplementedError

    def save(self, flow: Flow, node: Node):
        """
        Save the node. This method is called after the node is saved in flow.
        """
        raise NotImplementedError


class TriggerNodeHandler(NodeHandler, ABC):
    """
    Base class for all trigger node handlers.
    """
    pass


class ActionNodeHandler(NodeHandler, ABC):
    """
    Base class for all action node handlers.
    """
    pass


class LogicNodeHandler(NodeHandler, ABC):
    """
    Base class for all logic node handlers.
    """
    pass
