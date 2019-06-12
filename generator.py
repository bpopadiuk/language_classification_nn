import csv
import random
from converter import Converter

class Generator():
    """ Generator class used to read input and write files.

    Example usage:
        l = ['english', 'spanish']
        g = Generator(l)
        g.convert_sentence(1000, 5)
        g.write_file('csv/inputs_5.csv')
    
    Args:
        langnames (list(str)) : a list of language names
    
    Attributes:
        langnames (list(str)) : a list of language names
        no_langs (int) : number of languages
        no_features (int) : number of features
        features (set()) : a set for features
        word_list{n} (list()) : a list of words in lang{n}

    """
    
    def __init__ (self, langnames):
        self.langnames = langnames
        self.no_langs = len(langnames)
        self.no_features = 22
        self.features = {}
        for i in range(self.no_langs):
            setattr(self, f'word_list{i}', list())

        self._read_files()


    def convert_sentence(self, list_size, size):
        """ Converts sentences to feature vectors and stores them in 
        self.features{n}

        Args:
            list_size (int) : the length of the number of features
            size (int) : the length of the sentence.
        """

        for i in range(self.no_langs):
            word_list = getattr(self, f'word_list{i}')
            
            max_int = len(word_list)
            for j in range(list_size):
                sentence = []
                while len(sentence) != size:
                    word = word_list[random.randrange(max_int)]
                    if word not in sentence:
                        sentence.append(word)

                s = ' '.join(word for word in sentence)
                converter = Converter(s)
                result = converter.result
                result.append(self.langnames[i])
                self.features[f'{self.langnames[i]}{j}'] \
                    = tuple(result)
        return 
                
    
    def write_file(self, filename):
        """Writes features to a csv file.

        Args:
            filename (str) : the name of the file to be written to
        """

        with open(filename, 'w', newline = '') as csvfile:
            langwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for key in self.features:
                value = self.features[key]
                l = []
                for val in value:
                    l.append(str(val))
                langwriter.writerow([l])
        return

    def _read_files(self):
        """Reads word list files to store in self.word_list{n}"""
        
        for langname in self.langnames:
            filename = f'data/word_lists/{langname}.txt'
            with open(filename) as f:
                index = self.langnames.index(langname)
                lang_list = getattr(self, f'word_list{index}')
                words = f.readlines()
                for word in words:
                    fword = ''.join(char for char in word if char is not '\n')
                    lang_list.append(fword)
            f.close()
        return 




# l = ['english', 'spanish', 'mandarin', 'japanese', 'arabic', 'turkish']
# g = Generator(l)
# g.convert_sentence(1000, 5)
# g.write_file('csv/inputs_5.csv')