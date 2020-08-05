# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
import os

from gensim.models.keyedvectors import KeyedVectors
import numpy as np


class W2V(object):
    def __init__(self, w2v_file_name="GoogleNews-vectors-negative300-SLIM.bin"):
        self.__w2v_file_name = w2v_file_name
        self.__w2v_path = os.path.join(
            "checkpoint", "vector_models", self.__w2v_file_name
        )
        self.__w2v_model = KeyedVectors.load_word2vec_format(
            self.__w2v_path, binary=True
        )

    def get_w2v_file_name(self):
        return self.__w2v_file_name

    def w2v_for_question(self, question):
        current_vector = np.zeros(300, dtype="float32")
        lstm_vector = []
        for word in question:
            try:
                word_vector = self.__w2v_model[word]
            except BaseException:
                word_vector = np.zeros(300, dtype="float32")
            lstm_vector.append(word_vector)
            current_vector += word_vector
        return current_vector, lstm_vector
