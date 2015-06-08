from argparse import ArgumentParser
import os


class TestCase(object):

    def __init__(self):
        self.tests = list()

    def add_test(self, command, name):
        self.tests.append(Test(command, name))

    def finish(self):
        failures = list()
        for test in self.tests:
            failures.extend(test.failures)
        if len(failures) == 0:
            print "\033[32m%s\033[m" % test.name
        else:
            print "\033[31m%s\033[m" % test.name
            for expected, got in failures:
                print "    Expected:"
                print "        %s" % expected
                print "    Got:"
                print "        %s" % got


class Test(object):

    def __init__(self, command, name):
        self.command = os.popen(command)
        self.name = name
        self.failures = list()

    def handle_line(self, line):
        output = self.command.read(len(line))
        if line != output:
            self.failures.append([line, output])


def test_file(path):
    test_case = TestCase()
    for line in open(path).readlines():
        if line.startswith("$ "):
            test_case.add_test(line[2:], path)
        else:
            test_case.tests[-1].handle_line(line)
    test_case.finish()

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
