# -*- mode: python -*-

# Inherit the environment from my parent.
Import('env')
import os
import commands
# Make a copy of the environment, so my changes are limited in this directory and sub-directories.
env = env.Clone()
#############################################################################################################
env.Append(ACSUBST = {'BUILDDIR': env['relative_build_dir']})
env.Append(ACSUBST = {'TOP_BUILDDIR': env['builddir']})
env.Append(ACSUBST = {'TOP_SRCDIR': env['topdir']})
env.Append(ACSUBST = {'abs_top_srcdir': env['topdir']})

loggerconf = env['topdir'] + '/testdata/conf/log4cpp.conf'

env.Append(ACSUBST = {'DOTEST_LOGGER_CONF': loggerconf})

env.ac_substitute(target = [env['project_name'] + '/test/test.h'], 
                     source = [env['project_name'] + '/test/test.h.in'])

env.AppendENVPath('LD_LIBRARY_PATH',
                  Dir(env['LIB_DIR']).abspath + ':' + env['engine_common_library_dir'] +
                  ':' + env['mysql_library_dir'] + ':/lib64/:/usr/local/lib64:/usr/local/lib')

env.Append(CPPPATH = ['#'])
env.Append(CPPPATH = [env['engine_common_header_dir'],
                      '/usr/local/include/'])
env.Append(LIBPATH = ['/usr/local/lib/',
                      '/usr/local/lib64',
                      env['engine_common_library_dir'],
                      env['mysql_library_dir']])

# Test Library
if env['heap_check_type'] == 'tcmalloc':
    env.check_library_not_auto_add('tcmalloc')

#env.add_directory('tools')
env.add_directory(env['project_name'])

env.build_package(env['project_name'], [], strip = False)

###########################################################################################
#Add Additional share obj to ha2_package
'''
ret, expat = commands.getstatusoutput("ldd /usr/local/bin/AliWS |grep expat |awk -F\"=>\""
                                      "'{print $2}' |awk -F\"(\" '{print $1;}'"
                                      "|awk -F\" \" '{print $1;}'")
print "expat is %s" % expat

ret, enet = commands.getstatusoutput("file /usr/local/lib/libenet.so |awk -F\"\`\" '{print $2;}'"
                                     "|awk -F\"'\" '{print $1;}'")
enet = '/usr/local/lib/%s' % enet
print "enet is %s" % enet

# Make distribution
env['DIST_DIR'] = '#dist/';
env['DIST_INCLUDE_DIR'] = env['DIST_DIR'] + 'include/' + project_name

if env['mode'] == 'debug':
    dir_suffix = 'd'
else:
    dir_suffix = ''

env['DIST_LIB_DIR'] = env['DIST_DIR'] + 'lib' + env['target'] + dir_suffix
env['DIST_BIN_DIR'] = env['DIST_DIR'] + 'bin' + env['target'] + dir_suffix

dist_includes = []

dist_libs = []

dist_bins = []

for i in dist_includes:
    t = env.InstallAs(env['DIST_INCLUDE_DIR'] + i, 'include/apsara/' + i)
    env.Alias('dist', t)
    Env.Default(t)

for i in dist_libs:
    t = env.Install(env['DIST_LIB_DIR'], 'lib/' + i)
    env.Alias('dist', t)
    env.Default(t)

for i in dist_bins:
    t = env.Install(env['DIST_BIN_DIR'], 'bin/' + i)
    env.Alias('dist', t)
    env.Default(t)
'''
