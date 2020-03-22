# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## \[0.3.0\] \[2020-03-22\]

### Added

* More examples.

### Changed

* A lot of changes to package structure. Might be documented here more later.

## \[0.2.4\] \[2020-03-13\]

### Added

* Draft of grasshopper example showcasing robot control using `compas_rrc`.
* Command line argument to skip writing progress while running `compas_rcf.abb_runner`: `--skip-progress-file`.

### Changed

* Replaced `pathlib` with `os.path` in `compas_rcf.abb.connectivity` for Python 2 compatibility.
* `compas_rcf.abb_runner` now writes progress to json while waiting for robot, to make sure the robot isn't idle between loops.
* Some improvements to the `compas_rcf.utils.csv_reports` module, more data points and more informative headers.

## \[0.2.3\] \[2020-03-11\]

### Added

* `compas_rcf.abb.helpers.RapidToolData` now takes optional tolerance for tooldata values.
* `compas_rcf.docker.docker_cmds._run` is a new helper function for docker commands that works in both Python 2 and 3.
* `compose_up` has a new keyword `check_output` that toggles return code check of `subprocess` call.
* `compose_down` added to `compas_rcf.docker`

### Changed

* `base-docker-compose.yml` in `src/compas_rcf/docker/compose_files/abb` renamed to `master-bridge-docker-compose.yml`
* `dict` key `abb_driver` in `compas_rcf.abb.connectivity.DOCKER_COMPOSE_PATHS` renamed to `driver`.
* `env_vars` in `compas_rcf.abb.connectivity.connection_check` is now a stand alone keyword argument instead of being picked up from `**kwargs`.
* `RapidTooldata.from_plane_point` creates a `RapidTooldata` object without using `from_frame_point`.

## \[0.2.2\] \[2020-03-06\]

### Added

*   Class `compas_rcf.abb.helpers.RapidToolData` added to create Rapid tooldata from compas and Rhino geometries.
*   Class property `weight` added to `compas_rcf.fabrication.ClayBullet`.
*   MyPy configuration so Mypy can find imports when running from Vim + Ale. Libraries without typehints set to `ignore_missing_imports`.

### Changed

*   `compas_rcf.abb.helpers` split into `helpers` and `connectivity` make `helpers` importable from IronPython.
*   Robot instruction in `compas_rcf.abb.programs.pick_bullet` to go to picking_frame now specifies `zone_pick` instead of `zone_travel` to make sure that the tool actuators activate at the correct time.
*   Module `compas_rcf.utils.csv_reports` now adds more data from `ClayBullet` instances.
*   `compas_rcf.install_rhino`, `compas_rcf.utils.compas_to_rhino` and `compas_rcf.rhino_to_compas` now moved to new package `compas_rcf.rhino` to more clearly show where an environment with Rhino is necessary. `install_rhino` is however still available from `compas_rcf.install_rhino`.
*   Renamed `compas_rcf.utils.util_funcs.list_elem_w_index_wrap` to `wrap_list`.

## \[0.2.1\] \[2020-03-04\]

### Changed

*   `compas_rcf.fabrication.abb_runner` moved to `compas_rcf.abb_runner`.

## \[0.2.0\] \[2020-03-02\]

### Added

-   Prompt to confirm start of fabrication added to `compas_rcf.fabrication.abb_runner.abb_run`, replacing confirmation in `get_settings`.

### Changed

