from abc import ABC, abstractmethod
from importlib import import_module


class ClassifierTraining(ABC):
    """
    Trains a classifier for a mentor
    """

    @abstractmethod
    def train(self):
        """
        Trains the classifier updating trained weights to be saved later with save()

        Returns:
            scores: (float array) cross validation scores for training data
            accuracy: (float) accuracy score for training data
        """
        pass

    @abstractmethod
    def save(self, to_path=None):
        pass


class ClassifierTrainingFactory(ABC):
    """
    A factory that creates a mentor_classifier.classifiers.Classifier given a checkpoint and mentor[s].
    Generally associated with a specific architecture, but not a specific checkpoint
    """

    @abstractmethod
    def create(self, checkpoint, mentors):
        """
        Creates a ClassifierTraining instance given a checkpoint and mentor[s]

        Args:
            checkpoint: (str) id for the checkpoint
            mentors: (str|mentor_classifier.mentor.Mentor|list of mentors/mentor ids) mentor[s] used in classifier

        Returns:
            classifierTraining: (mentor_classifier.classifiers.training.ClassifierTraining)
        """
        pass


_factories_by_arch = {}


def register_classifier_training_factory(arch, fac):
    """
        Register a mentor_classifier.classifiers.CheckpointClassifierFactory for an arch

        Args:
            arch: (str) id for the architecture
    """
    assert isinstance(arch, str)
    assert isinstance(fac, ClassifierTrainingFactory)
    _factories_by_arch[arch] = fac


def find_classifier_training_factory(arch):
    """
        Creates a mentor_classifier.classifiers.training.ClassifierTrainingFactory given an arch and checkpoint.

        Args:
            arch: (str) id for the architecture
            checkpoint: (str) id for the checkpoint

        Returns:
            classifier: (mentor_classifier.classifiers.ClassifierFactory)
    """
    assert isinstance(arch, str)
    if arch not in _factories_by_arch:
        import_module(f"mentor_classifier.classifiers.arch.{arch}.training")
    fac = _factories_by_arch[arch]
    assert isinstance(fac, ClassifierTrainingFactory)
    return fac
