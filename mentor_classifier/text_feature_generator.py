#
# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
#
import re
import numpy as np

"""
This class contains the methods that operate on the questions to generate text features that can help the classifier make better decisions.
"""


class TextFeatureGenerator(object):
    def __init__(self):
        pass

    def any_negation(self, question_text):
        for word in question_text.lower().split():
            if word in ["n", "no", "non", "not"] or re.search(r"\wn't", word):
                return 1
        return 0

    def log_wordcount(self, question_text):
        wordcount = len(question_text.split())
        return np.log(1 + wordcount)

    def negation_mod(self, question_text):
        count = 0
        for word in question_text.lower().split():
            if word in ["n", "no", "non", "not"] or re.search(r"\wn't", word):
                count = count + 1
        return count % 2

    def what_question(self, question_text):
        if "what" in question_text.lower().split():
            return 1
        return 0

    def how_question(self, question_text):
        if "how" in question_text.lower().split():
            return 1
        return 0

    def why_question(self, question_text):
        if "why" in question_text.lower().split():
            return 1
        return 0

    def when_question(self, question_text):
        if "when" in question_text.lower().split():
            return 1
        return 0

    def where_question(self, question_text):
        if "where" in question_text.lower().split():
            return 1
        return 0
