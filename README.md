# cloudpoint_cli

_A Command Line Interface for Veritas CloudPoint_

It makes two assumptions:


* You have installed Veritas CloudPoint
* You're using bash as your shell (**_for command completion only_**)

Installation
-------------

```./setup.sh ```

> After setup completes, refresh your bash environment (start a new shell)

Usage/Examples
-------------

**For running any commands with the CLI, you first need to _authenticate_ with CloudPoint**

**```cloudpoint authenticate```**

Once authenticated, you can run all the other commands.

* Getting Reports          : `cloudpoint reports show`
* Create Roles             : ```cloudpoint roles create```
* Getting help on commands : ```cloudpoint -h``` OR ```cloudpoint --help```
* You can also get help on sub-commands : ```cloudpoint licenses -h```


Python Support
--------------
**cloudpoint_cli** requires Python3.3+

Common Problems
---------------
If command completion is not working after running the setup script, start a new session.

License
-------
Licensed under the terms of the [MIT LICENSE](https://opensource.org/licenses/MIT)
