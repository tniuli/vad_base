# -*- mode: python -*-

import re
import sys
import os
import os.path
import platform

SetOption('duplicate','hard-soft-copy')

# disable warning about 'two different environment specified for ...'
SetOption('warn', 'no-duplicate-environment')

# avoid scanning sources files for header dependency, when possible
SetOption('implicit_cache', 1)

# The root environment
# Place to store some options which will influence the compiler
env = Environment()
env['HOME'] = os.environ['HOME']
arch = platform.architecture()[0][:2]

env.Decider('MD5-timestamp')

env['project_name'] = 'vad_base'

def hard_link_func(dest, source, env):
    if os.access(dest, os.F_OK):
        os.unlink(dest)
    os.link(source, dest)
    return 0
#env['INSTALL'] = hard_link_func

customize_conf_file = 'build_conf.py'
tips_of_customize_conf_file = '''#!/bin/env python # -*- mode: python -*- #
###########################################################################
# You set all command line args for "scons" in this file, eg:             #
#                                                                         #
#  CXX = "distcc g++" #set c++ compiler to "distcc g++"                   #
#                                                                         #
# invoke "scons -h" to see all available args                             #
###########################################################################
def get_upper_path():
    import os
    path = os.getcwd()
    ls = path.split("/")
    n = len(ls)
    if n < 1:
        return None
    n = n -1
    path = '/'
    dirCount = n
    n = 1
    while n < dirCount :
        path = path + ls[n] + '/'
        n = n+1
    return path
root = get_upper_path()

engine_common_header_dir = '/home/w/include/'
engine_common_library_dir='/home/w/lib64/'

mysql_library_dir='/usr/lib64/mysql'
library_type = 'shared'
heap_check_type = 'none'
mode = 'debug'
'''

if not os.path.exists(customize_conf_file):
    outfile = open(customize_conf_file, 'w')
    outfile.write(tips_of_customize_conf_file)
    outfile.close()
env['user_conf'] = File(customize_conf_file)

# Variables
vars = Variables(customize_conf_file)

vars.Add('CC', 'set cc compiler', 'gcc')
vars.Add('CXX', 'set c++ compiler', 'g++')
vars.Add('CJGEN', 'set cjgen path', 'cjgen')


vars.Add(PathVariable('engine_common_library_dir', 
                      'path to common libraries installed',
                      '',
                      PathVariable.PathIsDir))

vars.Add(PathVariable('mysql_library_dir', 
                      'path to mysql library installed',
                      '',
                      PathVariable.PathIsDir))

vars.Add(PathVariable('engine_common_header_dir', 
                      'path to common header installed',
                      '',
                      PathVariable.PathIsDir))
'''
vars.Add(PathVariable('elog_library_dir', 
                      'path to elog library installed',
                      '',
                      PathVariable.PathIsDir))

vars.Add(PathVariable('elog_header_dir', 
                      'path to elog header installed',
                      '',
                      PathVariable.PathIsDir))

vars.Add(PathVariable('enet_library_dir', 
                      'path to enet library installed',
                      '',
                      PathVariable.PathIsDir))

vars.Add(PathVariable('enet_header_dir', 
                      'path to enet header installed',
                      '',
                      PathVariable.PathIsDir))

vars.Add(PathVariable('tr1_header_dir', 
                      'path to tr1 header files directory',
                      '.',
                      PathVariable.PathIsDir))

vars.Add(PathVariable('boost_header_dir', 
                      'path to boost header files directory',
                      '.',
                      PathVariable.PathIsDir))
'''
vars.Add(EnumVariable('mode', 'Set build mode', 'debug',
                      allowed_values=('debug', 'release')))

vars.Add(EnumVariable('target', 'Set target machine', arch,
                      allowed_values=('32', '64')))

vars.Add(EnumVariable('warn', 'Set -W option in compiler', 'all',
                      allowed_values=('all', 'default')));

vars.Add(BoolVariable(
            'coverage',
            'Switch to enable code coverage, e.g: coverage=true, MUST use along with mode=debug',
            'false'))

vars.Add(BoolVariable(
             'profile', 'Generate profile data for gconf, e.g: profile=true, MUST use along with mode=debug',
             'false'))

vars.Add(EnumVariable('library_type', 'specify which type of library should be build',
                      'shared', allowed_values=('static', 'shared', 'both')))

