*******************************************************************************
ABB fabrication runner
*******************************************************************************

.. note::
   Requires ``compas_rrc``. Follow the installation steps in :doc:`../getting_started`.

Requirements
============

* Virtual or real ABB controller with compas_rrc's rapid set up.
* Python ``>=3.7``
* Docker desktop
* ``abb-driver`` image from ``compas_rrc``

Fabrication data
================

Fabrication data is created in Grasshopper, see :doc:`./grasshopper-examples`.
The information is stored as a list of :obj:`compas_rcf.fab_data.ClayBullet`
dumped to a JSON file.

The JSON file can be edited from Grasshopper after initial creation.

Fabrication configuration
=========================

Fabrication configurations are stored as ``YAML`` files which allows for easy
editing.

.. literalinclude:: ../../src/compas_rcf/fab_data/config_default.yaml
   :language: yaml
   :caption: Default configuration

Fabrication run
===============

Run the script from a terminal using the command
:code:``python -m compas_rcf.abb.run``. There are some flags that can be set
when running this command:

.. code-block::

   $ python -m compas_rcf.abb.run --help
   usage: run.py [-h] [-t {real,virtual}] [-q] [--debug] [--skip-logfile]
              [--skip-progress-file]

   optional arguments:
     -h, --help            show this help message and exit
     -t {real,virtual}, --target {real,virtual}
                           Set fabrication runner target.
     -q, --quiet           Don't print logging messages to console.
     --debug               Log DEBUG level messages.
     --skip-logfile        Don't send log messages to file.
     --skip-progress-file  Skip writing progress to json during run.

Run setup
---------

Select target (real or virtual controller) and configuration file.

.. code-block::

   $ python -m compas_rcf.abb.run
   {{timestamp}}:INFO:<module>:compas_rcf version: {{version}}
   ? Load config or use default?  (Use arrow keys)
   » Default.
     Load.
   ? Load config or use default?  Default.
   {{timestamp}}:INFO:interactive_conf_setup:Default configuration loaded from package
   ? Target?  (Use arrow keys)
   » Virtual robot
     Real robot
   ? Target?  Virtual robot
   {{timestamp}}:INFO:interactive_conf_setup:Target is VIRTUAL controller.
   [...]


Next ``docker-compose up`` runs to make sure these three containers are running:

* ``ros-master``
* ``ros-bridge``
* ``abb-driver``

.. code-block::

   [...]
   ros-master-driver is up-to-date
   ros-bridge-driver is up-to-date
   abb-driver is up-to-date
   [...]


Next, select fabrication file using the open file dialog.

.. code-block::

   [...]
   {{timestamp}}:INFO:main:Fabrication data read from: {{path to json-file}}
   {{timestamp}}:INFO:main:x items in clay_bullets.
   [...]

Now the connection to ROS is set up, and the script tries to ping the
controller. If there is no response, the docker container ``abb-driver`` is
restarted. This is because of some issues with reconnecting with ROS to the
controller.

.. code-block::

   [...]
   {{timestamp}}:INFO:onOpen:Connection to ROS MASTER ready.
   {{timestamp}}:INFO:check_reconnect:No response from controller, restarting abb-driver service.
   Recreating abb-driver ... done
   [...]

After the connection is set up the fabrication data is checked for
``ClayBullets`` with the attribute ``placed``, if found the scripts
prompts the user if they want to skip ``ClayBullets``.

.. code-block::

   [...]
   ? Some or all bullet seems to have been placed already.  (Use arrow keys)
   » Skip all bullet marked as placed in JSON file.
     Place all anyways.
     ---------------
     Place some of the bullets.
   [...]

Finally, there is a last confirmation before the robot starts moving.

.. code-block::

   [...]
   ? Ready to start program?  (Y/n)
   [...]

During the run
--------------

The script then goes through the list and sends commands to pick and place
clay cylinders. There's timers set for the pick and place procedures which
is used to calculate cycle time for every bullet. This together with the time
of placement is stored in the ``ClayBullet`` in the attributes ``cycle_time`` and
``placed``.

The list of ``ClayBullets`` is continually written to a file in the
same directory as the original fabrication data file, but with "IN_PROGRESS"
prepended to the file name.

This is to record the cycle time and time of placement, but also to create a file
that an interrupted run can use as a start point. This makes resuming a
fabrication run after an interruption easy.

The progress of the fabrication run is printed in the terminal as well as on
the flexpendant:

.. code-block::

   [...]
   {{timestamp}}:INFO:main:Bullet 000/1827 with id 18280.
   [...]

End of run
-----------

.. code-block::

   [...]
   {{timestamp}}:INFO:main:Finished program with x bullets.

When all ``ClayBullets`` are placed the ``"IN-PROGRESS"`` file is moved to
``00_done``, in the same directory as the original fabrication file.
