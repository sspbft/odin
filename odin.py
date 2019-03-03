from conf import conf
from orchestrator.deployment import deploy_as_byz_node, deploy_as_normal_node
import api.pl as api
import logging

logger = logging.getLogger(__name__)


def setup_logging():
    """Configures the logging for Odin."""
    FORMAT = "\033[94mOdin.%(name)s ==> [%(levelname)s] : " + \
             "%(message)s\033[0m"
    logging.basicConfig(format=FORMAT, level=logging.INFO)


def launch():
    pl_slice = conf.get_slice()
    node_count = conf.get_number_of_nodes()
    byz_count = conf.get_number_of_byzantine()

    nodes = api.get_nodes_for_slice(pl_slice, node_count)
    regular_nodes = nodes[byz_count:]
    byz_nodes = nodes[:byz_count]

    for n in regular_nodes:
        deploy_as_normal_node(n)

    for n in byz_nodes:
        deploy_as_byz_node


if __name__ == "__main__":
    setup_logging()
    launch()
