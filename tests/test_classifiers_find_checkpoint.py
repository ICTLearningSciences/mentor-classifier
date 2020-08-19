#
# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
#
import os

import pytest

from mentor_classifier.checkpoints import find_checkpoint
from .helpers import resource_root_checkpoints_for_test

CHECKPOINTS_ROOT = resource_root_checkpoints_for_test(__file__)


@pytest.mark.parametrize(
    "checkpoints_root,expected_checkpoint",
    [(CHECKPOINTS_ROOT, os.path.join("lstm_v1", "2019-11-06-2357"))],
)
def test_it_finds_the_newest_checkpoint_by_alpha(checkpoints_root, expected_checkpoint):
    expected_checkpoint_abs = os.path.abspath(
        os.path.join(checkpoints_root, expected_checkpoint)
    )
    actual_checkpoint = find_checkpoint(checkpoints_root)
    assert expected_checkpoint_abs == actual_checkpoint
