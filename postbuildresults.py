import datetime
from mozautolog import RESTfulAutologTestGroup
import os
import re
import socket
import tailer


def find_latest_dir(directory):
    """Returns the most recently created directory in the given directory,
       as determined by the parsing the directory's name.
    """
    earliest = (None, None)
    for name in os.listdir(directory):
        filename = os.path.join(directory, name)
        if not os.path.islink(filename) and os.path.isdir(filename):
            try:
                filetime = datetime.datetime.strptime(name, '%Y-%m-%d_%H-%M-%S')
                if not earliest[0] or filetime > earliest[0]:
                    earliest = (filetime, filename)
            except ValueError:
                pass
    if earliest[1]:
        return earliest[1]

def submit_to_autolog(commit, logfile, error):
    print 'submitting to autolog'

    testgroup = RESTfulAutologTestGroup(
        testgroup = "Build",
        os = 'android',
        platform = 'emulator',
        harness = 'marionette',
        machine = socket.gethostname(),
        logfile=logfile)

    testgroup.set_primary_product(
        tree = 'b2g',
        buildtype = 'opt',
        revision = commit)

    testgroup.add_test_suite(
        testsuite = 'b2g emulator build',
        cmdline = '',
        passed = 1 if logfile is None else 0,
        failed = 0 if logfile is None else 1,
        todo = 0)

    if error:
        testgroup.add_test_failure(test='build', text=error, status='FAILURE')

    testgroup.submit()


if __name__ == "__main__":
    # locate the jenkins workspace dir in which this file is somewhere contained
    startdir = os.getcwd()
    while not startdir.endswith('workspace'):
        startdir = os.path.dirname(startdir)
        if len(startdir) < 2:
            raise Exception("workspace directory not found")

    # get the get revision number
    commit = open(os.path.join(startdir, 'git.revision'), 'r').read()
    print 'commit: ', commit

    # locate the log inside the newest build dir
    buildsdir = os.path.join(os.path.dirname(startdir), 'builds')
    builddir = find_latest_dir(buildsdir)
    log = os.path.join(builddir, 'log')

    # see if this log shows a success
    tail = tailer.tail(open(log), 50)
    logfile = None
    error = None
    if 'Finished: SUCCESS' not in ''.join(tail):
        # not successful, get more lines to write to output log
        tail = tailer.tail(open(log), 300)
        error = '\n'.join(tail[-3:])
        logfile = os.path.join(os.path.dirname(log), 'autolog_log')
        f = open(logfile, 'w')
        f.writelines(["%s\n" % x for x in tail])
        f.close()

    submit_to_autolog(commit, logfile, error)

