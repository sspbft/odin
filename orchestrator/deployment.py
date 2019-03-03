from conf import conf
import logging

logger = logging.getLogger(__name__)
SLICE = conf.get_slice()


def generate_hosts_file():
    # TODO implement
    pass


def deploy(regular_nodes, byz_nodes):
    generate_hosts_file()

    for n in regular_nodes:
        deploy_node(n)
    for n in byz_nodes:
        deploy_node(n)


def deploy_node(node):
    logger.info(f"Deploying BFTList to node {node['hostname']}")
