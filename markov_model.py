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

            # Get the next char and add one to its frequency
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

        if len(kgram) != self.order():
            raise ValueError("kgram length not equal to order")
        elif kgram not in self.st:
            return 0
        else:
            return sum(v for v in self.st[kgram].values())
        
    def char_freq(self, kgram, c):
        """
        Return number of times character c follows kgram.
        """

        if len(kgram) != self.order():
            raise ValueError("kgram length not equal to order")
        elif kgram not in self.st or c not in self.st[kgram]:
            return 0
        else:
            return self.st[kgram][c]
        
    def rand(self, kgram):
        """
        Return a random character following kgram.
        """

        if len(kgram) != self.order():
            raise ValueError("kgram length not equal to order")
        elif kgram not in self.st:
            raise ValueError("kgram not in Markov model")
        else:
            # 0 <= rand <= kgram freq
            rand_num = stdrandom.uniformInt(1, self.kgram_freq(kgram) + 1)

            # Decrement rand by the char_freq until it hits 0
            for c in self.st[kgram].keys():
                rand_num -= self.char_freq(kgram, c)
                if rand_num <= 0:
                    return c
        
    def gen(self, kgram, T):
        """
        Generate and return a string of length T by simulating a trajectory
        through the correspondng Markov chain. The first k (<= T) characters
        of the generated string is the argument kgram.
        """
        
        s = kgram
        for i in range(T - self.order()):
            s += self.rand(s[len(s) - self.order():])

        return s
        
    def replace_unknown(self, corrupted):
        """
        Replace unknown characters (~) in corrupted with most probable
        characters, and return that string.
        """

        original = ''
        for i in range(len(corrupted)):
            if corrupted[i] == '~':

                # Used to keep track of the best possibility
                best_probability = 0
                best_char = None
                
                # Iterate over all possibilities
                kgram = corrupted[i - self.order():i]
                for c in self.st[kgram].keys():

                    # Construct a possibility to test a character
                    test = corrupted[:i] + c + corrupted[i + 1:]
                    probability = 1.0

                    # Perform various tests to see the probability
                    for j in range(self.order() + 1):
                        test_kgram = test[i + j - self.order():i + j]
                        if self.kgram_freq(test_kgram) > 0:
                            probability *= self.char_freq(test_kgram, test[i + j]) / self.kgram_freq(test_kgram)
                        else:
                            probability = 0

                    # Compare the probability of this char to the best
                    if best_probability <= probability:
                        best_probability = probability
                        best_char = c

                # Add the best match to the string
                original += best_char

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
