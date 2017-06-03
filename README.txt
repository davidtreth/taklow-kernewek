Author: David Trethewey davidtreth@gmail.com

Dynnargh dhe taklow-kernewek
Welcome to taklow-kernewek

A series of mainly python programs for language processing
focused on the Cornish language. 
I will be uploading some more as I develop things and tidy up old code.

The source code is open-source with a GNU General Public License.
Corpus is from
www.howlsedhes.co.uk/kerneweg (Traditional Texts)
www.kernewegva.com/tekstow.html (Solempnyta - Benjamin Bruch)
www.learncornishlanguage.co.uk (Lord of the Rings translation by Jerry Sethir)
www.kesva.org/free-books-to-download (Example sentences from Skeul an Yeth 1 - Wella Brown + Kesva an Taves Kernewek/Cornish Language Board)


Description:

cornish_corpus.py: some code using the Python NLTK to analyse Cornish text statistically.

find the commonest words in particular texts (see kernewek-corpus folder) etc.
The program is now capable of counting letter frequencies within a text including ch, gh, dh, th, and sh as consonant digraphs and the gemminate forms as trigraphs, and oe, eu, and ou as vowel digraphs.
There are other potential things that may in future be done with corpora in NLTK see http://www.nltk.org/
This program will need Python NLTK and matplotlib to be available.

inflektya.py: a python module to inflect Cornish verbs by tense and person and prepositions by person. Based on A Grammar of Modern Cornish, 3rd ed. W. Brown 2001, and Cornish Verbs, 3rd ed. Kesva an Taves Kernewek 2010. There are some classes of verbs which may be incompletely or incorrectly dealt with.

mutatya.py: a python module to mutate a Cornish word where you give the word as a string and the desired mutation state as an integer between 1 and 6.
Mutation is a phonetic feature of Cornish (similar to how it happens in Welsh) whereby the initial consonants of words can change in certain grammatical circumstances, e.g, kath = a cat, an gath = the cat.
update 28.07.16: this now provides a facility to generate possible reverse mutations of a given word, e.g. "garr" could be original "garr" or "karr". These are not checked as to whether they actually exist in Cornish or whether the mutation is grammatically possible for that word. 
The option to use 'traditional' graphs of the form used in SWF/T is now available.
update 10.08.16: now includes functions mutate_cy() and rev_mutate_cy() to do Welsh mutations

sylabellen_ranna.py: a module for splitting Cornish words into their consituent syllables. A work in progress and a prelimary to a program to transliterate between different Cornish spelling systems such as Kemmyn and the Standard Written Form. It has also been suggested to me that in future I could also develop this in the area of rhyme, and poetry etc.
Update (08-07-15): now this calculates syllable and word length on the basis of 1 unit for a short vowel or consonant, 2 for half-long vowel or gemminate 'double' consonant, or 3 for a long vowel.
Update (16-04-16): there is now an option to go through line-by-line counting the number of syllables in each line with the --line option. The --short option simply reports the number of syllables found in each word rather than giving details.
Update (18-03-17): There are now regular expressions in the Standard Written Form of Cornish (FSS). The regular expressions have also been rewritten using re.compile for clarity.
There is some more work to do because some words have more than one possible segmentation. This can be an issue when a rare consonant cluster exists, such as <lv> in palv etc. but other words such as milvil have the same grapheme split into two syllables. However once the <lv> grapheme is allowed to terminate a syllable, milvil is split into ['milv', 'il'] in forward segmentation mode.
A similar issue exists with <rv> in arv etc. Possibly develop a version that identifies every possible segmentation, and assigns probabilities somehow.


# Usage: python sylabelenn_ranna_kw.py <inputfile>
# where <inputfile> is the path to an input file containing 
# text in Kernewek Kemmyn
#
# there are optional command line switches --test (runs some extra test code), --line (line by line processing of input),
# --short (only reports number of syllables in each word rather than displaying details)



treuslytherenna.py: a module for converting Kernewek Kemmyn text to the Standard Written Form of Cornish. 

# Usage python treuslytherenna.py [--short] [--line] [--verberr] <inputfile>
# where <inputfile> is the path to an input file containing text in Kernewek Kemmyn
# and --short causes it to only output the SWF text, and --line processes the input line by line and outputs Kernewek Kemmyn
# and SWF text interlinearlly
# --verberr flags up when the segmentation fails to use all of the word

testenn.txt and cw_strip.txt are files I have been using to feed sylabellen_ranna.py with material, either small sets of test words, or the Creation of the World in Kernewek Kemmyn with line numbers etc. stripped out

niverow.py: this contains functions to generate text numbers in Cornish, either from integers, or with the noun included. 

kovtreylyans.py: A rudimentary 'Translation Memory' tool. Take an input English sentence and find common bigrams and trigrams with a set of bilingual sentences, and return these as output along with sentences in which they occur, currently using the end of chapter examples from Skeul an Yeth 1 by Wella Brown. Options exist to find all bigrams and trigrams, or only those that contain at least one non-stopword (based on NLTK stopwords corpus).

