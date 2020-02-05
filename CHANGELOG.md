# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.4] 2020-02-05

### Added

* Added abb non-interactive fabrication script
* Added docker-compose files for ABB ROS setup

## [0.1.3] 2020-02-04

### Added
* Example file `grasshopper_non_interactive` setup in docs
* Partly finished structure for future ur online fabrication procedure

### Changed
* `utils.py` now divided into multiple modules
* Other renames and moves

### Removed


## [0.1.2] 2020-02-03

### Changed
* Name change from `rcf` to `compas_rcf`.

## [0.1.1] 2020-02-03

### Added
* First release, package setup by applying [compas-dev/cookiecutter-pypackage](https://github.com/compas-dev/cookiecutter-pypackage) on small library of modules from previous phase of project

### Changed
* `rcf/ur` renamed to `rcf/ur_control`
* Fabrication related functions moved from `rcf/ur` to `rcf/fabrication`

### Removed
* Unused code in `rcf/ur_control`

## [0.1.0]

* Start value for version