vars.Add(EnumVariable('heap_check_type', 'specify which type of heapcheck tools should be used',
                      'none',  allowed_values=('tcmalloc', 'none')))

vars.Add(EnumVariable('monitor', 'specify which type of monitor should be used', 'none',
                      allowed_values=('amon', 'none')))

vars.Add(BoolVariable('enable_strip',
                      'Enable strip operation in build_package(), e.g: enable_strip=true',
                      'false'))

vars.Update(env)
Help(vars.GenerateHelpText(env))

# Build flags
#   later used to define folder bins and libs will be stored
env.AppendUnique(CCFLAGS = '-fPIC')

if env['mode'] == 'debug':
    env.MergeFlags('-g')
else:
    # -fno-strict-aliasing is required, or Shennong unit test will fail
    env.MergeFlags('-g -O2')

if env['coverage']:
    env.AppendUnique(CCFLAGS = '-fprofile-arcs')
    env.AppendUnique(CCFLAGS = '-ftest-coverage')
    env.AppendUnique(LINKFLAGS = '-fprofile-arcs')
    env.AppendUnique(LINKFLAGS = '-ftest-coverage')

if env['profile']:
    env.AppendUnique(CCFLAGS = '-pg')
    env.AppendUnique(LINKFLAGS = '-pg')

if env['warn'] == 'all':
    env.MergeFlags('-Wall')

if env['monitor'] == 'amon':
   env.MergeFlags('-DAMON')
   env.Append(LIBS = 'amon')

# Directories
#   Define these variables
env['BUILD_MODE'] = env['mode'] + env['target']
env['relative_build_dir'] = 'build/' + env['BUILD_MODE']
env['BUILD_DIR'] = '#'+ env['relative_build_dir']
env['PACKAGES_DIR'] = env['BUILD_DIR'] + '/packages'
env['PACKAGES_STAGING_DIR'] = env['PACKAGES_DIR'] + '/staging'
env['BIN_DIR'] = env['BUILD_DIR'] + '/bin'
env['UNITTEST_DIR'] = env['BUILD_DIR'] + '/unittest'
env['LIB_DIR'] = env['BUILD_DIR'] + '/lib'
env['PYEXT_DIR'] = env['BUILD_DIR'] + '/pyext'
env.Append(LIBPATH = env['LIB_DIR'])

env['topdir'] = env.Dir('#').abspath
env['builddir'] = env['topdir'] + '/' + env['BUILD_DIR'][1:]

env['sdk_name'] = env['project_name'] + '_sdk'
env['sdk_version'] = '0.1.0'
env['sdk_full_name'] = '%s-%s-%s' % (env['sdk_name'], env['sdk_version'], env['mode'] + env['target'])
env['sdk_release'] = 1
env['SDK_BUILD_DIR'] = env['builddir'] + '/sdk/' + env['sdk_full_name']
env['SDK_BUILD_DIR_INCLUDE'] = env['SDK_BUILD_DIR'] + '/include'
env['SDK_BUILD_DIR_LIB'] = env['SDK_BUILD_DIR'] + '/lib'
env['SDK_BUILD_DIR_VAD_BASE'] = env['SDK_BUILD_DIR'] + '/vad_base'

##############################################################################################
# common compiler flags
### Macros used to write 64-bit constant compatibly for both 32-bit and 64-bit
### compiler (__UINT64_C and __INT64_C) will only be available if this macro
### is defined, in addition to #include <stdint.h>
#env.MergeFlags('-D__STDC_LIMIT_MACROS')

# fix Glob bug
# Glob use the file list returned by OS as is. So when the directory has a new
# file, the *order* of file list changes, and trigger an unnecessary rebuild.
# Fix this problem by sorting the list by file names.
def glob(self, *args, **kwargs):
    files = self.Glob_(*args, **kwargs)
    files.sort(lambda x,y:cmp(str(x), str(y)))
    return files
env.__class__.Glob_ = env.__class__.Glob
env.__class__.Glob = glob
del glob

def append(self, *args, **kwargs):
    if 'CPPPATH' in kwargs:
       list = kwargs['CPPPATH']
       if (type(list) == type('')):
          list = [list]
       for path in list:
           if len(path) > 0 and (path[0] == '#'):
              self.Append_(CPPPATH=[self['BUILD_DIR'] + '/' +path[1:]])
    self.Append_(*args, **kwargs)

env.__class__.Append_ = env.__class__.Append
env.__class__.Append = append
del append

