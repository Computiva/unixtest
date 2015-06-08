from argparse import ArgumentParser
import os

def test_file(path):
    for line in open(path).readlines():
        if line.startswith("$ "):
            command = os.popen(line[2:])
        else:
            output = command.read(len(line))
            if line == output:
                print "\033[32m%s\033[m" % path
            else:
                print "\033[31m%s\033[m" % path
                print "    Expected:"
                print "        %s" % line
                print "    Got:"
                print "        %s" % output

def test_dir(path):
    for child in os.listdir(path):
        child_path = os.path.join(path, child)
        if os.path.isfile(child_path):
            test_file(child_path)

def main():
    arguments_parser = ArgumentParser(description="Test programs that handle text streams.")
    arguments_parser.add_argument("path", help="path to directory")
    arguments = arguments_parser.parse_args()
    path = vars(arguments)["path"]
    test_dir(path)
