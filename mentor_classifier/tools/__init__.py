# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
import logging
import os

CHECKPOINT_ROOT_DEFAULT = "/app/checkpoint"
ARCH_DEFAULT = "lstm_v1"


def find_checkpoint(
    checkpoint_root: str = CHECKPOINT_ROOT_DEFAULT,
    arch: str = ARCH_DEFAULT,
    checkpoint: str = None,
) -> str:
    all_archs_root = (
        os.path.join(checkpoint_root, "classifiers")
        if os.path.isdir(os.path.join(checkpoint_root, "classifiers"))
        else checkpoint_root
    )
    arch_root = os.path.abspath(os.path.join(all_archs_root, arch))
    if not os.path.isdir(arch_root):
        logging.warning(f"find_checkpoint with non-existent root {arch_root}")
        return None
    if not checkpoint:
        all = sorted(
            [
                c
                for c in os.listdir(arch_root)
                if os.path.isdir(os.path.join(arch_root, c))
            ]
        )
        return os.path.join(arch_root, all[-1]) if len(all) >= 1 else None
    cp = os.path.join(arch_root, checkpoint)
    if not os.path.isdir(cp):
        logging.warning(f"find_checkpoint but checkpoint does not exist {cp}")
        return None
    return cp
