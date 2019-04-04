import stdio
import stdrandom
import sys


class MarkovModel(object):
    """
    Represents a Markov model of order k from a given text string.
    """

    def __init__(self, text, k):
        """
        Create a Markov model of order k from given text (assumed
        to have length at least k).
        """

        # Add first k chars of text to end to make it circular
        text = text + text[:k]

        # Create empty dictionary for holding frequencies
        st = dict()
        for i in range(len(text) - k):

            # Get next k chars and add them to dict
            s = text[i: i + k]
            if s not in st:
                st[s] = {}

            # Get the next char and add one to the frequency
            c = text[i + k]
            if c in st[s]:
                st[s][c] += 1
            else:
                st[s][c] = 1

        # Add properties to MarkovModel instance
        self.st = st
        self.k = k
        
    def order(self):
        """
        Return order of Markov model.
        """

        return self.k

    def kgram_freq(self, kgram):
        """
        Return number of occurrences of kgram in text.
        """

        if len(kgram) != self.k:
            raise ValueError("kgram length not equal to order")
        elif kgram not in self.st:
            return 0
        else:
            return sum(v for v in self.st[kgram].values())
        
    def char_freq(self, kgram, c):
        """
        Return number of times character c follows kgram.
        """

        if len(kgram) != self.k:
            raise ValueError("kgram length not equal to order")
        elif kgram not in self.st or c not in self.st[kgram]:
            return 0
        else:
            return self.st[kgram][c]
        
    def rand(self, kgram):
        """
        Return a random character following kgram.
        """

        if len(kgram) != self.k:
            raise ValueError("kgram length not equal to order")
        elif kgram not in self.st:
            raise ValueError("kgram not in Markov model")
        else:
            total = self.kgram_freq(kgram)
            rand = stdrandom.uniformInt(0, total + 1)
            for c in self.st[kgram]:
                total -= self.st[kgram][c]
                if total <= 0:
                    return c
        
    def gen(self, kgram, T):
        """
        Generate and return a string of length T by simulating a trajectory
        through the correspondng Markov chain. The first k (<= T) characters
        of the generated string is the argument kgram.
        """
        
        s = kgram
        for i in range(T - self.k):
            s += self.rand(s[len(s) - self.k:])

        return s
        
    def replace_unknown(self, corrupted):
        """
        Replace unknown characters (~) in corrupted with most probable
        characters, and return that string.
        """

        # Return the index of the maximum element in the given list a.
        def argmax(a):
            return a.index(max(a))

        original = ''
        for i in range(len(corrupted)):
            if corrupted[i] == '~':
                corrupted[i] = self.rand(corrupted[i - self.k:])
            else:
                original += corrupted[i]
        return original


def _main():
    """
    Test client [DO NOT EDIT].
    """

    text, k = sys.argv[1], int(sys.argv[2])
    model = MarkovModel(text, k)
    a = []
    while not stdio.isEmpty():
        kgram = stdio.readString()
        char = stdio.readString()
        a.append((kgram.replace("-", " "), char.replace("-", " ")))
    for kgram, char in a:
        if char == ' ':
            stdio.writef('freq(%s) = %s\n', kgram, model.kgram_freq(kgram))
        else:
            stdio.writef('freq(%s, %s) = %s\n', kgram, char,
                         model.char_freq(kgram, char))


if __name__ == '__main__':
    _main()