# The following code is to create the directory from . to env['BUILD_DIR']
# This is because a bug in scons: #16926

def copy_dir(s, d):
    if (not os.path.isdir(s)):
        return

    if (not os.path.isdir(d)):
        os.mkdir(d)

    sub = os.listdir(s)
    for e in sub:
        if (not e.startswith('.') and e != 'build' and e != 'package'):
            copy_dir(os.path.join(s,e), os.path.join(d,e))
env.AddMethod(copy_dir)

if (not os.path.isdir('build')):
    print 'mkdir', 'build'
    os.mkdir('build')

if (not os.path.isdir(env['BUILD_DIR'][1:])):
    print 'mkdir', env['BUILD_DIR'][1:]
    os.mkdir(env['BUILD_DIR'][1:])

copy_dir('.', env['BUILD_DIR'][1:])
# end of bug-fix for 16926

# Custom builders
### read SConscript in the given sub-folders, exports define what
### variables are to exported to that SConscript
def add_directory(self, *dirs):
    return self.SConscript(dirs=Flatten(dirs), exports={'env':self})
env.AddMethod(add_directory)

def install(self, *args, **kwargs):
    t = self.Install(*args, **kwargs)
    self.Default(t)
    return t
env.AddMethod(install)

env.Append(BUILDERS = {'strip_builder' : Builder(action= "/usr/bin/strip -o $TARGET $SOURCE") })

def stripped_install(self, target, source):
    source = self.File(self.Flatten([source]))
    targetDir = self.Dir(target)
    r = []
    for s in source:
        t = self.strip_builder(target = str(targetDir) + '/' + s.name, source = s);
        r = r + t;
    return self.Flatten(r)
env.AddMethod(stripped_install)

env.Append(BUILDERS = {'aTar' : Builder(action= "/bin/tar -f ${TARGET} $TARFLAGS .", multi = 1) })

def build_package(self, name, source, strip=False, subdir="",  *args, **kwargs):
    package_name = '%s/%s_%s.tar.gz' % (self['PACKAGES_DIR'], name, self['BUILD_MODE'])
    package_staging = self['PACKAGES_STAGING_DIR'] + '/' + name
    staging_files = []
    if strip:
        staging_files = self.stripped_install(package_staging + "/" + subdir, source)
    else:
        staging_files = self.Install(package_staging+"/" + subdir, source)
    package_staging = self.Dir(package_staging)
    for file in staging_files:
        self.AppendUnique(TARFLAGS='-z')
        self.AppendUnique(TARFLAGS='-c')
        self.AppendUnique(TARFLAGS='-C' + package_staging.path)
        self.Depends(package_name, file)
        self.aTar(package_name, file)
    self.Alias('package', package_name)
env.AddMethod(build_package)

### Build a static library and copy the lib binary to LIB_DIR
def build_static_library(self, set_default='yes', *args, **kwargs):
    target = self.StaticLibrary(*args, **kwargs)
    target = self.Install(self['LIB_DIR'], target)
    if set_default == 'yes':
        self.Alias('dev', target)
        self.Default(target)
    return target
env.AddMethod(build_static_library)

### Build a dynamic library and copy the lib binary to LIB_DIR
def build_shared_library(self, set_default='yes', package = None, *args, **kwargs):
    target = self.SharedLibrary(*args, **kwargs)
    target = self.Install(self['LIB_DIR'], target)
    for t in target:
        t.attributes.shared = True;
    if package != None:
        if 'source' in kwargs:
            del kwargs['source']
        if self['enable_strip']:
            self.build_package(package, target, strip=True, *args, **kwargs)
        else:
            self.build_package(package, target, strip=False, *args, **kwargs)
    if set_default == 'yes':
        self.Alias('dev', target)
        self.Default(target)
    return target
env.AddMethod(build_shared_library)

def get_upper_path(self, *args):
    path = args[0]
    print 'get_upper_path , path is ', path
    ls = path.split("/")
    n = len(ls)
    if n < 1:
        return None
    n = n -1
    path = '/'
    dirCount = n
    n = 1
    while n < dirCount :
        path = path + ls[n] + '/'
        n = n+1
    return path
env.AddMethod(get_upper_path)

def build_library(self, *args, **kwargs):
    extend_environment(self, *args, **kwargs)
    self = self.Clone();
    
    ret = []
    if env['library_type'] == 'static' or env['library_type'] == 'both':
        ret.append(build_static_library(self, *args, **kwargs))
    if env['library_type'] == 'shared' or env['library_type'] == 'both':
        ret.append(build_shared_library(self, *args, **kwargs))
    return ret
