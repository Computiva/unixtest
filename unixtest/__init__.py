from argparse import ArgumentParser
import subprocess
import os

OUTPUT = 0
INPUT = 1


class TestCase(object):

    def __init__(self):
        self.tests = list()

    def add_test(self, command, name):
        if len(self.tests) > 0:
            self.tests[-1].finish()
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
        self.process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        self.command_in = self.process.stdin
        self.command_out = self.process.stdout
        self.name = name
        self.failures = list()
        self.io = OUTPUT
        self.expected_output = list()

    def _parts(self, line):
        part = str()
        for char in line:
            if char == "|":
                yield part
                self.io = OUTPUT if self.io == INPUT else INPUT
                part = str()
            else:
                part += char
        yield part

    def handle_line(self, line):
        for part in self._parts(line):
            if self.io == OUTPUT:
                self.expected_output.append(part)
            if self.io == INPUT:
                self.command_in.write(part)

    def finish(self):
        self.command_in.close()
        for expected_output in self.expected_output:
            output = self.command_out.read(len(expected_output))
            if output != expected_output:
                self.failures.append([expected_output, output])
        self.process.wait()


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