termyn.py: A set of functions for telling the time and date in Cornish. This makes use of the Python time module, and also the niverow.py module.

wordnettest.py: a program that uses the NLTK Wordnet corpus to find related words from an input English sentence, in order to attempt to find synonynms in the bilingual corpus.
For example 'hill' has a number of synsets, one of which is a hyponym of the Synset('natural_elevation.n.01'): a raised or elevated geological formation. The hyponyms of this will include words such as mountain.
However it is also a baseball term Synset('mound.n.01'): (baseball) the slight elevation on which the pitcher stands and the hypernym Synset('baseball_equipment.n.01'): equipment used in playing baseball will match to a wide variety of baseball terms.
As it is quite experimental and doesn't have a GUI frontend (yet), it is not included in the launch bar of TaklowKernewekLonchyer.pyw, so should be separately launched.

apposyans_awrgrym.py: ask the user 20 mental arithmetic questions with numbers as Cornish words.

Graphical User Interface frontends
==================================

TaklowKernewekLonchyer.pyw: A launcher bar which launches the other Python scripts. It may be necessary to copy the taklowGUI.py script or create a symbolic link in the espeaktexttospeech directory since otherwise its import fails when launched in this way. The launcher bar uses TaklowKernewekLonch.py which is adaptation of PyGadgets.py from the Programming Python 3rd edition examples. This uses the further programs launchmodes.py and Launcher.py taken from the Programming Python 3rd edition examples.

TaklowKernewekLonchyer_netbook.pyw: This is a version of the launcher bar, which sets some of the GUI window sizes more suited to smaller screen sizes.

kovtreylyansGUI.py: A Tkinter GUI frontend for kovtreylyans.py.

espeaktexttospeech/: This folder contains scripts that enable the use of the espeak text-to-speech software to make a basic attempt at reading Cornish text. This was achieved by using string replace functions to alter the spelling to conform the text to Welsh spelling conventions to the extent that the espeak Welsh voice will produce an approximately correct result. The espeak Welsh voice is fairly basic so it is not very realistic. 
The gorhemmyn_kw.py file greets the user depending on the time of day according to the system clock (uses espeak).

sentence_generator/: This folder contains some horribly obsfucated Python code to generate random sentences following particular structures in Cornish from a small vocabulary. It can optionally give an English gloss on the sentences.

taklowGUI.py: defines some Tkinter GUI widgets imported by other GUI modules.

mutatyaGUI.py: A Tkinter GUI frontend for mutatya.py. Now includes reverse mutation, and option for 'traditional' graphs as used in SWF/T.

treigloGUI.py: A Tkinter GUI for the Welsh mutation functions of mutatya.py. Not included in the launch bar of TaklowKernewekLonchyer.pyw, so should be separately launched. There will in future be a separate launch bar for Welsh language tools.

sylrannaGUI.py: A Tkinter GUI frontend for syllabenn_ranna_kw.py

treuslytherennaGUI.py: A Tkinter GUI frontend for treuslytherenna.py 

inflektyaGUI.py: A Tkinter GUI frontend for inflektya.py

termynGUI.py: A Tkinter GUI frontend for termyn.py, allowing display of the date, and time either approximate to quarter hours, or to the minute, or a greeting appropriate to the time of day.

espeaktexttospeech/kows_kernewek_GUI.py: A Tkinter GUI for Cornish text to speech.

corpus_wordfreqGUI.py: A Tkinter GUI to output the frequencies of the most common words in the corpus texts, draw a cumulative frequency plot of lengths of words in the texts, or draw a grouped bar chart of frequencies of particular words.
In the last case, it is neccesary to add words to the samples list using the entry box and buttons in the middle panel (or accept the default sample list).
It can also now count letter frequencies, using consonant and vowel digraphs.

This counts the numbers of each character using a defaultdict(int) adding one to d[c] whenever the character c is encountered.
Digraphs are handled by temporarily replacing the digraphs with single characters and looping through the alphabetic words of the text joined into a as a single string.
For example the digraph ch is replaced by č and sh by š before looping through, but converted back to ch and sh for output.
Update 22/10/16: In the GUI there is now an option to use, or not use the digraphs in the letter frequency calculation (except ch which is used in both cases).

It is also possible to draw a lexical dispersion plot, showing where in a text particular words appear graphically, as a percentage of the whole text.

As of May 2017, there is now an option to choose the interface language of the GUI (Cornish or English) and switch between using Kernewek Kemmyn and manuscript spellings (there is a different set of texts available in each).

apposyans_awrgrymGUI.py: A graphical user interface mental arithmatic quiz.

Allows choice between easy (only numbers 1 to 10, and answers are always >= 0), medium (input numbers up to 20, and negative answers allowed), hard (input numbers up to 40).
It can also be specified whether to have only addition, or subtraction, or either, randomly chosen.

