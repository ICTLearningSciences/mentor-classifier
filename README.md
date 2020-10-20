mentor-classifiers
==================

Usage
-----

This image is most often used to train, test, and run inference for mentor classifiers.

TODO: migrate checkpoint train/test scripts to this repo in a way that they're still
easy to run from a website project.

Development
-----------

#### Required Software

- make
- git + git lfs
- pyenv (if you have pyenv installed will help ensure the correct python version)

#### Tests

Any changes made to this repo should be covered by tests. To run the existing tests:

```
make test
```

All pushed commits must also pass format and lint checks. To check all required tests before a commit:

```
make test-all
```

To fix formatting issues:

```
make format
```

Releases
--------

Currently, this image is semantically versioned. When making changes that you want to test in another project, create a branch and PR and then you can release a test tag one of two ways:

To build/push a work-in-progress tag of `mentor-classifier` for the current commit in your branch

- find the `docker_tag_commit` workflow for your commit in [circleci](https://circleci.com/gh/ICTLearningSciences/workflows/mentor-classifier)
- approve the workflow
- this will create a tag like `https://hub.docker.com/mentor-classifier:${COMMIT_SHA}`

To build/push a pre-release semver tag of `mentor-classifier` for the current commit in your branch

- create a [github release](https://github.com/ICTLearningSciences/mentor-classifier/releases/new) **from your development branch** with tag format `/^\d+\.\d+\.\d+(-[a-z\d\-.]+)?$/` (e.g. `1.0.0-alpha.1`)
- find the `docker_tag_release` workflow for your git tag in [circleci](https://circleci.com/gh/ICTLearningSciences/workflows/mentor-classifier)
- approve the workflow
- this will create a tag like `uscictdocker/mentor-classifier:1.0.0-alpha.1`



Once your changes are approved and merged to master, you should create a release tag in semver format as follows:

- create a [github release](https://github.com/ICTLearningSciences/mentor-classifier/releases/new) **from master** with tag format `/^\d+\.\d+\.\d$/` (e.g. `1.0.0`)
- find the `docker_tag_release` workflow for your git tag in [circleci](https://circleci.com/gh/ICTLearningSciences/workflows/mentor-classifier)
- approve the workflow
- this will create a tag like `uscictdocker/mentor-classifier:1.0.0`