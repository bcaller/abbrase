all: unigrams.json

CFLAGS=-Wall -Wextra -Os

CORPUS_EXEMPLAR=z.gz

data/${CORPUS_EXEMPLAR}:
	mkdir -p data
	cd data; curl -o "./data/#1.gz" --create-dirs -C - \
				'http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-1gram-20120701-[a-z].gz'

# the ngrams data is 'mostly sorted' -- lines tend to be in order, but it occasionally restarts
# do a groupby (join records from different years into one) to reduce the data volume, then final sort+groupby
data/1gram.csv.gz: | data/${CORPUS_EXEMPLAR} groupby
	zcat data/*.gz | pv | ./groupby 3 | LC_ALL=c sort | ./groupby 2 | gzip -9 > $@

# extract the 100,000 most common words
data/1gram_common.csv: data/1gram.csv.gz
	zcat $< | sort -rgk2 | head -n 100000 > $@

data/prefixes.txt: data/1gram_common.csv
	cat $< | sed 's/^\(...\).*\t/\1\t/' | grep '^[a-z]\{3\}' | LC_ALL=c sort | ./groupby 2 | sort -rgk2 | head -n 1024 | tr "\\n" "," | sed 's/,$//' > $@

unigrams.json:
	# relies on data/prefixes.txt data/*.gz,
	pypy unigrams.py