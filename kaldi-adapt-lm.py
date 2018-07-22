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

from optparse     import OptionParser
from nltools      import misc
from kaldiadaptlm import kaldi_adapt_lm

DEFAULT_KALDI_ROOT = '/opt/kaldi'
DEFAULT_WORK_DIR   = 'work'

#
# init 
#

misc.init_app ('kaldi-adapt-lm')

#
# commandline parsing
#

parser = OptionParser("usage: %prog [options] src_model_dir lm.arpa dst_model_name")

parser.add_option ("-f", "--force", action="store_true", dest="force",
                   help="overwrite work dir if it exists")

parser.add_option ("-k", "--kaldi-root", dest="kaldi_root", type = "str", default=DEFAULT_KALDI_ROOT,
                   help="kaldi root dir (default: %s)" % DEFAULT_KALDI_ROOT)

parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="enable verbose logging")

parser.add_option ("-w", "--work-dir", dest="work_dir", type = "str", default=DEFAULT_WORK_DIR,
                   help="work dir (default: %s)" % DEFAULT_WORK_DIR)

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

if len(args) != 3:
    parser.print_usage()
    sys.exit(1)

src_model_dir  = args[0]
lm_fn          = args[1]
dst_model_name = args[2]
work_dir       = options.work_dir

if os.path.exists(work_dir):
    if options.force:
        #
        # cleanup leftovers from previous runs
        #
        cmd = 'rm -rf %s' % work_dir
        logging.info(cmd)
        os.system(cmd)
    else:
        logging.error("work dir %s already exists." % work_dir)
        sys.exit(1)

kaldi_root = options.kaldi_root

#
# main
#

kaldi_adapt_lm (kaldi_root, src_model_dir, lm_fn, work_dir, dst_model_name)

logging.info ( "All done." )

