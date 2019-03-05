from conf import conf
from helpers import io
from threading import Thread, Event
import logging
import socket
import orchestrator.connector as conn

logger = logging.getLogger(__name__)
SLICE = conf.get_slice()


def generate_hosts_file(nodes):
    with open("hosts.txt", "w") as f:
        for i, n in enumerate(nodes):
            ip = socket.gethostbyname(n["hostname"])
            f.write(f"{i},{n['hostname']},{ip},{5000+i}\n")


def deploy(regular_nodes, byz_nodes):
    generate_hosts_file(regular_nodes + byz_nodes)

    threads = []
    i = 0
    for n in regular_nodes:
        threads.append(Thread(target=deploy_and_run, args=(n, i)))
        i += 1
    for n in byz_nodes:
        threads.append(Thread(target=deploy_and_run, args=(n, i)))
        i += 1

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    logger.info("Application deployed and running!")

    i = 0
    for n in regular_nodes:
        logger.info(f"Node {i} running on {n['hostname']}")
        i += 1
    for n in byz_nodes:
        logger.info(f"Byzanting node {i} running on {n['hostname']}")
        i += 1
    forever = Event()
    forever.wait()


def deploy_and_run(node, node_id):
    deploy_node(node)
    launch_using_thor(node["hostname"], node_id)
    return


def deploy_node(node):
    logger.info(f"Deploying BFTList to node {node['hostname']}")
    target_dir = conf.get_target_dir()
    hostname = node["hostname"]

    conn.run_command(hostname, f"pkill -u {conf.get_slice()}")

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
    return conn.run_command(hostname, f"rm ~/bootstrap_node.sh")


def launch_using_thor(hostname, i):
    thor_dir = f"{conf.get_target_dir()}/thor"
    n = conf.get_number_of_nodes()
    f = conf.get_number_of_byzantine()
    p = conf.get_abs_path_to_app()
    e = conf.get_app_entrypoint()
    lp = f"{conf.get_target_dir()}/application.log"
    cmd_string = (f"cd {thor_dir} && source ./env/bin/activate && python " +
                  f"thor.py -n {n} -f {f} -p {p} -e '{e}' -i {i} -lp {lp} " +
                  f"planetlab &")
    return conn.run_command(hostname, cmd_string)
