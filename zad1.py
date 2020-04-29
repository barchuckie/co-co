import argparse
import math


def parse_arguments():
    """Handle program arguments."""
    argparser = argparse.ArgumentParser(description='Sign counter')

    argparser.add_argument(
        "input_file",
        help='Input file to count bytes from.'
    )

    return argparser.parse_args()


def byte_counter(input_file):
    """Read bytes from file and collect data.
    
    -- input_file - file to read bytes from
    """
    sym_counter = {}
    total = 0
    conditional_counter = {}
    current_sym = b'\x00'
    with open(input_file, 'rb') as file:
        byte = file.read(1)
        while byte:
            if byte not in sym_counter.keys():
                sym_counter[byte] = 0
            if byte not in conditional_counter.keys():
                conditional_counter[byte] = {}
            if current_sym not in conditional_counter[byte].keys():
                conditional_counter[byte][current_sym] = 0
            sym_counter[byte] += 1
            conditional_counter[byte][current_sym] += 1
            total += 1
            current_sym = byte
            byte = file.read(1)

    s = 0
    for letter, cond_letters in conditional_counter.items():
        print(f'{letter}: Total: {sym_counter[letter]}')
        for l, v in cond_letters.items():
            print(f'\t\t{l} : {v}')
            if l in sym_counter.keys():
                s += v*(math.log(sym_counter[l],2) - math.log(v,2))

    print('Total:', total)

    # entropy
    print("Entropy:", sum([x*(math.log(total,2)-math.log(x,2)) for x in sym_counter.values()])/total)
    print(f'Conditional entropy: {s/total}')


def main():
    """Read file and print data about it."""
    args = parse_arguments()
    byte_counter(args.input_file)


if __name__ == "__main__":
    main()
