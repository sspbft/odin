import logging


logger = logging.getLogger(__name__)


def deploy_as_normal_node(node):
    logger.info(f"Deploying BFTList to normal node {node['hostname']}")


def deploy_as_byz_node(node):
    logger.info(f"Deploying BFTList to byzantine node {node['hostname']}")