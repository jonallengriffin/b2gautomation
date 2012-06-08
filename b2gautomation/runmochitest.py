# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
from logparser import LogParser
from mozautolog import RESTfulAutologTestGroup as AutologTestGroup
from mozprocess.processhandler import ProcessHandler
from optparse import OptionParser
import os
import socket
import sys
import uuid

def post_to_autolog(data, testChunk, revision=None, logfile=None):
    testgroup = AutologTestGroup(machine=socket.gethostname(),
                                 id=data['id'],
                                 platform='emulator',
                                 os='android',
                                 harness='buildbot',
                                 testgroup='mochitests-%s' % testChunk,
                                 logfile=logfile,
                                )

    testgroup.set_primary_product(tree='b2g',
                                  revision=revision,
                                  buildtype='opt',
                                 )

    testgroup.add_test_suite(testsuite='mochitest',
                             passed=data.get('passed', 0),
                             failed=data.get('failed', 0),
                             todo=data.get('todo', 0),
                             id="%s-testsuite1" % data['id'],
                            )

    for tf_index, failure in enumerate(data.get('failures', [])):
        for f in failure.get('failures', []):
            testgroup.add_test_failure(test=failure.get('test', None),
                                       id="%s-testfailure1.%d" % (data['id'], (tf_index+1)),
                                       duration=failure.get('duration', None),
                                       **f
                                      )

    testgroup.submit()


def main():
    parser = OptionParser()
    parser.add_option('--logfile', dest='logfile', action='store',
                      default='mochitest.log',
                      help='path to log file')
    parser.add_option('--revision', dest='commit', action='store',
                      help='repo revision')
    parser.add_option('--python-path', dest='pythonPath', action='store',
                      help='path to python, for use with a virtualenv')
    parser.add_option('--runtests-path', dest='runtestsPath', action='store',
                      help='path to runtestsb2g.py')
    parser.add_option('--autolog', dest='autolog', action='store_true',
                      help='post results to autolog')
    parser.add_option('--emulator', dest='emulator', action='store',
                      help='the architecture of the emulator to use, arm or x86')
    parser.add_option('--b2g-path', dest='b2gPath', action='store',
                      help='the path to the B2G repo, used for emulator tests')
    parser.add_option('--total-chunks', dest='totalChunks', action='store',
                      help='the number of total test chunks')
    parser.add_option('--this-chunk', dest='thisChunk', action='store',
                      help='the number of this test chunk to run')
    parser.add_option('--run-only-tests', dest='runOnlyTests', action='store',
                      help='path to manifest containing tests to run')
    parser.add_option('--exclude-tests', dest='excludeTests', action='store',
                      help='path to manifest containing tests to exclude')
    parser.add_option('--adb-path', dest='adbPath', action='store',
                      default='adb',
                      help='the path to adb, if not on your path')
    parser.add_option('--xre-path', dest='xrePath', action='store',
                      help='the path to xpcshell')
    parser.add_option('--no-window', dest='noWindow', action='store_true',
                      help="don't show the emulator window")

    options, args = parser.parse_args()

    options.logfile = os.path.abspath(options.logfile)

    if not options.pythonPath:
        options.pythonPath = sys.executable
    options.pythonPath = os.path.abspath(options.pythonPath)

    if options.autolog and not options.commit:
        raise Exception('must specify --revision if --autolog is used')

    # handle emulator-specific options
    if options.b2gPath:

        if not options.emulator:
            # figure out what kind of emulator we're using
            productDir = os.path.join(options.b2gPath, "out", "target", "product")
            if os.access(os.path.join(productDir, "generic"), os.F_OK):
                print 'using arm emulator'
                options.emulator = 'arm'
            elif os.access(os.path.join(productDir, "generic_x86"), os.F_OK):
                print 'using x86 emulator'
                options.emulator = 'x86'
            else:
                raise Exception("Unable to determine emulator architecture; "
                                "please specify the --emulator [arm|x86] argument")

        # if there is an adb in the B2G path, use it
        testAdbPath = os.path.join(options.b2gPath, "out", "host", "linux-x86", "bin", "adb")
        if os.access(testAdbPath, os.F_OK) and options.adbPath == 'adb':
            options.adbPath = testAdbPath

    if os.access(options.logfile, os.F_OK):
        os.remove(options.logfile)

    # build the command-line for runtestsb2g.py
    cmd = [options.pythonPath, options.runtestsPath,
           '--adbpath', options.adbPath,
           '--console-level', 'INFO']

    if options.runOnlyTests:
        cmd.extend([
           '--run-only-tests', options.runOnlyTests])

    if options.excludeTests:
        cmd.extend([
           '--exclude-tests', options.excludeTests])

    if options.emulator:
        cmd.extend([
           '--emulator', options.emulator, '--b2gpath', options.b2gPath,
           '--remote-webserver', '10.0.2.2'])
    else:
        cmd.extend([
           '--marionette', 'localhost:2828'])

    if options.thisChunk and options.totalChunks:
        cmd.extend([
           '--total-chunks', options.totalChunks, '--this-chunk', options.thisChunk])

    if options.xrePath:
        cmd.extend([
           '--xre-path', options.xrePath])

    if options.noWindow:
        cmd.extend([
           '--no-window'])

    print cmd

    # call runtestsb2g.py
    process = ProcessHandler(cmd, logfile=options.logfile, storeOutput=False,
                             cwd=os.path.dirname(options.runtestsPath))
    exit_code = process.waitForFinish()
    print 'exit_code', exit_code

    if exit_code:
        return exit_code

    # parse the mochitest logfile, which will give us a nice dict of results
    parser = LogParser([options.logfile], harnessType='mochitest')
    results = parser.parseFiles()
    results['id'] = str(uuid.uuid1())
    print json.dumps(results, indent=2)

    # post the results to autolog
    if options.autolog:
        assert(options.thisChunk)
        post_to_autolog(results,
                        options.thisChunk,
                        logfile=options.logfile,
                        revision=options.commit)

if __name__ == "__main__":
    main()

