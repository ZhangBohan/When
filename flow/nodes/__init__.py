from typing import Dict, Type

from .base import NodeHandler
from .github_loopkup import GithubLookupNodeHandler

ALL_NODE_MAP: dict[str, Type[NodeHandler]] = {
    'github-lookup': GithubLookupNodeHandler,
}
