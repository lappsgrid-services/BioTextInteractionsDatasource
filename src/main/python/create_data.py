"""create_data.py

Script to take the orignal BioText protein-protein interactons data and create
data resources.

This project has been shelved for now, see the README.md file at the top-level
of this repository for reasons.

Usage:

    $ python3 create_data.py

This creates the needed data in ../resources/data.

This script assumes that BioText data with protein-protein interactions are
available in ../resources/biotext/protein-protein. In particular, it needs the
following two files:

   sentences_from_citations_that_contain_both_proteins_for_all_interactions.txt
   sentences_from_full_text_that_contain_both_proteins_for_all_interactions.txt

These files can be downloaded from http://biotext.berkeley.edu/data.html.

For some reason, the second of those files was not UTF8 encoded. It looks like
it may have been the latin-1 encoding and it also looks like it makes strange
use of U+0096 (START OF GUARDED AREA), which the code below replaces with a
dash.

Data Description

Sentences with less than two PROT annotations: 0
Sentences with 2 protein annotations: 1003
Sentences with 3 protein annotations: 369
Sentences with 4 protein annotations: 130
Sentences with 5 protein annotations: 47
Sentences with 6 protein annotations: 13
Sentences with 7 protein annotations: 3
Sentences with 8 protein annotations: 4
Sentences with 9 protein annotations: 0
Sentences with 10 protein annotations: 1

"""

import os
import codecs
import io


BIOTEXT_DIR = '../resources/biotext/protein-protein/'
NAME = 'sentences_from_%s_that_contain_both_proteins_for_all_interactions.txt'
INTERACTIONS1 = BIOTEXT_DIR + NAME % "full_papers"
INTERACTIONS2 = BIOTEXT_DIR + NAME % "citations"


DATA = {}

DATA_DIR = os.path.join('..', 'resources', 'data')
PUBMED_IDS_FILE = os.path.join(DATA_DIR, 'pubmed_ids.txt')


def read_data():
    count = 0
    for line in codecs.open(INTERACTIONS1, encoding="latin_1"):
        count += 1
        if line.strip():
            (relation, sentences) = line.strip().split('=====')
            read_sentences(relation, sentences)


def read_sentences(relation, sentences):
    for sentence in sentences.split('||'):
        identifier, text = sentence.split('==>')
        pubmed_id, prot1, prot2 = identifier.split('_')
        text = text.replace("\N{START OF GUARDED AREA}", '-')
        DATA.setdefault(pubmed_id, []).append((pubmed_id, relation, prot1, prot2, text))


def print_data():

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    with open(PUBMED_IDS_FILE, 'w') as fh_identifiers:
        for pubmedID in DATA:
            #if pubmedID != '10545121': continue
            fh_identifiers.write("%s\n" % pubmedID)
            alltext = io.StringIO()
            offset = 0
            annotations = 0
            proteinID = 0
            with open(os.path.join(DATA_DIR, pubmedID), 'w') as fh:
                #write_file(fh, DATA[pubmedID])
                in_prot1 = False
                in_prot2 = False
                prot1_tokens = []
                prot2_tokens = []
                prot1_type = None
                prot2_type = None
                prot1_start = None
                prot2_start = None
                prot1_end = None
                prot2_end = None

                #print()
                
                for (pubmed_id, relation, prot1, prot2, text) in DATA[pubmedID]:

                    #print(text)

                    if text.count('<PROT') == 2:
                        print(text.count('<PROT'), relation, text)
                        #print(text.count('<PROT'), relation, '\n', text, '\n')
                        
                    for token in text.split():
                        if token.startswith('<PROT1'):
                            in_prot1 = True
                            prot1_start = offset
                            prot1_type = token[7:-1]
                        elif token.startswith('<PROT2'):
                            in_prot2 = True
                            prot2_start = offset
                            prot2_type = token[7:-1]
                        elif token.startswith('</PROT1'):
                            prot1_end = offset - 1
                            #print('\n>>>', relation, prot1_type, prot1_start, prot1_end, prot1_tokens)
                            prot1_tokens = []
                            in_prot1 = False
                        elif token.startswith('</PROT2'):
                            prot2_end = offset - 1
                            #print('\n>>>', relation, prot2_type, prot2_start, prot2_end, prot2_tokens)
                            prot2_tokens = []
                            in_prot2 = False
                        else:
                            alltext.write(token + " ")
                            if in_prot1:
                                prot1_tokens.append(token)
                            elif in_prot2:
                                prot2_tokens.append(token)
                            offset += len(token) + 1

                    #print()
                    alltext.write("\n")
                    offset += 1
                    
                    fh.write("%s\t%s\t%s\t%s\n" % (relation, prot1, prot2, text))

            #print('***')
            #print(alltext.getvalue())
            
            #break
            
                

def write_file(fh, data):
    for (pubmed_id, relation, prot1, prot2, text) in data:
        fh.write("%s\t%s\t%s\t%s\n" % (relation, prot1, prot2, text))
        

        
                
if __name__ == '__main__':
    read_data()
    print_data()
