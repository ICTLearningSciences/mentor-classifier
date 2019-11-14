import os
import numpy as np

from tensorflow.keras.models import load_model
from sklearn.externals import joblib
from tensorflow.keras.preprocessing.sequence import pad_sequences

from mentorpal.classifiers import (
    CheckpointClassifierFactory,
    Classifier,
    register_classifier_factory,
)
from mentorpal.mentor import Mentor
from mentorpal.nltk_preprocessor import NLTKPreprocessor
from mentorpal.w2v import W2V
from mentorpal.utils import sanitize_string

# store the ARCH because we use it several places
ARCH = "lstm_v1"


# NOTE: classifiers MUST extend abstract base class `mentorpal.classifiers.Classifier`
class LSTMClassifier(Classifier):
    """
    Create a classifier instance for a mentor

    Args:
        mentor: (str|Mentor)
            A mentor instance or the id for a mentor to load
        data_path: (str)
            path to the root of model data for this classifier
    """

    @staticmethod
    def get_classifier_arch():
        global ARCH
        return ARCH

    def __init__(self, mentor, data_path):
        if isinstance(mentor, str):
            print("loading mentor id {}...".format(mentor))
            mentor = Mentor(mentor)
        assert isinstance(
            mentor, Mentor
        ), "invalid type for mentor (expected mentor.Mentor or string id for a mentor, encountered {}".format(
            type(mentor)
        )
        self.mentor = mentor
        self.__model_path = os.path.join(data_path, mentor.get_id())
        self.name = ARCH
        self.logistic_model, self.topic_model, self.w2v_model = self.__load_model(
            self.get_model_path()
        )

    def get_answer(self, question, canned_question_match_disabled=False):
        if not canned_question_match_disabled:
            sanitized_question = sanitize_string(question)
            if sanitized_question in self.mentor.question_ids:
                answer_id = self.mentor.question_ids[sanitized_question]
                answer_question = self.mentor.ids_answers[answer_id]
                return answer_id, answer_question, 1.0
        preprocessor = NLTKPreprocessor()
        processed_question = preprocessor.transform(question)
        w2v_vector, lstm_vector = self.w2v_model.w2v_for_question(processed_question)
        padded_vector = pad_sequences(
            [lstm_vector],
            maxlen=25,
            dtype="float32",
            padding="post",
            truncating="post",
            value=0.0,
        )
        topic_vector = self.__get_topic_vector(padded_vector)
        predicted_answer = self.__get_prediction(w2v_vector, topic_vector)
        return predicted_answer

    def get_arch(self):
        return self.name

    def get_classifier_id(self):
        return self.get_model_path()

    def get_model_path(self):
        return self.__model_path

    def __load_model(self, model_path):
        logistic_model = None
        topic_model = None
        word2vec = None
        print("loading model from path {}...".format(model_path))
        if not os.path.exists(model_path) or not os.listdir(model_path):
            print("Local checkpoint {0} does not exist.".format(model_path))
        try:
            path = os.path.join(model_path, "lstm_topic_model.h5")
            topic_model = load_model(path)
        except BaseException:
            print(
                "Unable to load topic model from {0}. Classifier needs to be retrained before asking questions.".format(
                    path
                )
            )
        try:
            path = os.path.join(model_path, "fused_model.pkl")
            logistic_model = joblib.load(path)
        except BaseException:
            print(
                "Unable to load logistic model from {0}. Classifier needs to be retrained before asking questions.".format(
                    path
                )
            )
        word2vec = W2V()
        return logistic_model, topic_model, word2vec

    def __get_topic_vector(self, lstm_vector):
        model_path = self.get_model_path()
        if self.topic_model is None:
            try:
                self.topic_model = load_model(
                    os.path.join(model_path, "lstm_topic_model.h5")
                )
            except BaseException:
                raise Exception(
                    "Could not find topic model under {0}. Please train classifier first.".format(
                        model_path
                    )
                )

        predicted_vector = self.topic_model.predict(lstm_vector)
        return predicted_vector[0]

    def __get_prediction(self, w2v_vector, topic_vector):
        model_path = self.get_model_path()
        if self.logistic_model is None:
            try:
                self.logistic_model = joblib.load(
                    os.path.join(model_path, "fused_model.pkl")
                )
            except BaseException:
                raise Exception(
                    "Could not find logistic model under {0}. Please train classifier first.".format(
                        model_path
                    )
                )
        test_vector = np.concatenate((w2v_vector, topic_vector))
        test_vector = test_vector.reshape(1, -1)
        prediction = self.logistic_model.predict(test_vector)
        decision = self.logistic_model.decision_function(test_vector)
        confidence_scorces = (
            sorted(decision[0]) if decision.ndim >= 2 else sorted(decision)
        )
        highest_confidence = confidence_scorces[-1]
        if highest_confidence < -0.88:
            return "_OFF_TOPIC_", "_OFF_TOPIC_", highest_confidence
        if not len(prediction) >= 1 and prediction[0]:
            raise Exception(
                f"Prediction should be a list with at least one element (answer text) but found {prediction}"
            )
        answer_text = prediction[0]
        answer_id = self.mentor.find_id_for_answer_text(answer_text)
        if not answer_id:
            raise Exception(
                f"No answer id found for answer text (classifier_data may be out of sync with trained model): {answer_text}"
            )
        return self.mentor.answer_ids[prediction[0]], prediction[0], highest_confidence


# CheckpointClassifierFactory impl that will get registered globally for this arch ('lstm_v1')
class __ClassifierFactory(CheckpointClassifierFactory):
    def create(self, checkpoint, mentors):
        return LSTMClassifier(mentors, checkpoint)


# NOTE: always make sure this module lives in `mentorpal.classifiers.arch.${ARCH}`
# so that it can be discovered/loaded by arch name
register_classifier_factory(ARCH, __ClassifierFactory())
