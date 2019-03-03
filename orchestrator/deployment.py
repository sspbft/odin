import logging
import orchestrator.connector as conn


logger = logging.getLogger(__name__)


def generate_hosts_file():
    pass

def deploy(regular_nodes, byz_nodes):
    generate_hosts_file()
    
    for n in regular_nodes:
        deploy_node(n)
    for n in byz_nodes:
        deploy_node(n)


def deploy_node(node):
    logger.info(f"Deploying BFTList to node {node['hostname']}")