env.AddMethod(build_library)
'''
def build_sdk_library(self, *args, **kwargs):
    self = self.Clone();
    target = []
    if env['library_type'] == 'static':
        target.append(build_static_library(self, set_default='no', *args, **kwargs))
    if env['library_type'] == 'shared':
        target.append(build_shared_library(self, set_default='no', *args, **kwargs))
    self.Alias('sdk', target)
    return target
env.AddMethod(build_sdk_library)
'''

def extend_environment(self, *args, **kwargs):
    if 'LIBS' in kwargs:
        if type(kwargs['LIBS']) != type([]):
            kwargs['LIBS'] = (' '.join(Flatten(kwargs['LIBS']))).split(' ')
    else:
        kwargs['LIBS'] = []
    kwargs['LIBS'].extend(self['LIBS'])

def build_program(self, package = None,  *args, **kwargs):
    extend_environment(self, *args, **kwargs)
    target = self.Program(*args, **kwargs)
    target = self.Install(self['BIN_DIR'], target)
    print "package:", package
    if package != None:
        if 'source' in kwargs:
            del kwargs['source']
        if self['enable_strip']:
            self.build_package(package, target, strip=True, *args, **kwargs)
        else:
            self.build_package(package, target, strip=False, *args, **kwargs)
    self.Alias('dev', target)
    self.Default(target)
    return target
env.AddMethod(build_program)

### do unit test ###
def run_unittest_(target, source, env):
    cmd = '/bin/env'
    lib_path = '/usr/lib' + arch 	    
    env.AppendENVPath('LD_LIBRARY_PATH', '/lib64/' + ':' +'/usr/local/lib' + ':' + lib_path)
    if env['heap_check_type'] == 'tcmalloc' and not re.search("_perftest$", source[0].abspath):
        env.AppendENVPath('LD_PRELOAD', '/usr/local/lib/libtcmalloc.so')
        env.AppendENVPath('HEAPCHECK', 'normal')
    for item in env['ENV'].items():
        cmd += (' %s=%s' % item)
    cmd += ' %s' 
    for p in source:
        dirname = os.path.dirname(p.abspath)
        print "ATest: Entering directory `%s'" % dirname
        print cmd % p.abspath + ' --gtest_output=./gtest-output'
        
        ret = os.system(cmd % p.abspath + ' --gtest_output=xml:gtest-output/')
        #print "ATest: Leaving directory `%s'" % dirname
        if ret: 
            return ret
    return 0
    
env.Append(BUILDERS = {'run_unittest_builder' : Builder(action= run_unittest_) })

def build_unittest(self, *args, **kwargs):
    extend_environment(self, *args, **kwargs)
    target = self.Program(*args, **kwargs)
    for p in target:
        self.Alias('test', p)
        check = self.run_unittest_builder(str(p) + '_dummy', source = p)
        self.Alias('check', check)
        Requires(check, 'ac')
    return target
### do unit test ###
env.AddMethod(build_unittest)

def build_cangjie(self, dst, src):
    self.Depends(dst, env['CJGEN'])
    self.cangjie_(dst, src)

env.AddMethod(build_cangjie)

### Build Cangjie definition file ###
env.Append(BUILDERS = {'cangjie_builder' : Builder(action=env['CJGEN'] + ' $SOURCE $TARGET') })

### Just copy (link) files into build files.
### It must be used with duplicate=1
env.Append(BUILDERS = {'do_nothing_builder' : Builder(action='') })
def duplicate(self, *args):
    for f in args:
        self.Default(self.do_nothing_builder(f+'_copy', f))
env.AddMethod(duplicate)

def duplicate_and_bin(self, *args):
    for f in args:
        self.Default(self.do_nothing_builder(f+'_copy', f))
        t = self.Install(self['BIN_DIR'], f)
        self.Default(t)
        self.Alias('dev', t)
env.AddMethod(duplicate_and_bin)

def check_library_with_header(self, lib, header, **kwargs):
    conf = Configure(self)
    if not conf.CheckLibWithHeader(lib, header, 'CXX', **kwargs):
        Exit(-1)
    env = conf.Finish()
env.AddMethod(check_library_with_header)

def check_library(self, *args, **kwargs):
    conf = Configure(self)
    for f in args:
        if not conf.CheckLib(f, **kwargs):
            Exit(-1)
    env = conf.Finish()
