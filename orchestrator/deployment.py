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


def deploy(byz_nodes, regular_nodes, args):
    if not args.reuse_hosts:
        generate_hosts_file(byz_nodes + regular_nodes)

    threads = []
    i = 0
    for n in byz_nodes + regular_nodes:
        t = Thread(target=deploy_and_run, args=(n, i, args))
        t.start()
        threads.append(t)
        i += 1

    for t in threads:
        t.join()

    logger.info("Application deployed and running!")

    i = 0
    for n in byz_nodes + regular_nodes:
        logger.info(f"Node {i} running on {n['hostname']}")
        i += 1

    forever = Event()
    forever.wait()


def deploy_and_run(node, node_id, args):
    ret_code = deploy_node(node)
    if ret_code != 0:
        logger.error(f"Deployment to {node['hostname']} failed")
    logger.info(f"Launching app on host {node['hostname']} with " +
                f"ID {node_id}")
    launch_using_thor(node["hostname"], node_id, args)
    return


def deploy_node(node):
    git_url = conf.get_application_git_url()
    git_branch = conf.get_application_git_branch()
    app_folder = conf.get_app_folder()
    target_dir = conf.get_target_dir()
    app_dir = f"{target_dir}/{app_folder}"
    hostname = node["hostname"]
    logger.info(f"Deploying {app_folder} on branch {git_branch} to node " +
                f"{hostname}")

    conn.run_command(hostname, f"pkill -u {conf.get_slice()}")

    # provision node
    conn.transfer_files(
        hostname,
        [
            io.get_abs_path("conf/log_files.yml"),
            io.get_abs_path("scripts/bootstrap_node.sh")
        ],
        "~"
    )
    conn.run_command(
        hostname,
        f"cd ~ && chmod +x bootstrap_node.sh && sh bootstrap_node.sh" +
        f" > ~/bootstrap.log"
    )
    logger.info(f"Node {hostname} provisioned")

    logger.info(f"Transferring app files to {hostname}")
    # transfer app files and set up app
    conn.transfer_files(
        hostname,
        [
            io.get_abs_path("hosts.txt"),
            io.get_abs_path(conf.get_bootstrap_script())
        ],
        target_dir
    )

    conn.run_command(hostname, f"cd {target_dir} && git clone {git_url}" +
                               f" && cd {app_folder} && git checkout " +
                               f"{git_branch} && git pull")
    conn.run_command(hostname, f"mv {target_dir}/bootstrap_app.sh {app_dir}")
    conn.run_command(hostname, f"cd {app_dir} && sh bootstrap_app.sh" +
                               f" > ~/bootstrap.log")

    logger.info(f"{app_folder} setup on {hostname}")

    # cleanup
    return conn.run_command(hostname, f"rm ~/bootstrap_node.sh")


def launch_using_thor(hostname, i, args):
    thor_dir = f"{conf.get_target_dir()}/thor"
    n = conf.get_number_of_nodes()
    f = conf.get_number_of_byzantine()
    p = conf.get_abs_path_to_app()
    e = conf.get_app_entrypoint()
    lp = f"{conf.get_target_dir()}/application.log"
    rs = conf.get_app_run_sleep()
    nss_flag = " -nss " if args.non_selfstab else " "
    cmd_string = (f"cd {thor_dir} && source ./env/bin/activate && " +
                  f"python thor.py -n {n} -f {f} -p {p} -e '{e}' " +
                  f"-i {i} -lp {lp} -rs {rs}{nss_flag}planetlab &")
    logging.info(f"Launching Thor with cmd: {cmd_string} on {hostname}")
    return conn.run_command(hostname, cmd_string)
