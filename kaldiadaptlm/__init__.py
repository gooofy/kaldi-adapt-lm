#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016, 2017, 2018 Guenter Bartsch
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# adapt an existing kaldi model to a new language model
#

import os
import sys
import logging

from nltools import misc

def kaldi_adapt_lm(kaldi_root, src_model_dir, lm_fn, work_dir, dst_model_name):

    steps_path = '%s/egs/wsj/s5/steps' % kaldi_root
    if not os.path.exists (steps_path):
        raise Exception ('%s does not exist - is kaldi really installed in %s ?' % (steps_path, kaldi_root))

    tmpl_dir = os.path.dirname(os.path.abspath(__file__)) + '/templates'

    #
    # copy dictionary and phoneme sets from original model
    #

    logging.info("copying dictionary and phoneme sets from original model...")

    misc.mkdirs('%s/data/local/dict' % work_dir)
    misc.copy_file ('%s/data/local/dict/lexicon.txt' % src_model_dir,           '%s/data/local/dict/lexicon.txt' % work_dir)
    misc.copy_file ('%s/data/local/dict/nonsilence_phones.txt' % src_model_dir, '%s/data/local/dict/nonsilence_phones.txt' % work_dir)
    misc.copy_file ('%s/data/local/dict/silence_phones.txt' % src_model_dir,    '%s/data/local/dict/silence_phones.txt' % work_dir)
    misc.copy_file ('%s/data/local/dict/optional_silence.txt' % src_model_dir,  '%s/data/local/dict/optional_silence.txt' % work_dir)
    misc.copy_file ('%s/data/local/dict/extra_questions.txt' % src_model_dir,   '%s/data/local/dict/extra_questions.txt' % work_dir)

    #
    # language model 
    #

    misc.copy_file (lm_fn, '%s/lm.arpa' % work_dir)

    #
    # create skeleton dst model
    #

    logging.info("creating skeleton destination model...")

    misc.mkdirs ('%s/exp/adapt'  % work_dir)

    misc.copy_file ('%s/model/final.mdl' % src_model_dir, '%s/exp/adapt/final.mdl' % work_dir)
    misc.copy_file ('%s/model/cmvn_opts' % src_model_dir, '%s/exp/adapt/cmvn_opts' % work_dir)
    misc.copy_file ('%s/model/tree'      % src_model_dir, '%s/exp/adapt/tree'      % work_dir)

    for optional_file in [ 'final.mat', 'splice_opts', 'final.occs', 'full.mat' ] :
        if os.path.exists('%s/model/%s' % (src_model_dir, optional_file)):
            misc.copy_file ('%s/model/%s' % (src_model_dir, optional_file), '%s/exp/adapt/%s' % (work_dir, optional_file))

    if os.path.exists('%s/extractor' % src_model_dir):

        misc.mkdirs ('%s/exp/extractor' % work_dir)

        misc.copy_file ('%s/extractor/final.mat'         % src_model_dir, '%s/exp/extractor/final.mat'         % work_dir)
        misc.copy_file ('%s/extractor/global_cmvn.stats' % src_model_dir, '%s/exp/extractor/global_cmvn.stats' % work_dir)
        misc.copy_file ('%s/extractor/final.dubm'        % src_model_dir, '%s/exp/extractor/final.dubm'        % work_dir)
        misc.copy_file ('%s/extractor/final.ie'          % src_model_dir, '%s/exp/extractor/final.ie'          % work_dir)
        misc.copy_file ('%s/extractor/splice_opts'       % src_model_dir, '%s/exp/extractor/splice_opts'       % work_dir)

        misc.mkdirs ('%s/exp/ivectors_test_hires/conf' % work_dir)

        misc.copy_file ('%s/ivectors_test_hires/conf/splice.conf'       % src_model_dir, '%s/exp/ivectors_test_hires/conf'    % work_dir)

    misc.mkdirs ('%s/conf'  % work_dir)
    misc.copy_file ('%s/conf/mfcc.conf' % src_model_dir,        '%s/conf/mfcc.conf' % work_dir)
    misc.copy_file ('%s/conf/mfcc_hires.conf' % src_model_dir,  '%s/conf/mfcc_hires.conf' % work_dir)
    misc.copy_file ('%s/conf/online_cmvn.conf' % src_model_dir, '%s/conf/online_cmvn.conf' % work_dir)

    #
    # copy scripts and config files
    #
     
    misc.copy_file       ('%s/kaldi-run-adaptation.sh' % tmpl_dir, '%s/run-adaptation.sh' % work_dir)
    misc.copy_file       ('%s/kaldi-cmd.sh' % tmpl_dir,            '%s/cmd.sh' % work_dir)
    misc.render_template ('%s/kaldi-path.sh.template' % tmpl_dir,  '%s/path.sh' % work_dir, kaldi_root=kaldi_root)
    misc.copy_file       ('%s/kaldi-model-dist.sh' % tmpl_dir,     '%s/model-dist.sh' % work_dir)

    misc.symlink ('%s/egs/wsj/s5/steps' % kaldi_root, '%s/steps' % work_dir)
    misc.symlink ('%s/egs/wsj/s5/utils' % kaldi_root, '%s/utils' % work_dir)

    cmd = '/bin/bash -c "pushd %s && bash run-adaptation.sh && popd"' % work_dir
    logging.info (cmd)
    os.system (cmd)

    cmd = '/bin/bash -c "pushd %s && bash model-dist.sh "%s" && popd"' % (work_dir, dst_model_name)
    logging.info (cmd)
    os.system (cmd)


