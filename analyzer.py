import string
import copy


def remove_braced(text):
    """str -> str
    Remove braces and data in it.
    """
    result = str()
    start = text.find('(')
    end = text.find(')')
    if start != -1 and end != -1:
        result = text[start+1:end]
    out = text.replace('(' + result + ')', '')
    return out


def parse_word_data(data):
    """str -> tuple
    Return tuple where first element if a word
    and the second is parsed list of synonyms.
    """
    data = data.lower()
    dashed = data.split('—')
    keyword = dashed[0].strip()
    syn_data = str()
    del dashed[0]
    syn_data = "".join(dashed)
    while '(' in syn_data and ')' in syn_data and syn_data.index('(') < syn_data.index(')'):
        syn_data = remove_braced(syn_data)
    syn_data = syn_data.replace(';', ',')
    syn_data = "".join(syn_data.split('\n'))
    syn_data = ", ".join(syn_data.split(','))
    parsed_synonyms = list()
    for word in syn_data.split():
        parsed_synonyms.append(word.replace(',', ' ').strip())
    return keyword, parsed_synonyms


def init_synonyms(path):
    """str -> dict
    Return a dict of synonyms where key is
    a word and value is a list of its synonyms.
    """
    ukrainian_upper = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'
    synons = dict()
    oneword_data = str()
    with open(path, 'r') as data_file:
        for line in data_file:
            if line[0] in ukrainian_upper:
                parsed_data = parse_word_data(line)
                synons[parsed_data[0]] = parsed_data[1]
                oneword_data = str()
            oneword_data += line
    return synons

def posinit_synonyms(synonyms):
    """dict -> dict
    Return corrected synonyms dictionary without 'див.' reference.
    """
    pass


if __name__ == '__main__':
    print(init_synonyms('syn.txt'))