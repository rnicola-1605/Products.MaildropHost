#!/usr/bin/env python
##############################################################################
#
# Copyright (c) 2004-2009 Jens Vagelpohl and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" make_emails: Generate fake email files for maildrop testing

$Id: make_emails.py 1696 2009-02-08 08:22:06Z jens $
"""

#####################################################################
# EDIT THESE VARIABLES
#####################################################################

# UNLOCKED_EMAILS - The number of unlocked email files to generate
UNLOCKED_EMAILS = 10

# LOCKED_EMAILS - The number of locked email files to generate.
LOCKED_EMAILS = 2

# RECIPIENTS - The list of email recipient addresses to be used
RECIPIENTS = [ 'root@localhost' ]

# SENDER - Who these emails appear to originate from
SENDER = 'root@localhost'

#####################################################################
# NO EDITING BELOW HERE
#####################################################################

MAIL_TEMPLATE = """\
##To:%(recipient)s
##From:%(sender)s
From: "Maildrop Testing" <%(sender)s>
To: "Unlucky Recipient" <%(recipient)s>
Subject: %(subject)s

Sent by the maildrop testing script
"""

import os
import random

from config import MAILDROP_HOME
try:
    from config import MAILDROP_SPOOL
    MAILDROP_SPOOLS = tuple([x.strip() for x in MAILDROP_SPOOL.split(';')])
except:
    MAILDROP_SPOOLS = (os.path.join(MAILDROP_HOME, 'spool'),)

for spool in MAILDROP_SPOOLS:
    if not os.path.isdir(spool):
        os.makedirs(spool)

def create_emails():
    """ Create the test emails """
    pathjoin = os.path.join
    all_files = []

    for spool in MAILDROP_SPOOLS:
        all_files.extend([os.path.join(spool, x) for x in os.listdir(spool)])

    for old_file in all_files:
        if old_file.find('unlocked_') != -1:
            os.remove(pathjoin(spool, old_file))

    for i in range(UNLOCKED_EMAILS):
        spool = random.choice(MAILDROP_SPOOLS)
        f = open(pathjoin(spool, 'unlocked_%d' % i), 'w')
        f.write(MAIL_TEMPLATE % { 'recipient' : random.choice(RECIPIENTS)
                                , 'sender'    : SENDER
                                , 'subject'   : 'unlocked email'
                                } )
        f.close()

    for i in range(LOCKED_EMAILS):
        spool = random.choice(MAILDROP_SPOOLS)
        filename = 'locked_%d' % i
        lockname = '%s.lck' % filename
        l = open(pathjoin(spool, lockname), 'w')
        l.write('locked')
        l.close()
        f = open(pathjoin(spool, 'locked_%d' % i), 'w')
        f.write(MAIL_TEMPLATE % { 'recipient' : random.choice(RECIPIENTS)
                                , 'sender'    : SENDER
                                , 'subject'   : '***LOCKED***'
                                } )
        f.close()


if __name__ == '__main__':
    create_emails()

