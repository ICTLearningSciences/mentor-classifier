# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
import os
import csv
from datetime import datetime


class Logger(object):
    "New Class with static methods to log data through Python, specifically for the web version"

    def __init__(self):
        print("Logger")

    @staticmethod
    def logUserID(ID, uID):
        if not os.path.isfile("QuestionAnswerLog.csv"):
            with open("QuestionAnswerLog.csv", "a", newline="") as log:
                logWriter = csv.writer(log, delimiter=",", quotechar='"')
                logWriter.writerow(
                    [
                        "UserID",
                        "SessionID",
                        "MentorID",
                        "Question",
                        "NPC Answer",
                        "Classifier Answer",
                        "Final Chosen Answer",
                        "Final Video ID",
                        "NPC Editor Confidence",
                        "Classifier Confidence",
                        "Time",
                    ]
                )
        with open("QuestionAnswerLog.csv", "a", newline="") as log:
            logWriter = csv.writer(
                log,
                delimiter=",",
                quotechar="|",
                quoting=csv.QUOTE_MINIMAL,
                lineterminator=",",
            )  # this keeps the rest open for
            logWriter.writerow([ID, uID])

    @staticmethod
    def logData(
        mentor,
        question,
        answerNPC,
        answerClassifier,
        finalAnswer,
        videoID,
        npcConfidence,
        classifierConfidence,
    ):
        with open("QuestionAnswerLog.csv", "a", newline="") as log:
            logWriter = csv.writer(log, delimiter=",", quotechar='"')
            logWriter.writerow(
                [
                    mentor.id,
                    question,
                    answerNPC,
                    answerClassifier,
                    finalAnswer,
                    videoID,
                    npcConfidence,
                    classifierConfidence,
                    datetime.now(),
                ]
            )
