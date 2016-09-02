#!/usr/bin/python3

'''
this script will install all the required packages that you need on
ubuntu to compile and work with this package.

It will:
    - add repositories
    - download signing keys
    - receive keys from the keyserver
    - install packages

TODO:
- only install packages if they are not already installed.
- install this too: https://www.dropbox.com/download?dl=packages/ubuntu/dropbox_1.6.2_amd64.deb
    (dropbox do not have a ppa or package in the ubuntu archives).
- consider using the python-apt python module to do most of the hard work in this script.
'''

import subprocess # for check_output, Popen, PIPE
import os # for system
import os.path # for isfile
import sys # for exit

##############
# parameters #
##############
# do you want to do ppas?
do_ppa=False
# do you want to do keys?
do_keys=False
# do you want to receive keys?
do_recv_keys=False
# do you want to be silent when installing packages?
opt_silent=True
# do you want to check the result from subprocess? 
opt_check=True
# do you want to debug this script?
opt_debug=False
# do you want to show progress?
opt_progress=True
# what ppas do you want to add?

# the lines we are interested in look like this:
# pub   4096R/EFE21092 2012-05-11
def keys_read():
    output=subprocess.check_output([
        'apt-key',
        'list',
    ]).decode().strip()
    for line in output.split('\n'):
        if not line.startswith('pub'):
            continue
        parts=line.split()
        all_keys.add(parts[1].split('/')[1])

def keys_have(key_id):
    return key_id in all_keys

def subprocess_wrap(args, silent=opt_silent, check=opt_check):
    if silent:
        if check:
            subprocess.check_call(
                args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            subprocess.call(
                args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
    else:
        if check:
            subprocess.check_call(args)
        else:
            subprocess.call(args)

########
# code #
########
keys_read()
altered_apt_configuration=False
codename=subprocess.check_output([
    'lsb_release',
    '--codename',
    '--short',
    ]).decode().strip()
if opt_debug:
    print('codename is [{0}]'.format(codename))

# repositories

if do_ppa:
    for ppa in opt_ppas:
        if opt_progress:
            print('processing ppa [{0}]...'.format(ppa))
        # cinelerra-ppa-ppa-trusty.list
        short_ppa=ppa[4:]
        parts=short_ppa.split('/')
        #filename='/etc/apt/sources.list.d/{0}-{1}-{2}.list'.format(parts[0], parts[1], codename)
        filename='/etc/apt/sources.list.d/{0}.list'.format(parts[0])
        if opt_debug:
            print('filename is [{0}]'.format(filename))
        if os.path.isfile(filename):
            if opt_progress:
                print('already there in [{0}]...'.format(filename))
            continue
        altered_apt_configuration=True
        subprocess_wrap([
            'sudo',
            'add-apt-repository',
            '--enable-source', # source code too
            '--yes', # dont ask questions
            ppa
        ])

# downloaded keys

if do_keys:
    for dl, key_id in opt_keys_download:
        if opt_progress:
            print('processing download key [{0}], [{1}]...'.format(dl, key_id))
        if keys_have(key_id):
            if opt_progress:
                print('already have this key')
            continue
        altered_apt_configuration=True
        if opt_progress:
            print('downloading key...')
        os.system('wget -q -O - {0} | sudo apt-key add -'.format(dl))
        keys_read()
        assert keys_have(key_id)

# received keys

if do_recv_keys:
    for srvr, key_id in opt_keys_receive:
        if opt_progress:
            print('processing receive key [{0}], [{1}]...'.format(srvr, key_id))
        if keys_have(key_id):
            if opt_progress:
                print('already have this key')
            continue
        altered_apt_configuration=True
        if opt_progress:
            print('receiving key...')
        subprocess_wrap([
            'sudo',
            'apt-key',
            'adv',
            '--keyserver',
            srvr,
            '--recv-keys',
            key_id,
        ])
        keys_read()
        assert keys_have(key_id)

# update apt state

if altered_apt_configuration:
    if opt_progress:
        print('updating apt states...')
    subprocess_wrap([
        'sudo',
        'apt-get',
        'update',
    ])
    # remove unneeded .save apt files
    os.system('sudo rm -f /etc/apt/sources.list.d/*.save /etc/apt/sources.list.save')

# install packages

if opt_progress:
    print('installing packages...')
args=[
    'sudo',
    'apt-get',
    'install',
    '--assume-yes'
]
args.extend(opt_packs)
subprocess_wrap(args, silent=False)
