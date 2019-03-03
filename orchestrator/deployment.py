from conf import conf
from helpers import io
import logging
import orchestrator.connector as conn

logger = logging.getLogger(__name__)
SLICE = conf.get_slice()


def generate_hosts_file(nodes):
    with open("hosts.txt", "w") as f:
        for i, n in enumerate(nodes):
            f.write(f"{i},{n['hostname']},1.3.3.7,{5000+i}\n")


def deploy(regular_nodes, byz_nodes):
    generate_hosts_file(regular_nodes + byz_nodes)

    # NOTE that this is just temporary, to avoid faulty deployments on n nodes
    deploy_node(regular_nodes[1])

    # for n in regular_nodes:
    #     deploy_node(n)
    # for n in byz_nodes:
    #     deploy_node(n)


def deploy_node(node):
    logger.info(f"Deploying BFTList to node {node['hostname']}")
    target_dir = conf.get_target_dir()
    hostname = node["hostname"]

    # provision node
    conn.transfer_files(
        hostname,
        [io.get_abs_path("scripts/bootstrap_node.sh")],
        "~"
    )
    conn.run_command(
        hostname,
        "cd ~ && chmod +x bootstrap_node.sh && sh bootstrap_node.sh"
    )
    logger.info(f"Node {hostname} provisioned")

    # transfer app files and set up app
    conn.transfer_files(
        hostname,
        [io.get_abs_path("hosts.txt"),
         io.get_abs_path(conf.get_bootstrap_script())
         ],
        target_dir
    )

    git_url = conf.get_application_git_url()
    app_folder = conf.get_app_folder()
    app_dir = f"{target_dir}/{app_folder}"
    conn.run_command(hostname, f"cd {target_dir} && git clone {git_url}")
    conn.run_command(hostname, f"mv {target_dir}/bootstrap_app.sh {app_dir}")
    conn.run_command(hostname, f"cd {app_dir} && sh bootstrap_app.sh")

    logger.info(f"{app_folder} setup on {hostname}")

    # cleanup
    conn.run_command(hostname, f"rm ~/bootstrap_node.sh")
