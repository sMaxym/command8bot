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
    for index in range(len(parsed_synonyms)):
        parsed_synonyms[index] = parsed_synonyms[index].strip('.')
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
    for key in synonyms:
        if 'див' in synonyms[key]:
            try:
                keyword_index = synonyms[key].index('див')
                synonyms[key].extend(synonyms[synonyms[key][keyword_index + 1]])
                synonyms[key].remove('див')
            except:
                synonyms[key].remove('див')
    return synonyms


def find_synonyms(root, synonyms):
    """str -> list(str)
    """
    keys = list()
    result = list()
    for key in synonyms.keys():
        if root in key:
            keys.append(key)
    result.extend(keys)
    for key in keys:
        for word in synonyms[key]:
            if root in word:
                result.append(word)
    return result


def get_word_root(word):
    """str -> str
    Return a main valid part of the word.
    """
    prefixes = ['роз', 'без', 'недо']
    for prefix in prefixes:
        if word.startswith(prefix):
            word = word[len(prefix):]
            break
    return word[:len(word) // 2] if len(word) > 4 else word


if __name__ == '__main__':
    # test_dict = init_synonyms('syn.txt')
    # test_dict = posinit_synonyms(test_dict)
    # with open('out.txt', 'w') as f:
    #     for key in test_dict:
    #         print(key, test_dict[key], file=f)

    test_dict = init_synonyms('syn.txt')
    test_dict = posinit_synonyms(test_dict)
    print(find_synonyms(get_word_root('аналіз'), test_dict))