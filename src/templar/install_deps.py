"""
this script will install all the required packages that you need on
ubuntu to compile and work with this package.
"""

import os
import os.path
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

import templar.version

# in what folder do we install tools?
tools = 'tools'
# do you want to debug this script?
opt_debug = False
# do you want to show progress?
opt_progress = True
# what ppas do you want to add?
opt_ppas = [
]
# what keys to download and trust via apt-key?
opt_keys_download = [
]
# keys to receive from keyservers
opt_keys_receive = [
]
# update apt
opt_update = False

#############
# functions #
#############
do_msg = False


def msg(s):
    if do_msg:
        print(s)


do_debug = False


def debug(s):
    if do_debug:
        print(s)


hide = True


def check_call_print(args):
    if hide:
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res_out, res_err = p.communicate()
        if p.returncode:
            print(res_out.decode(), file=sys.stderr)
            print(res_err.decode(), file=sys.stderr)
            sys.exit(p.returncode)
    else:
        subprocess.check_call(args)


all_keys = None


def keys_read():
    """
    the lines we are interested in look like this:
    pub   4096R/EFE21092 2012-05-11
    """
    global all_keys
    all_keys = set()
    output = subprocess.check_output([
        'apt-key',
        'list',
    ]).decode().strip()
    for line in output.split('\n'):
        if not line.startswith('pub'):
            continue
        parts = line.split()
        all_keys.add(parts[1].split('/')[1])


def keys_have(key_id):
    return key_id in all_keys


def get_codename():
    local_codename = subprocess.check_output([
        'lsb_release',
        '--codename',
        '--short',
    ]).decode().strip()
    if opt_debug:
        print('codename is [{0}]'.format(local_codename))
    return local_codename


NODE_FILE = 'package.json'


def install_node():
    # if the file is not there it is NOT an error
    if not os.path.isfile(NODE_FILE):
        return
    msg('installing from [{0}]...'.format(NODE_FILE))
    check_call_print([
        'npm',
        'install',
    ])

codename = None
altered_apt_configuration = False


def do_start():
    keys_read()
    global codename
    codename = get_codename()


def do_ppas():
    global altered_apt_configuration
    for ppa in opt_ppas:
        if opt_progress:
            print('processing ppa [{0}]...'.format(ppa))
        # cinelerra-ppa-ppa-trusty.list
        short_ppa = ppa[4:]
        parts = short_ppa.split('/')
        filename = '/etc/apt/sources.list.d/{0}-{1}-{2}.list'.format(parts[0], parts[1], codename)
        if opt_debug:
            print('filename is [{0}]'.format(filename))
        if os.path.isfile(filename):
            if opt_progress:
                print('already there in [{0}]...'.format(filename))
            continue
        altered_apt_configuration = True
        check_call_print([
            'sudo',
            'add-apt-repository',
            # '--enable-source', # source code too
            '--yes',  # don't ask questions
            ppa
        ])


def download_keys():
    global altered_apt_configuration
    for dl, key_id in opt_keys_download:
        if opt_progress:
            print('processing download key [{0}], [{1}]...'.format(dl, key_id))
        if keys_have(key_id):
            if opt_progress:
                print('already have this key')
                continue
        altered_apt_configuration = True
        if opt_progress:
            print('downloading key...')
        os.system('wget -q -O - {0} | sudo apt-key add -'.format(dl))
        keys_read()
        assert keys_have(key_id)


def receive_keys():
    global altered_apt_configuration
    for server, key_id in opt_keys_receive:
        if opt_progress:
            print('processing receive key [{0}], [{1}]...'.format(server, key_id))
        if keys_have(key_id):
            if opt_progress:
                print('already have this key')
            continue
        altered_apt_configuration = True
        if opt_progress:
            print('receiving key...')
        check_call_print([
            'sudo',
            'apt-key',
            'adv',
            '--keyserver',
            server,
            '--recv-keys',
            key_id,
        ])
        keys_read()
        assert keys_have(key_id)


def update_apt():
    if altered_apt_configuration and opt_update:
        if opt_progress:
            print('updating apt states...')
        check_call_print([
            'sudo',
            'apt-get',
            'update',
        ])
        # remove unneeded .save apt files
        os.system('sudo rm -f /etc/apt/sources.list.d/*.save /etc/apt/sources.list.save')


def install_packs(d):
    if 'packs' not in d:
        return
    msg('installing packages from deps.py...')
    debug(d.packs)
    args = [
        'sudo',
        'apt-get',
        'install',
        '--assume-yes',
        # TODO: remove this
        '--allow-unauthenticated',
    ]
    args.extend(d.packs)
    check_call_print(args)


