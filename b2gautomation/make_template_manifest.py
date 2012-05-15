from git import *
from optparse import OptionParser
import os
from xml.dom.minidom import parse


def make_template_manifest(repo_path, input_manifest, output_manifest):
    if not input_manifest:
        input_manifest = os.path.join(repo_path, ".repo", "manifests", "default.xml")
    dom = parse(input_manifest)
    projects = dom.getElementsByTagName('project')
    for project in projects:
        path = os.path.join(repo_path, project.getAttribute('path'))
        repo = Repo(path)
        commit = repo.head.commit.hexsha
        project.setAttribute('revision', commit)
    out = open(output_manifest, 'w')
    dom.writexml(out)


if __name__ == "__main__":
    parser = OptionParser(usage='%prog [options] /path/to/B2G/repo')
    parser.add_option('--repo', dest='repo_path', action='store',
                      help='directory of the B2G repo')
    parser.add_option('--source', dest='input_manifest', action='store',
                      help='source manifest')
    parser.add_option('--dest', dest='output_manifest', action='store',
                      default='default.xml',
                      help='location to write template manifest')

    options, args = parser.parse_args()
    if not args:
        parser.print_usage()
        parser.exit()

    make_template_manifest(args[0],
                           options.input_manifest,
                           options.output_manifest)

