### Cornish sentence generator ###
### David Trethewey ###

this directory contains some horribly 
obsfuscated Python code to generate random Cornish 
sentences. I wrote this a fair while ago and it grew organically over
a period of time, and the program needs substantial revision
to improve the structure.

Requires espeak to actually speak the sentences.

Python scripts:

keskows5.py: the main program which creates the sentences and writes
them to the command line. Using a predefined structure select words
randomly from lists to make sentences.
This is essentially a not very rigourously defined version of a context-free grammar.
Verb inflections are done with a function inside the module. 
TODO - reimplement with external modules inflektya + mutatya. and a lot of 
tidying up.
use command-line flags --onesent to write only one sentence
    		      --english to include an english translation
		      --writetofile to write to files rather than just 
		      		    the command-line

keskows5_word.py: defines a 'word' object to describe a cornish word. This
containes the spelling, part of speech, semantic category, gender,
and English gloss.

keskows5_readwords.py: reads the words in the vocabulary from the text files
There are text files containing the vocabulary for each semantic category.

keskows5_createword.py: a script for the user to interactively add new words 
from the command-line

kernewek_to_welshorthography.py: used to transliterate the spelling for espeak's
Welsh voice.

Shell script:
kows_lavar.sh: runs keskows5.py writing one sentence to file, then kernewek_to_welshorthography.py on the output of that and then espeak on that.
