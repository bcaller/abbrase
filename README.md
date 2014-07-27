#Abbrase POS (Parts of Speech)#

Abbrase is an abbreviated passphrase generator. An abbrase is one of the passwords it produces. It generates a password and a phrase like "phyeigdolrejutt" and "physical eight dollars rejected utterly".

Try the [web version](http://rmmh.github.io/abbrase).

Creating secure passwords is easy. Remembering them is hard. [Pwgen](http://sourceforge.net/projects/pwgen/) makes them memorable though prounouncability. XKCD [suggests](http://xkcd.com/936/) using a series of random common words, but memorizing series of unrelated words can be difficult, and typing long phrases can be tedious.

Abbrase POS uses parts of speech to make phrases of the form ADJECTIVES*-NOUN-VERB-ADJECTIVES*-NOUN, and abbreviating each word to the first few letters. This strikes a balance between excessive password length and excessive mnemonic length. Passwords generated by Abbrase are as secure as a number with the same length. "122079103" and "toldulbal" (tolerably dull ball) are equally hard to attack.

See the original by rmmh for a more sophisticated version using bigrams and Markov chains. I, however, prefer the results from this version. A combination of the two approaches may be even better, although n-gram data includes articles and prepositions (a, the, for, of…) which I ignore.

The wordlist was generated with data from Google NGrams [dataset](http://storage.googleapis.com/books/ngrams/books/datasetsv2.html), used under the [Creative Commons Attribution 3.0 Unported License](http://creativecommons.org/licenses/by/3.0/). However, it needed slight modification as there are some words which have the wrong parts of speech tagged or are OCR mistakes. A better solution to my modifications is possible soon.

##Theory##

Language is the most information-dense thing people memorize. Brains don't operate on bits.

Pi recitation record-holders don't have thousands of digits in their minds. They map clusters of digits to far more mentally palatable words, memorizing a long story instead of a sequence of digits.

Memorizing a grammatically-sensible sentence fragment is easier than a sequence of randomly chosen words.

Picking a favorite phrase from the ones generated by Abbrase could make them very slightly easier to attack. A sophisticated attacker could check passwords that are likely to be picked before others. If the attacker can perfectly model which passwords you would prefer, this reduces the security of your password in a proportioanl amount to the number of passwords you selected it from -- if you picked from 32 passwords generated by abbrase, it makes your password 32x easier to attack (5 bits of security lost).

##Building##

    git clone https://github.com/bcaller/abbrase.git
    cd abbrase
    make
    ./abbrase
    
If you want to make your own prefix list of 1024 3-letter prefixes (as I have):

* Put comma separated prefixes.txt in ./data
* Download all http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-1gram-20120701-[a-z].gz for [a-z] with prefixes to ./data/[a-z].gz
* Run py unigrams.py to make unigrams.json

unigrams.json is a dictionary of "prefix" : Array(Array(adjective suffixes), Array(noun suffixes), Array(verb suffixes)) and can be modified if you want

##Getting phrases##
abbrase.py
or
	from abbrase import abbrase
	abbrase(num=7)


##FAQ##

*Q:* Isn't using a phrase more secure than abbreviating it?

*A:* Not at all for phrases Abbrase generates. Displayed phrases are generated deterministically from the password, so they have no added security. Otherwise yes, 4 words have more security than 4 abbreviated words, but they're less convenient to type, and the added characters aren't as valuable as the first few characters.

##Sample output##

(don't actually use any of these passwords!)

    Generating passwords with 50 bits of entropy
    Password            Phrase
    ---------------     --------------------
	emboraneateetoo		embryonic orange nears teenaged tool
	rairevtowawatak		raised revenue towed aware taking
	smumasdegjunnea		smudgy mas degrades junctional nearer
	adhmutnodwiltho		adhoc mutilation nodding willed thorn
	cobpoifunpaleno		cobblestoned point funds palpable enormity
	teshisunphimrus		testy historian unpacks hime ruse
	bruacrlevunphac		brutish acronym levelled unpleasant hacienda
	darhoswaitopqui		daring host waits topmost quiet
	admparranhopeye		admirable partner rang hopeless eyelid
	tolsinhatsovcop		tolerable singer hatches sovran copy
	hacanyindwavnei		hac anything indulges wavelike neighborhood
	dedbotempfutent		deductible bottom emphasises futuristic entrance
	eagfauacqhelmap		eager fault acquires helpful map
	actmerdeafounei		actual merger deals foul neighborhood
	oneloopiecoaonl		onerous loom pierces coarse onlooker
	dodabucivkniobv		doddering abuse civilise knitted obverse
	incfivmakavautt		incomplete fiver make available utterance
	movoftwonbaccri		moveable oft won backward critic
	tinliaingsamite		tinted liabilities ingrained same item
	tasafrdemsafmap		tasty africanus demonstrate safest mapping
	toutitsermanwat		toughest title services many water
	edidomabitesack		edited dominance abides testable ackson
	ariacqrushimsis		arithmetical acquaintance rustles hime sister
	bonaimhilbinavo		boned aim hile binocular avocado
	looliqmodexcsyn		looking liqueur modeled exciting synthesis
	goueigniccashan		gouged eigenvalue nicks casual handle
	grawiflovrandus		gradual wife loves randomness dusk
	socinvinhweifru		socialist invention inhabits weightless frustration
	hurfleexifauegg		hurtful fleet exists faulty egg
	dicpanenfcoioxi		dictionary pant enforces coiled oxide
	canascsamfieacu		canonical asceticism sampled fiercest acumen
	optnoipuspilacr		optimistic noise pushes pillared acreage
	wandiradenavcov		wanted dirt adenosine navigational coverage
	thoteldolvotsom		thousand telegram doles votive someone
	boipupsinyelpan		boisterous pupil singing yellowish pant
	eggsencelshaavo		eggshaped sensation celebrates sharp avocado