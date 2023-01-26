import json
from typing import List

from flow.models import Flow, Node
from flow.nodes import ALL_NODE_MAP
from flow.nodes.base import NodeContext, ActionNodeHandler, TriggerNodeHandler, LogicNodeHandler


class Executor(object):
    """
    This class is responsible for executing a flow.
    """

    def __init__(self, flow: Flow):
        self.flow = flow

    def execute(self, input_context: NodeContext) -> NodeContext:
        """
        Execute the flow.
        """
        return self.execute_nodes(self.flow.nodes.all(), NodeContext(**input_context))

    def execute_nodes(self, nodes: List[Node], input_context: NodeContext) -> NodeContext:
        """
        Execute the nodes.
        """
        result: NodeContext = NodeContext()
        for node in nodes:
            node_code = node.code
            handler = ALL_NODE_MAP.get(node_code)
            if issubclass(handler, (TriggerNodeHandler, ActionNodeHandler)):
                if node.params:
                    node_params = NodeContext(**node.params)
                else:
                    node_params = NodeContext()
                input_context.update(**node_params)
                result = handler().handle(node, input_context)
            elif issubclass(handler, LogicNodeHandler):
                raise NotImplementedError

        return result
