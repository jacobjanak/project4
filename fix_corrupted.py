import stdio
import sys
from markov_model import MarkovModel


def main():

    # Get command line arguments
    k = int(sys.argv[1])
    s = sys.argv[2]

    # Read text from standard input
    text = sys.stdin.read()

    # Create MarkovModel instance from text
    M = MarkovModel(text, k)

    # Write the result
    stdio.writeln(M.replace_unknown(s))


if __name__ == '__main__':
    main()
