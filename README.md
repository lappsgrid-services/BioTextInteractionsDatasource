# BioTextInteractionsDatasource

Data source for protein-protein interactions from the BioText project. For more information on these BioText data see http://biotext.berkeley.edu/data.html and the Rosario & Hearst paper on that page.

***This project has been abandoned for now, see below for reasons.***

The protein-protein interaction data are NOT gold annotations of text. Instead, it is a database of textual occurrences of protein pairs that stand in a particular relation. For example, it has data for the pair <*tat*, *RelA*> in an *activates* relation, including the following which shows how the pair cooccurs in a sentence:

> To show that the retarded band observed by EMSA in HIV - <PROT1_155871>  tat </PROT1_155871> - treated cells was indeed NF - B , nuclear extracts were incubated with antibodies either to p50 ( NF - B1 ) or to p65 ( <PROT2_5970>  RelA </PROT2_5970> ) subunits .

It is not the case that the relation is expressed in this piece of text, it could, but it does not have to be the case. The goal for this dataset was to provide training data for protein pairs, not a gold standard.

Since we were looking for a gold standard of text annotations we are not currently pursuing these data.
