import sys

print('Počet argumentů:', len(sys.argv), 'arguments.')
print('Seznam argumentů:', str(sys.argv))


def read_txt_file_as_chars(filename):
    with open(sys.argv[1], 'r', encoding='utf8') as reader:
        chars = reader.read()
    return chars


def read_txt_file_as_lines(filename):
    with open(sys.argv[1], 'r', encoding='utf8') as reader:
        lines = reader.readlines()
    return lines


def write_txt_file_as_chars(filename, chars, reverse=False):
    chars = chars if not reverse else reversed(chars)
    with open(filename, 'w', encoding='utf8') as writer:
        for char in chars:
            writer.write(char)
    return filename


def write_txt_file_as_lines(filename, lines, reverse=False):
    lines = lines if not reverse else reversed(lines)
    with open(filename, 'w', encoding='utf8') as writer:
        for line in lines:
            writer.write(lines)
    return filename


znaky = read_txt_file_as_chars(sys.argv[1])
write_txt_file_as_chars(sys.argv[2], znaky)
print(read_txt_file_as_chars(sys.argv[2]))