# ![Numenta Logo](http://numenta.org/images/numenta-icon128.png) NuPIC Studio

## NuPIC Studio [![Build Status](https://travis-ci.org/numenta/nupic.studio.png?branch=master)](https://travis-ci.org/numenta/nupic.studio)

NuPIC Studio is a virtual studio that allows developers to create, debug, and visualize HTM networks from NuPIC library. Some of its advantages:
 * Users can open, save, or change their "HTM projects" or of other developers. A typical project contains data to be trained, neural network configuration, statistics, etc, which can be shared to be analysed or integrated with other projects.
 * Users can create their own encoders and sensors to feed the HTM network.
 * Any changes in the nupic source can be immediatedly viewed. This helps users that wish test improvements like hierarchy, attention, and motor integration.

For more information, see [numenta.org](http://numenta.org) or the [NuPIC Studio wiki](https://github.com/numenta/nupic.studio/wiki).

## Installation

Currently supported platforms:

 * Linux (32/64bit)
 * Mac OSX

Dependencies:

 * Python (2.7 or later)
 * PIP
 * Nupic
 * PyQt4

For install PyQt4

 * On RedHat based systems (Fedora, Mandriva, …) run:


    yum install PyQt4

 * On Debian based systems (Ubuntu, Mint, …) run:


    apt-get install python-qt4

_Note_: If you get a "permission denied" error when using these commands, you can run them with 'sudo'.

## User instructions

If you want only use it, simply do this:

    pip install nustudio

_Note_: If you get a "permission denied" error when using pip, you may add the --user flag to install to a location in your home directory, which should resolve any permissions issues. Doing this, you may need to add this location to your PATH and PYTHONPATH. Alternatively, you can run pip with 'sudo'.

Once it is installed, you can execute the app using:

    nustudio

and then click on `Open Project` button to open any example to getting started with NuPIC.

## Developer instructions

If you want develop, debug, or simply test NuPIC Studio, clone it and follow the instructions:

### Using command line

> This assumes the `NUPIC_STUDIO` environment variable is set to the directory where the NuPIC Studio source code exists.

    cd $NUPIC_STUDIO
    python setup.py build
    python setup.py develop

### Using an IDE

The following instructions will work in the most Python IDEs:

 * Open your IDE.
 * Open a project specifying the `$NUPIC_STUDIO` repository folder as location.
 * Click with mouse right button on `setup.py` file listed on project files and select `Run` command on pop-up menu. This will call the build process. Check `output` panel to see the result.
 * If the build was successful, just click on `program.py` and voilà!

If you don't have a favourite Python IDE, this article can help you to choose one: http://pedrokroger.net/choosing-best-python-ide/