-   Docstring changes in `compas_rcf.utils.compas_to_rhino` and `rhino_to_compas`.
-   Redone the reference pages in the docs and fixed import problems.
-   Replaced usage of `AttrDict` from `confuse.Configuration` in `compas_rcf.fabrication.abb_runner` to use the original `confuse.Configuration` object. E.g. `fab_conf["target"].get()` instead of `fab_conf.target`. This is to make the use of the `Configuration` object uniform across modules.
-   `ZONE_DICT` moved from `compas_rcf.abb.helpers` to `compas_rcf.fabrication.conf`, mainly due to weird import errors.
-   `confuse.Template` object `confuse.Path` vendorised from upstream master and put in `compas_rcf.fabrication.conf`.
-   Renamed `logging` to `log` in `compas_rcf.fabrication.abb_runner` to make usage of the `logging` object uniform across modules.
-   Added logging to `compas_rcf.abb.helpers`, `compas_rcf.fabrication.conf`, `compas_rcf.abb.programs`,
-   Directories set up previously by globals in `compas_rcf.fabrication.abb_runner` is now accessible using the configuration file. The old globals are now the default value in the configuration.
-   Moved submodule `docker` from `compas_rcf.utils.docker` to `compas_rcf.docker` including its submodules and Docker-Compose files.
-   Refactored connection check from `compas_rcf.fabrication.abb_runner` to its own function: `compas_rcf.abb.helpers.connection_check`.
-   Refactored logging setup from `compas_rcf.fabrication.abb_runner.abb_runner` to it's own function: `compas_rcf.fabrication.abb_runner.logging_setup`.
-   Refactored fabrication data analysis and prompts for skipping or placing bullets in `compas_rcf.fabrication.abb_runner.abb_runner` to its own function: `compas_rcf.fabrication.abb_runner.setup_fab_data`.
-   Refactored `compas_rcf.fabrication.abb_runner.get_setup` to `compas_rcf.fabrication.conf.interactive_conf_setup`.
-   Moved `compas_rcf.fabrication.abb_runner.initial_setup` to: `compas_rcf.abb.programs.pre_procedure`.
-   Moved `compas_rcf.fabrication.abb_runner.shutdown_procedure` to: `compas_rcf.abb.programs.post_procedure`.
-   Moved `compas_rcf.fabrication.abb_runner.send_picking` to: `compas_rcf.abb.programs.pick_bullet`.
-   Moved `compas_rcf.fabrication.abb_runner.send_placing` to: `compas_rcf.abb.programs.place_bullet`.
-   Moved `compas_rcf.fabrication.abb_runner.send_grip_release` to: `compas_rcf.abb.programs.grip_and_release`.
-   Logging setup is now run in the `if __name__ = "__main__"` part of `compas_rcf.fabrication.abb_runner`.

### Removed