def install_python_packs(d):
    for name, installer in [('requirements', 'pip'), ('requirements3', 'pip3')]:
        if name not in d:
            continue
        args = [
            installer,
            'install',
            '--user',
        ]
        args.extend(d[name])
        check_call_print(args)


def install_closure_old():
    jar_name = 'closure-compiler-v20161024'
    os.system(
        'wget -qO- https://dl.google.com/closure-compiler/compiler-latest.zip |'
        '(cd tools; bsdtar -xf- {jar_name}.jar)'.format(jar_name=jar_name))
    os.rename('tools/{jar_name}.jar'.format(jar_name=jar_name), 'tools/closure.jar')
    os.chmod('tools/closure.jar', 0o0775)


def install_closure():
    # some parameters
    url = "https://dl.google.com/closure-compiler/compiler-latest.zip"
    output = "tools/closure.jar"
    # create a temp file
    with tempfile.TemporaryFile(mode="wb") as temp_handle:
        # download the zip to the temp file
        response = urllib.request.urlopen(url)
        temp_handle.write(response.read())
        temp_handle.seek(0)
        # open the zip file
        with zipfile.ZipFile(temp_handle) as zip_file:
            jar_files = list(filter(lambda file_name: file_name.endswith('.jar'), zip_file.namelist()))
            assert len(jar_files) == 1
            jar_file = jar_files[0]
            # extract the jar file
            zip_file.extract(jar_file, output)


def install_jsmin():
    os.system(
        'wget -qO- https://raw.githubusercontent.com/douglascrockford/JSMin/master/jsmin.c |'
        '(cd tools; gcc -x c -O2 - -o jsmin)')


def install_jsl():
    os.system('cd tools; svn -q co https://javascriptlint.svn.sourceforge.net/svnroot/javascriptlint/trunk jsl')
    os.system('cd tools/jsl; python setup.py build > /dev/null')


def install_jsl_source():
    os.system('wget -qO- http://www.javascriptlint.com/download/jsl-0.3.0-src.tar.gz | (cd tools; tar zxf -)')
    os.system('cd tools; python setup.py build')


def install_css_validator():
    os.system('cd tools; git clone --depth 1 --branch master git@github.com:w3c/css-validator.git')
    os.system('cd tools/css-validator; ant')


def rm_tools():
    if os.path.isdir(tools):
        shutil.rmtree(tools)


tp = 'out/web/third_party'


def install_tp():
    if not os.path.isfile('templardefs/jschess.py'):
        return
    sys.path.append(os.getcwd())
    import templardefs.jschess
    if os.path.isdir(tp):
        shutil.rmtree(tp)
    os.makedirs(tp)

    for dep in templardefs.jschess.deps:
        print('getting javascript library [{0}]'.format(dep.name))
        if dep.downloadUrl:
            debug(dep.downloadUrl + ',' + dep.myFile)
            urllib.request.urlretrieve(dep.downloadUrl, filename=dep.myFile)
        if dep.downloadUrlDebug:
            debug(dep.downloadUrlDebug + ',' + dep.myFileDebug)
            urllib.request.urlretrieve(dep.downloadUrlDebug, filename=dep.myFileDebug)
        if dep.downloadCss:
            debug(dep.downloadCss + ',' + dep.css)
            urllib.request.urlretrieve(dep.downloadCss, filename=dep.css)
        if dep.closure:
            debug('doing closure')
            check_call_print([
                'tools/closure-compiler-v20160713.jar',
                dep.myFileDebug,
                '--js_output_file',
                dep.myFile,
            ])
        if dep.jsmin:
            debug('doing jsmin')
            subprocess.check_call([
                'tools/jsmin',
            ],
                stdout=open(dep.myFile, 'w'),
                stdin=open(dep.myFileDebug),
            )

    # chmod all files
    for f in os.listdir(tp):
        debug('considering [{0}]'.format(f))
        full = os.path.join(tp, f)
        if os.path.isfile(full):
            debug('chmodding [{0}]'.format(full))
            os.chmod(full, 0o0444)


tool_funcs = {
    'closure': install_closure,
    'jsmin': install_jsmin,
    'jsl': install_jsl,
    'jsl_source': install_jsl_source,
    'css-validator': install_css_validator,
}


def install_tools(d):
    if 'tools' not in d:
        return
    if len(d.tools) > 0:
        if not os.path.isdir(tools):
            os.mkdir(tools)
    for t in d.tools:
        print('installing tool [{0}]'.format(t))
        # noinspection PyUnresolvedReferences
        tool_funcs[t].__call__()


def check_version(d):
    if 'python_version_needed' not in d:
        return
    msg('checking python version from deps.py...')
    templar.version.check_version(d.python_version_needed)


def install_deps(d):
    install_node()
    install_packs(d)
    install_tools(d)
    install_python_packs(d)
    check_version(d)
    # TBD: get rid of this
    install_tp()
