import stdio
import sys
from markov_model import MarkovModel


def main():
    # Get command line args as ints
    k = int(sys.argv[1])
    T = int(sys.argv[2])

    # read text from standard input
    text = sys.stdin.read()

    # Generate the random text from a MarkovModel
    random_text = MarkovModel(text, k).gen(text[:k], T)

    # Write result
    stdio.writeln(random_text)

if __name__ == '__main__':
    main()
