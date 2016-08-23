
def install_jsl():
    print('installing tool [{0}]'.format('jsl'))
    if not os.path.isdir(tools):
        os.mkdir(tools)
    #os.system('wget -qO- http://www.javascriptlint.com/download/jsl-0.3.0-src.tar.gz | (cd tools; tar zxf -)')
    #os.system('cd tools; python setup.py build')
    os.system('cd tools; svn -q co https://javascriptlint.svn.sourceforge.net/svnroot/javascriptlint/trunk jsl')
    os.system('cd tools/jsl; python setup.py build > /dev/null')

def install_closure():
    print('installing tool [{0}]'.format('closure'))
    if not os.path.isdir(tools):
        os.mkdir(tools)
    #jar_name='compiler.jar'
    jar_name='closure-compiler-v20160713'
    os.system('wget -qO- https://dl.google.com/closure-compiler/compiler-latest.zip | (cd tools; bsdtar -xf- {jar_name}.jar)'.format(jar_name=jar_name))
    os.chmod('tools/{jar_name}.jar'.format(jar_name=jar_name), 0o0775)

def install_closure():
    print('installing tool [{0}]'.format('closure'))
    if not os.path.isdir(tools):
        os.mkdir(tools)
    #jar_name='compiler.jar'
    jar_name='closure-compiler-v20160713'
    os.system('wget -qO- https://dl.google.com/closure-compiler/compiler-latest.zip | (cd tools; bsdtar -xf- {jar_name}.jar)'.format(jar_name=jar_name))
    os.chmod('tools/{jar_name}.jar'.format(jar_name=jar_name), 0o0775)

def install_jsmin():
    print('installing tool [{0}]'.format('jsmin'))
    if not os.path.isdir(tools):
        os.mkdir(tools)
    os.system('wget -qO- https://raw.githubusercontent.com/douglascrockford/JSMin/master/jsmin.c | (cd tools; gcc -x c -O2 - -o jsmin)')

def install_jsl():
    print('installing tool [{0}]'.format('jsl'))
    if not os.path.isdir(tools):
        os.mkdir(tools)
    #os.system('wget -qO- http://www.javascriptlint.com/download/jsl-0.3.0-src.tar.gz | (cd tools; tar zxf -)')
    #os.system('cd tools; python setup.py build')
    os.system('cd tools; svn -q co https://javascriptlint.svn.sourceforge.net/svnroot/javascriptlint/trunk jsl')
    os.system('cd tools/jsl; python setup.py build > /dev/null')