env.AddMethod(check_library)

def check_library_not_auto_add(self, *args):
    conf = Configure(self)
    for f in args:
        if not conf.CheckLib(f, symbol = "main", header = None, language = None, autoadd = 0):
            Exit(-1)
    env = conf.Finish()
env.AddMethod(check_library_not_auto_add)

def check_header(self, *args):
    conf = Configure(self)
    for f in args:
        if not conf.CheckCXXHeader(f):
            Exit(-1)
    env = conf.Finish()
env.AddMethod(check_header)
        
def get_library_name(self, name):
    libname = self['LIBPREFIX'] + name
    if self['library_type'] == 'static':
        libname = libname + self['LIBSUFFIX']
    else:
        libname = libname + self['SHLIBSUFFIX']
    return env['LIB_DIR'] + '/' + libname
env.AddMethod(get_library_name)

def get_library_path(self, *names):
    return map(lambda x : self.do_get_library_name(x), *names)
env.AddMethod(get_library_path)

def ac_substitute_(target, source, env):
    if source == [] or target == []:
        return 1

    acsustdict = {}
    if 'ACSUBST' in env:
        if type(env['ACSUBST'] ) == type({}):
            acsustdict = env['ACSUBST']
    srcfile = open(source[0].path, 'r')
    destfile = open(target[0].path, 'w')
    for line in srcfile.readlines():
        for key, value in acsustdict.items():
            line = re.sub( '@' + key + '@', value, line)
        destfile.write(line)
    srcfile.close()
    destfile.close()
    return 0
env.Append(BUILDERS = {'ac_substitute_builder' : Builder(action = ac_substitute_) })    

def ac_substitute(self, *args, **kwargs):
    target = self.ac_substitute_builder(*args, **kwargs)
    self.Default(target)
    self.Alias('ac', target)
    return target
env.AddMethod(ac_substitute)

def generate_error_info_(target, source, env):
    origin_file = source[0].path
    cpp_file = target[0].path
    header_file = cpp_file.replace(".cpp", ".h");
    ERRORINFO_START_FLAG = "%{\n"
    ERRORINFO_END_FLAG = "}%\n"
    FILE_SEPERATOR = "%file_seperator%\n"

    f = open(origin_file, 'r');
    fh = open(header_file, 'w');
    fcpp = open(cpp_file, 'w');
    cppContent = ""
    hContent = ""
    isErrorCode = False
    isCppContent = False
    cppCode = ""
    try:
        for line in f:
            if line == ERRORINFO_START_FLAG:
                isErrorCode = True
                continue
            elif line == ERRORINFO_END_FLAG:
                isErrorCode = False
                continue
            elif line == FILE_SEPERATOR:
                isCppContent = True
                continue
            if (isErrorCode) :
                list = line.split("\t")
                size = len(list)
                if (size < 2) :
                    print "ERROR at ", line
                    return False
                errorDefine = list[0]
                errorCode = list[1]
                if (size >= 3) :
                    errorMsg = list[2].rstrip("\n")
                    if errorMsg == "" :
                        errorMsg = '"' + errorDefine + '"'                        
                else:
                    errorMsg = '"' + errorDefine + '"'
                    
                hCode = "const ErrorCode " + errorDefine + " = " + errorCode + ";\n"
                hContent += hCode;
                cppCode += "    gCode2MsgMap[" +  errorDefine + "] = " + errorMsg + ";\n"
            elif isCppContent:
                cppContent += line
            else:
                hContent += line
    
        cppContent = cppContent % {'ERRORINFO': cppCode}
        fh.write(hContent)
        fcpp.write(cppContent)

    finally:
        f.close()
        fh.close()
        fcpp.close()
    return 0

env.Append(BUILDERS = {'generate_error_info_builder' : Builder(action = generate_error_info_) })

def generate_error_info(self, target, source, *args, **kwargs):
    extend_environment(self, *args, **kwargs)
    cpp_file = target
    origin_file = source
    header_file = cpp_file.replace(".cpp", ".h");
    t = self.generate_error_info_builder(target = cpp_file, source = origin_file, *args, **kwargs)
    env.SideEffect(header_file, t);
    return t;
env.AddMethod(generate_error_info)


env.SConscript(
    dirs = '.',
    exports = 'env',
    variant_dir = env['BUILD_DIR'],
    duplicate = 1
    )

