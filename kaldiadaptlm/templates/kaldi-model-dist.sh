#!/bin/bash

if [ $# != 1 ] ; then
    echo "usage: $0 <model>"
    exit 2
fi

MODEL=$1

EXPNAME=adapt
EXPDIR="exp"

AMNAME="kaldi-${MODEL}-${EXPNAME}"

echo "$AMNAME ..."

rm -rf "$AMNAME"
mkdir -p "$AMNAME/model"

cp $EXPDIR/$EXPNAME/final.mdl                               $AMNAME/model/
cp $EXPDIR/$EXPNAME/final.mat                               $AMNAME/model/ 2>/dev/null
cp $EXPDIR/$EXPNAME/final.occs                              $AMNAME/model/ 2>/dev/null
cp $EXPDIR/$EXPNAME/full.mat                                $AMNAME/model/ 2>/dev/null
cp $EXPDIR/$EXPNAME/splice_opts                             $AMNAME/model/ 2>/dev/null
cp $EXPDIR/$EXPNAME/cmvn_opts                               $AMNAME/model/ 2>/dev/null
cp $EXPDIR/$EXPNAME/tree                                    $AMNAME/model/ 2>/dev/null

mkdir -p "$AMNAME/model/graph"

cp $EXPDIR/$EXPNAME/graph/HCLG.fst                          $AMNAME/model/graph/
cp $EXPDIR/$EXPNAME/graph/words.txt                         $AMNAME/model/graph/
cp $EXPDIR/$EXPNAME/graph/num_pdfs                          $AMNAME/model/graph/
cp $EXPDIR/$EXPNAME/graph/phones.txt                        $AMNAME/model/graph/

mkdir -p "$AMNAME/model/graph/phones"
cp $EXPDIR/$EXPNAME/graph/phones/*                          $AMNAME/model/graph/phones/

if [ -e $EXPDIR/extractor/final.mat ] ; then

    mkdir -p "$AMNAME/extractor"

    cp $EXPDIR/extractor/final.mat                          $AMNAME/extractor/
    cp $EXPDIR/extractor/global_cmvn.stats                  $AMNAME/extractor/
    cp $EXPDIR/extractor/final.dubm                         $AMNAME/extractor/
    cp $EXPDIR/extractor/final.ie                           $AMNAME/extractor/
    cp $EXPDIR/extractor/splice_opts                        $AMNAME/extractor/

    mkdir -p "$AMNAME/ivectors_test_hires/conf"

    cp $EXPDIR/ivectors_test_hires/conf/ivector_extractor.conf  $AMNAME/ivectors_test_hires/conf/
    cp $EXPDIR/ivectors_test_hires/conf/online_cmvn.conf        $AMNAME/ivectors_test_hires/conf/
    cp $EXPDIR/ivectors_test_hires/conf/splice.conf             $AMNAME/ivectors_test_hires/conf/

fi

mkdir -p "$AMNAME/data/local/dict"
cp data/local/dict/*     $AMNAME/data/local/dict/

cp -rp data/lang         $AMNAME/data/

mkdir -p "$AMNAME/conf"
cp conf/mfcc.conf        $AMNAME/conf/mfcc.conf
cp conf/mfcc_hires.conf  $AMNAME/conf/mfcc_hires.conf
cp conf/online_cmvn.conf $AMNAME/conf/online_cmvn.conf

rm -f "$AMNAME.tar" "$AMNAME.tar.xz"
tar cfv "$AMNAME.tar" $AMNAME
xz -v -8 -T 12 "$AMNAME.tar"

rm -r "$AMNAME"