-   Prompt to confirm settings removed in `compas_rcf.fabrication.abb_runner.get_settings" in favour of a later confirmation of the whole setup in`abb\_run\`.

## \[0.1.22\] \[2020-02-28\]

### Added

-   Configuration option for timeout and wait times for docker commands in `compas_rcf.fabrication.runner`.

### Changed

-   Skip and/or place logic reworked in `compas_rcf.fabrication.abb_runner`.
-   `abb_runner` is now verbose by default, `--verbose` is removed in favour of `--quiet`.
-   Removed print statements from `abb_runner` and replaced them with `logging.info` calls.
-   Fixed `id` attribute logic and renamed it to `bullet_id`. classmethod `compas_rcf.fabrication.clay_objs.ClayBullet.from_data` is backwards compatible.

## \[0.1.21\] \[2020-02-26\]

### Changed

-   `compas_rcf.fabrication.abb_runner` now prints progress updates to Flex pendant.
-   `abb_runner` now dumps list of `ClayBullets` for every bullet into file with same filename as input JSON but with IN\_PROGRESS added to start.
-   `abb_runner` now checks if attribute `placed` is set on `ClayBullet` and if so asks user if it should be skipped or placed (with the option to set skip and place for all future bullets with `placed` attribute). This file is deleted when script exits cleanly.
-   `compas_rcf.utils.csv_` renamed to `csv_reports`. Instead of a conversion tool it now creates an opinionated report from JSON file. It can also handle directories and multiple files as inputs.

## \[0.1.20\] \[2020-02-25\]

### Added

-   Settings regarding picking grid added to `compas_rcf.fabrication.conf`.

### Changed

-   Function `get_picking_frame` in `compas_rcf.fabrication.abb_runner` reworked into `pick_frame_from_grid` which reads settings from conf to return frames from a grid of picking points.
-   JSON dump after end of `abb_runner` now dumps original list (`clay_bullets`) instead of a new.

## \[0.1.18\] \[2020-02-20\]

## \[0.1.19\] \[2020-20-22\]

### Changed

-   Reworded note in method `compas_rcf.utils.rhino_to_compas.rgplane_to_cgplane` to fix encoding error in Grasshopper.

## \[0.1.18\] \[2020-02-20\]

### Added

-   Dependency `prompt-toolkit` and `Pygments`.
-   Logging to `compas_rcf.utils.docker.docker_cmds`.
-   `compas_rcf.fabrication.abb_runner` now dumps placed `ClayBullets` after completed run, together with attribute `placed` with time of placement in UNIX epoch.
-   Functions `send_picking` & `send_placing` in `compas_rcf.fabrication.abb_runner` are now timed using Watch from compas\_rrc and the sum of their durations are stored as `ClayBullet.cycle_time`.
-   Added command line argument to `compas_rcf.fabrication.abb_runner`: `--skip-logfile`.
-   Module for converting JSON to CSV: `compas_rcf.utils.csv_`

### Changed

-   Replaced function `compas_rcf.utils.ui.print_conf_w_colors` with `pygment_yaml`, pretty printing yaml config using prompt\_toolkit and pygments.
-   Added check of Exception message in `compas_rcf.abb.helpers` to narrow error catching.
-   Paths in `compas_rcf.fabrication.abb_runner` are changed to be pathlib.Path objects.
-   Changed `compas_rcf.utils.rhino_to_compas.rgplane_to_cgframe` to correctly inherit X and Y axis from Rhino plane.
-   Added a note to `rgplane_to_cgplane` to clarify that X and Y axises are note stored in compas planes.

### Removed

-   Unused functions in `compas_rcf.utils.docker.docker_cmds`.

## \[0.1.17\] \[2020-02-18\]

### Added

-   Docker compose integration via `compas_rcf.utils.docker` to set up needed services for `compas_rcf.fabrication.abb_runner`.
-   Added ping function to `compas_rcf.abb.helpers`, sends NoOp to controller and waits for feedback.

### Changed

-   Reordered functions in `abb_runner` and added comments to section of the functions.

## \[0.1.16\] \[2020-02-18\]

### Changed

-   Grasshopper example file `create_bullets_read_write_json` updated to handle Grasshopper trees and take vkeys as an attribute.
-   `compas_rcf.fabrication.clay_obj.ClayBullet` property setter `trajectory_to` and `trajectory_from` updated to handle list of planes.
-   `compas_rcf.utils.util_funcs.ensure_frame` updated to convert point to Frame with given point and flipped XY plane.
-   Updated config for black to also target py2.7 so it doesn't add trailing commas to lists. (Which IronPy 2.7 can't handle)

## \[0.1.15\] \[2020-02-15\]

### Added

-   Attribute dictionary added to class `compas_rcf.fabrication.clay_obj.ClayBullet`
-   Attribute `vkey` added to `ClayBullet` to store vertex key from `compas.datastructures.Network`
-   Simple import tests added

### Changed

-   Property `Vector` in `ClayBullet` changed to represent the bullets center as a line.

## \[0.1.14\] \[2020-02-14\]

### Added

-   API docs. Some modules have issues but a lot of them works.

### Changed

-   More fixes of imports.
-   Split of Rhino dependent functions from `compas_rcf.utils.util_funcs` to `compas_rcf.utils.util_funcs_rhino`.

## \[0.1.13\] \[2020-02-14\]

### Added

-   Properties `centroid_frame`, `compressed_centroid_frame`, `centroid_plane` added `compressed_centroid_plane` to `compas_rcf.fabrication.clay_objs.ClayBullet`.
-   Classmethod `from_compressed_centroid_frame_like` added to `ClayBullet`.

### Changed

-   `compas_rcf.fabrication.abb_rcf_runner` renamed to `compas_rcf.fabrication.abb_runner`.
-   Typos in `abb_runner` fixed.
-   Trying to set up imports better between modules
-   Fixes for tkinter file dialog in `compas_rcf.utils.ui`.
-   Property `post_planes` renamed to `trajectory_from` in `ClayBullet`.

## \[0.1.12\] \[2020-02-13\]

### Added

-   Logging added to `compas_rcf.fabrication.abb_rcf_runner`.
-   Makes sure needles are retracted at start and end of `abb_rcf_runner`.
-   Hardcoded compression at pickup in `abb_rcf_runner`. Needs to be removed.
-   Added note about compas to `README.md`
-   Added note about compatibility with Python 2 and \< 3.6.

### Changed

-   Whole package has had its imports sorted
-   Set up black formatting and formatted everything
-   Travis now handles build and releasing of tagged commit, using `setuptools_scm` to handle version setup.
-   `setuptools_scm` replaces `MANIFEST.in` in handling what to include when building.
-   Package now requires Python \>= 3.6 for installation.

### Removed

-   Lots of dev deps

## \[0.1.10\] \[2020-02-11\]

### Added

-   Module `compas_rcf.fabrication.conf` added. Reads yaml files for fabrication settings. Provides template to validate files.
-   Package `confuse` new dependecy, ("painless YAML config files for Python")
-   Default config file (in YAML) added to `compas_rcf.fabrication`
-   Module `compas_rcf.abb.helpers` added, for now only a dict mapping Zone data names to absolute value

### Changed

-   `compas_rcf.fabrication.abb_rcf_runner` updated to use YAML configs.
-   docker compose dirs moved from `./docker` to `.data/docker-compose`

### Removed

-   Hard-coded fabrication configuration removed from `compas_rcf.fabrication.abb_rcf_runner`. Default values now stored in `compas_rcf.fabrication.default_config.yaml`

## \[0.1.9\] \[2020-02-09\]

### Added

-   Print colored dict function added to `compas_rcf.utils.ui`.
-   Packages Colorama and Questionary added to to requirements. They are used for CLI runner.

### Changed

-   `compas_rcf.fabrication.abb_fabrication_non_interactive` refactored
-   `compas_rcf.fabrication.abb_fabrication_non_interactive` renamed to `abb_rcf_runner`.
-   `compas_rcf.fabrication.abb_rcf_runner` now takes args and can edit conf setup during runtime.
-   `compas.rcf.fabrication.ClayBullet` property `placement_frame` changed to be where the tool should stop while placing. New property `location` is the new required argument for the object and defines the clay bullets lowest point. `placement_frame` is derived from `location` and `compressed height`.
-   `ClayBulley` attributes `pre_frames` and `post_frames` renamed to `trajectory_to` and `trajectory_from` to be more descriptive.
-   Fixes to docs: In Updating section of `getting_started.rst` python was changed to pip. Inline comments removed from installation instructions.

## \[0.1.8\] \[2020-02-07\]

### Changed

-   After some testing to find the best way to distribute this package given the dependency on private repository `compas_rrc` I've concluded to keep uploading to PyPi. This means that compas\_rrc will need to be installed manually before this package, since PyPi does not allow giving a \"direct dependency\`.

## \[0.1.6\] 2020-02-06

### Added

-   Set up sphinx docs
-   Added deploy job for travis
-   Open file dialog function added to new module `compas_rcf.util.ui`
-   Open file dialog implemented in ABB fabrication runner

### Changed

-   Travis Python 3 version bumped up to 3.7
-   docs moved from docsource to docs
-   sphinx target directory now dist/docs
-   Corrected compas\_fab version range (from `<0.12` to `<0.11`)
-   Fixed compas\_rrc requirement syntax given it's installed from git repository
-   Added compas\_rrc to installable packages for `compas_rcf.install_rhino`

## \[0.1.5\] 2020-02-05

### Added

-   `ClayBulletEncoder` to serialize `ClayBullet` added to `compas_rcf.fabrication.clay_obj`
-   Frames before and after placement added to `ClayBullet`
-   `from_data` constructor added to `ClayBullet`
-   Function to parse list of ClayBullet instances from JSON added in new module `compas_rcf.utils.json_`
-   `ensure_frame` function added to `compas_rcf.utils.util_funcs` to convert `Planes` to `Frames`
-   `compas_rcf.IPY` global boolean that uses `compas` function to check if IronPython is running the code.

### Changed

-   `Rhino` modules are only loaded if IronPython is running the code
-   `compas_rcf.fabrication.abb_fabrication_non_interactive` now reads JSON to load ClayBullets and extracts `Frames` from them
-   Most settings in `abb_fabrication_non_interactive` are moved to top and set as globals.

### Removed

-   `compas_rcf.utils.databases` mock module removed in favor of `json_`.

## \[0.1.4\] 2020-02-05

### Added

-   Added abb non-interactive fabrication script
-   Added docker-compose files for ABB ROS setup

## \[0.1.3\] 2020-02-04

### Added

-   Example file `grasshopper_non_interactive` setup in docs
-   Partly finished structure for future ur online fabrication procedure

### Changed

-   `utils.py` now divided into multiple modules
-   Other renames and moves

### Removed

## \[0.1.2\] 2020-02-03

### Changed

-   Name change from `rcf` to `compas_rcf`.

## \[0.1.1\] 2020-02-03

### Added

-   First release, package setup by applying [compas-dev/cookiecutter-pypackage](https://github.com/compas-dev/cookiecutter-pypackage) on small library of modules from previous phase of project

### Changed

-   `rcf/ur` renamed to `rcf/ur_control`
-   Fabrication related functions moved from `rcf/ur` to `rcf/fabrication`

### Removed

-   Unused code in `rcf/ur_control`

## \[0.1.0\]

-   Start value for version
