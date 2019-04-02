import datetime, os, signal, subprocess, sys, time, unittest

def run(command, stdin = None, timeout = 30):
    """
    Runs the specified command using specified standard input (if any) and
    returns the output on success. If the command doesn't return within the
    specified time (in seconds), "__TIMEOUT__" is returned.
    """

    start = datetime.datetime.now()
    l = command.split()
    l = [" ".join(v.split("|")) if "|" in v else v for v in l]
    process = subprocess.Popen(l,
                               stdin = subprocess.PIPE, 
                               stdout = subprocess.PIPE,
                               stderr = subprocess.STDOUT)
    if not stdin is None:
        process.stdin.write(bytes(stdin, 'utf-8'))
    process.stdin.close()
    while process.poll() is None:
        time.sleep(0.1)
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:
            os.kill(process.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            return "__TIMEOUT__"
    result = process.stdout.read().decode("utf-8")
    process.stdout.close()
    return result

class Exercise1(unittest.TestCase):

    def test1(self):
        command = "python3 password_checker.py Abcde1fg"
        sought = """False
"""
        got = run(command)
        self.assertNotEqual(got, "__TIMEOUT__")
        self.assertEqual(got, sought)

    def test2(self):
        command = "python3 password_checker.py Abcde1@g"
        sought = """True
"""
        got = run(command)
        self.assertNotEqual(got, "__TIMEOUT__")
        self.assertEqual(got, sought)

class Exercise2(unittest.TestCase):

    def test1(self):
        command = "python3 word_frequencies.py"
        sought = """of -> 2
the -> 2
it -> 2
times -> 2
was -> 2
worst -> 1
best -> 1
"""
        got = run(command, "it was the best of times it was the worst of times")
        self.assertNotEqual(got, "__TIMEOUT__")
        self.assertEqual(sorted(list(got)), sorted(list(sought)))

class Exercise3(unittest.TestCase):

    def test1(self):
        command = "python point.py 0 1 1 0"
        sought = """p1 = (0.0, 1.0)
p2 = (1.0, 0.0)
d(p1, p2) = 1.41421356237
"""
        got = run(command)
        self.assertNotEqual(got, "__TIMEOUT__")
        self.assertEqual(got, sought)

class Exercise4(unittest.TestCase):

    def test1(self):
        command = "python interval.py 3.14"
        sought = """[2.5, 3.5] contains 3.140000
[3.0, 4.0] contains 3.140000
[0.0, 1.0] intersects [0.5, 1.5]
[0.0, 1.0] intersects [1.0, 2.0]
[0.5, 1.5] intersects [1.0, 2.0]
[0.5, 1.5] intersects [1.5, 2.5]
[1.0, 2.0] intersects [1.5, 2.5]
[1.5, 2.5] intersects [2.5, 3.5]
[2.5, 3.5] intersects [3.0, 4.0]
"""
        got = run(command, "0 1 0.5 1.5 1 2 1.5 2.5 2.5 3.5 3 4")
        self.assertNotEqual(got, "__TIMEOUT__")
        self.assertEqual(got, sought)

class Exercise5(unittest.TestCase):

    def test1(self):
        command = "python rectangle.py 1.01 1.34"
        sought = """Area([0.0, 1.0] x [0.0, 1.0]) = 1.000000
Perimeter([0.0, 1.0] x [0.0, 1.0]) = 4.000000
Area([0.7, 1.2] x [0.9, 1.5]) = 0.300000
Perimeter([0.7, 1.2] x [0.9, 1.5]) = 2.200000
[0.7, 1.2] x [0.9, 1.5] contains (1.010000, 1.340000)
[0.0, 1.0] x [0.0, 1.0] intersects [0.7, 1.2] x [0.9, 1.5]
"""
        got = run(command, "0 1 0 1 0.7 1.2 .9 1.5")
        self.assertNotEqual(got, "__TIMEOUT__")
        self.assertEqual(got, sought)
        
class Problem1(unittest.TestCase):

    def test1(self):
        command = "python3 markov_model.py banana 2"
        sought = """freq(an, a) = 2
freq(na, b) = 1
freq(na, a) = 0
freq(na) = 2
"""
        got = run(command, "an a na b na a na -")
        self.assertNotEqual(got, "__TIMEOUT__")
        self.assertEqual(got, sought)

    def test2(self):
        command = "python markov_model.py gagggagaggcgagaaa 2"
        sought = """freq(aa, a) = 1
freq(ga, g) = 4
freq(gg, c) = 1
freq(ag) = 5
freq(cg) = 1
freq(gc) = 1
"""
        got = run(command, "aa a ga g gg c ag - cg - gc -")
        self.assertNotEqual(got, "__TIMEOUT__")
        self.assertEqual(got, sought)
        
class Problem2(unittest.TestCase):

    def test1(self):
        fh = open("data/input17.txt", "r")
        text, k, l = fh.read(), 2, 50
        fh.close()
        command = "python3 text_generator.py %s %s" %(k, l)
        got = run(command, text)
        self.assertNotEqual(got, "__TIMEOUT__")
        self.assertTrue(len(got) == l + 1 and got.startswith(text[:k]))

class Problem3(unittest.TestCase):

    def test1(self):
        command = "python3 fix_corrupted.py 4 it|w~s|th~|bes~|of|tim~s,|i~|was|~he|wo~st|of~times."
        sought = """it was the best of times, it was the worst of times.
"""
        fh = open("data/obama.txt", "r")
        text = fh.read()
        fh.close()
        got = run(command, text)
        self.assertNotEqual(got, "__TIMEOUT__")
        self.assertEqual(got, sought)
        
    def test2(self):
        command = "python3 fix_corrupted.py 2 it|w~s|th~|bes~|of|tim~s,|i~|was|~he|wo~st|of~times."
        sought = """it was the best of times, is was the worst of times.
"""
        fh = open("data/obama.txt", "r")
        text = fh.read()
        fh.close()
        got = run(command, text)
        self.assertNotEqual(got, "__TIMEOUT__")
        self.assertEqual(got, sought)

if __name__ == "__main__":
    unittest.main()
