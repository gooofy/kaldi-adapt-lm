# kaldi-adapt-lm

Adapt Kaldi-ASR nnet3 chain models from Zamia-Speech.org to a different
language model.

Constructive comments, patches and pull-requests are very welcome.

Tutorial
--------

To create the language model we would like to adapt our kaldi model to, we first
need to create a set of sentences. To get started, download and uncompress a generic set
of sentences for you language, e.g.

    wget 'http://goofy.zamia.org/zamia-speech/misc/sentences-en.txt.xz'
    unxz sentences-en.txt.xz

now suppose the file utts.txt contained the sentences you would like the model to
recognize with a higher probability than the rest. To achieve that, we add these
sentences five times in this examples to our text body:

    cat utts.txt utts.txt utts.txt utts.txt utts.txt sentences-en.txt >lm.txt

we also want to limit our language model to the vocabulary the audio model supports,
so let's extract the vocabulary next:

    MODEL="models/kaldi-generic-en-tdnn_sp-latest"
    cut -f 1 -d ' ' ${MODEL}/data/local/dict/lexicon.txt >vocab.txt

with those files in place we can now train our new language model using KenLM:

    lmplz -o 4 --prune 0 1 2 3 --limit_vocab_file vocab.txt --interpolate_unigrams 0 <lm.txt >lm.arpa

Now we can start the kaldi model adaptation process:

    kaldi-adapt-lm ${MODEL} lm.arpa mymodel

You should now be able to find a tarball of the resulting model inside the work subdirectory.

If at the end of adaptation process you have a lot of messages like "cp: cannot stat
'exp/adapt/graph/HCLG.fst': No such file or directory", then highly likely you run out of memory
during adaptation process. (For example adapting kaldi-generic-en-tdnn_250 model consumes near 12Gb
of RAM)

Links
-----

- <http://kaldi-asr.org/> [Kaldi ASR] 
- <https://zamia-speech.org> [Zamia Speech] 

Requirements
------------

- Python 2
- Kaldi ASR

License
-------

My own code is Apache-2.0 licensed unless otherwise noted in the
script’s copyright headers.

Author
------

Guenter Bartsch \<<guenter@zamia.org>\>
