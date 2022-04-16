import os
import time
from termcolor import colored
from setup import parse_arguments
from handler import parameters_handler


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
    print(colored("\t\tmany thanks to ~<|", 'yellow') + colored("\x1b[6;30;42m calfcrusher \x1b[0m", 'red') + colored("|>~ ", 'yellow'))
    print('\n')
    time.sleep(2)
    arguments = parse_arguments()
    try:
        parameters_handler(
            exploit=arguments.exploit,
            payload=arguments.payload,
            lport=arguments.local_port,
            rport=arguments.remote_port,
            lhost=arguments.local_host,
            output=arguments.payload_outfile,
            onion_ftp=arguments.onion_ftp
        )
    except Exception as e:
        print('\n')
        print(colored('\t\v! Error occur !', 'red'))
        print(colored(str(e.with_traceback(e.__traceback__)), 'yellow'))
        exit(0)


if __name__ == '__main__':
    os.system('cls') if os.name == 'nt' else os.system('clear')
    stemploit_main()
