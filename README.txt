Author: David Trethewey davidtreth@gmail.com

Dynnargh dhe "taklow-kernewek"

Welcome to taklow-kernewek

A series of mainly python programs for language processing
focused on the Cornish language. 
I will be uploading some more as I develop things and tidy up old code.
The code is open-source with a GNU GPL.

Description:
cornish_corpus.py: a little bit of code using the Python NLTK to analyse Cornish text statistically, find commonest words in particular texts (see kernewek-corpus folder) etc. There are other potential things that may be done with corpora in NLTK see http://www.nltk.org/ This will need Python NLTK and matplotlib to be available.

inflektya.py: a python module to inflect Cornish verbs by tense and person and prepositions by person. Based on A Grammar of Modern Cornish, 3rd ed. W. Brown 2001, and Cornish Verbs, 3rd ed. Kesva an Taves Kernewek 2010. There are some classes of verbs which may be incompletely or incorrectly dealt with.

mutatya.py: a python module to mutate a Cornish word where you give the word as a str and the desired mutation state as an integer between 1 and 6. Mutation is a phonetic feature of Cornish (similar to how it happens in Welsh) whereby the initial consonants of words can change in certain grammatical circumstances, e.g, kath = a cat, an gath = the cat.

sylabellen_ranna.py: a module for splitting Cornish words into their consituent syllabels. A work in progress and a prelimary to a program to transliterate between different Cornish spelling systems such as Kemmyn and the Standard Written Form. It has also been suggested to me that in future I could also develop this in the area of rhyme, syllable length, and poetry etc.
Update (08-07-15): now this calculates syllable and word length on the basis of 1 unit for a short vowel or consonant, 2 for half-long vowel or gemminate 'double' consonant, or 3 for a long vowel.
Update (16-04-16): there is now an option to go through line-by-line counting the number of syllables in each line with the --line option. The --short option simply reports the number of syllables found in each word rather than giving details.

# Usage: python sylabelenn_ranna_kw.py <inputfile>
# where <inputfile> is the path to an input file containing 
# text in Kernewek Kemmyn
#
# there are optional command line switches --test (runs some extra test code), --line (line by line processing of input),
# --short (only reports number of syllables in each word rather than displaying details)

treuslytherenna.py: a module for converting Kernewek Kemmyn text to the Standard Written Form of Cornish. It is currently incomplete since it does not implement all differences between Kemmyn and SWF yet, and requires some more testing.

# Usage python treuslytherenna.py [--short] [--line] [--verberr] <inputfile>
# where <inputfile> is the path to an input file containing text in Kernewek Kemmyn
# and --short causes it to only output the SWF text, and --line processes the input line by line and outputs Kernewek Kemmyn
# and SWF text interlinearlly
# --verberr flags up when the segmentation fails to use all of the word

testenn.txt and cw_strip.txt are files I have been using to feed sylabellen_ranna.py with material, either small sets of test words, or the Creation of the World in Kernewek Kemmyn with line numbers etc. stripped out

niverow.py: this contains functions to generate text numbers in Cornish, either from integers, or with the noun included. 

espeak-text-to-speech/: This folder contains scripts that enable the use of the espeak text-to-speech software to make a basic attempt at reading Cornish text. This was achieved by using string replace functions to alter the spelling to conform the text to Welsh spelling conventions to the extent that the espeak Welsh voice will produce an approximately correct result. The espeak Welsh voice is fairly basic so it is not very realistic. 
The gorhemmyn_kw.py file greets the user depending on the time of day according to the system clock (uses espeak).

sentence_generator/: This folder contains some horribly obsfucated Python code to generate random sentences following particular structures in Cornish from a small vocabulary. It can optionally give an English gloss on the sentences.

taklowGUI.py: defines some Tkinter GUI widgets imported by other GUI modules

mutatyaGUI.py: A Tkinter GUI frontend for mutatya.py

sylrannaGUI.py: A Tkinter GUI frontend for syllabenn_ranna_kw.py

treuslytherennaGUI.py: A Tkinter GUI frontend for treuslytherenna.py 

inflektyaGUI.py: A Tkinter GUI frontend for inflektya.py

espeak-text-to-speech/kows_kernewek_GUI.py: A Tkinter GUI for Cornish text to speech.

TaklowKernewekLonchyer.pyw: A launcher bar which launches the other Python scripts. It may be necessary to copy the taklowGUI.py script or create a symbolic link in the espeak-text-to-speech directory since otherwise its import fails when launcher in this way. The launcher bar uses TaklowKernewekLonch.py which is adaptation of PyGadgets.py from the Programming Python 3rd edition examples. This uses the further programs launchmodes.py and Launcher.py taken from the Programming Python 3rd edition examples.


