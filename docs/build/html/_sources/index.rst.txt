Generate GoogleTest/GoogleMock Test Suites for C++ Interfaces
--------------------------------------------------------------

**gen_test** is a toolset for automatic generation of GoogleTest and GoogleMock test suites from C++ pure virtual interface headers.

Developed in `python <https://www.python.org/>`_ code.

The README is used to introduce the tool and provide instructions on
how to install the tool, any machine dependencies it may have and any
other information that should be provided before the tool is installed.

|gen_test python checker| |gen_test python package| |gen_test interface checker| |gen_test isp checker| |gen_test srp checker| |github issues| |documentation status| |github contributors|

.. |gen_test python checker| image:: https://github.com/vroncevic/gen_test/actions/workflows/gen_test_python_checker.yml/badge.svg
   :target: https://github.com/vroncevic/gen_test/actions/workflows/gen_test_python_checker.yml

.. |gen_test python package| image:: https://github.com/vroncevic/gen_test/actions/workflows/gen_test_package_checker.yml/badge.svg
   :target: https://github.com/vroncevic/gen_test/actions/workflows/gen_test_package.yml

.. |gen_test interface checker| image:: https://github.com/vroncevic/gen_test/actions/workflows/gen_test_interface_checker.yml/badge.svg
   :target: https://github.com/vroncevic/gen_test/actions/workflows/gen_test_interface_checker.yml

.. |gen_test isp checker| image:: https://github.com/vroncevic/gen_test/actions/workflows/gen_test_isp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/gen_test/actions/workflows/gen_test_isp_checker.yml

.. |gen_test srp checker| image:: https://github.com/vroncevic/gen_test/actions/workflows/gen_test_srp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/gen_test/actions/workflows/gen_test_srp_checker.yml

.. |github issues| image:: https://img.shields.io/github/issues/vroncevic/gen_test.svg
   :target: https://github.com/vroncevic/gen_test/issues

.. |github contributors| image:: https://img.shields.io/github/contributors/vroncevic/gen_test.svg
   :target: https://github.com/vroncevic/gen_test/graphs/contributors

.. |documentation status| image:: https://readthedocs.org/projects/gen_test/badge/?version=latest
   :target: https://gen_test.readthedocs.io/en/latest/?badge=latest

.. toctree::
   :maxdepth: 4
   :caption: Contents

   self
   modules

🚀 Installation
---------------

|gen_test python3 build|

.. |gen_test python3 build| image:: https://github.com/vroncevic/gen_test/actions/workflows/gen_test_python3_build.yml/badge.svg
   :target: https://github.com/vroncevic/gen_test/actions/workflows/gen_test_python3_build.yml

Navigate to release `page`_ download and extract release archive.

.. _page: https://github.com/vroncevic/gen_test/releases

To install **gen_test** type the following

.. code-block:: bash

    tar xvzf gen_test-x.y.z.tar.gz
    cd gen_test-x.y.z/
    # python3
    wget https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py 
    python3 -m pip install --upgrade setuptools
    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade build
    pip3 install -r requirements.txt
    python3 -m build --no-isolation --wheel
    pip3 install ./dist/gen_test-*-py3-none-any.whl
    rm -f get-pip.py

You can use Docker to create image/container, or You can use pip to install

.. code-block:: bash

    # python3
    pip3 install gen_test

📦 Dependencies
---------------

**gen_test** requires next modules and libraries

* `ats-utilities - Python App/Tool/Script Utilities <https://pypi.org/project/ats-utilities/>`_

📁 Tool structure
-----------------

**gen_test** is based on OOP.

Tool structure

.. code-block:: bash

    gen_test/
         ├── core/
         │   ├── __init__.py
         │   ├── model/
         │   │   ├── cpp_interface.py
         │   │   ├── cpp_method.py
         │   │   ├── generation_result.py
         │   │   ├── __init__.py
         │   │   └── test_suite_config.py
         │   └── service/
         │       ├── engine.py
         │       ├── icmake_generator.py
         │       ├── icpp_parser.py
         │       ├── ifake_generator.py
         │       ├── imock_generator.py
         │       ├── __init__.py
         │       ├── iservice.py
         │       ├── isubprocessor.py
         │       └── itest_generator.py
         ├── engine.py
         ├── infrastructure/
         │   ├── cli/
         │   │   ├── engine.py
         │   │   ├── icli.py
         │   │   ├── __init__.py
         │   │   └── setup/
         │   │       ├── bundle.py
         │   │       ├── dep_validator.py
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       ├── keys.py
         │   │       ├── opt_validator.py
         │   │       ├── options.py
         │   │       ├── registry.py
         │   │       └── validator.py
         │   ├── command/
         │   │   ├── cmake_command_definition.py
         │   │   ├── cmake_command_executor.py
         │   │   ├── command.py
         │   │   ├── fake_command_definition.py
         │   │   ├── fake_command_executor.py
         │   │   ├── icommand_definition.py
         │   │   ├── icommand_executor.py
         │   │   ├── __init__.py
         │   │   ├── mock_command_definition.py
         │   │   ├── mock_command_executor.py
         │   │   ├── suite_command_definition.py
         │   │   ├── suite_command_executor.py
         │   │   ├── test_command_definition.py
         │   │   └── test_command_executor.py
         │   ├── config/
         │   │   ├── gen_test.cfg
         │   │   ├── gen_test.logo
         │   │   ├── scheme.json
         │   │   └── templates.tgz
         │   ├── generator/
         │   │   ├── cmake_generator.py
         │   │   ├── code_formatter.py
         │   │   ├── fake_generator.py
         │   │   ├── __init__.py
         │   │   ├── main_generator.py
         │   │   ├── mock_generator.py
         │   │   ├── template_provider.py
         │   │   └── test_generator.py
         │   ├── __init__.py
         │   ├── parser/
         │   │   ├── cpp_parser.py
         │   │   └── __init__.py
         │   ├── subprocessor.py
         │   └── templates/
         │       ├── cmake.template
         │       ├── fake.template
         │       ├── main.template
         │       ├── mock.template
         │       └── test.template
         ├── __init__.py
         ├── py.typed
         └── setup/
             ├── bundle.py
             ├── dep_validator.py
             ├── dependencies.py
             ├── factory.py
             ├── __init__.py
             ├── keys.py
             ├── opt_validator.py
             ├── options.py
             ├── registry.py
             └── validator.py

     13 directories, 76 files

✨ Features
-----------

* Parses C++ pure virtual interface header files (`.h` / `.hpp`).
* Synthesizes modern GoogleMock header mocks using `MOCK_METHOD(...)` with `#pragma once`.
* Generates unit test suites (`<interface>_test.cc`), in-memory fake stubs (`fake_<interface>.h`), and test runners (`test_main.cc`).
* Generates standalone `CMakeLists.txt` build scripts integrated with GoogleTest and GoogleMock.
* Configurable template engine structured in `templates.tgz` with `scheme.json` schema validation.
* Provides a modular and extensible architecture based on OOP, SOLID, and Hexagonal principles.
* Includes command line interface (CLI) support via a command/executor structure.
* High code quality with full type checking and 100% unit test coverage.

📊 Code coverage
----------------

.. csv-table:: Code coverage
   :file: coverage_table.csv
   :widths: 60, 10, 10, 20
   :header-rows: 1

🛠 Usage
--------

Install package

.. code-block:: bash

    pip3 install gen_test

Prepare main entry point by downloading `main.py` or create your own.

.. code-block:: bash

    wget -O main.py https://raw.githubusercontent.com/vroncevic/gen_test/main/main.py

Running tool for generating complete GoogleTest suite:

.. code-block:: bash

    python3 main.py suite --interface include/ISerialPort.h --output ./tests --prefix comm

Running tool for generating individual components:

.. code-block:: bash

    python3 main.py mock --interface include/ISerialPort.h --output ./tests
    python3 main.py test --interface include/ISerialPort.h --output ./tests
    python3 main.py fake --interface include/ISerialPort.h --output ./tests
    python3 main.py cmake --interface include/ISerialPort.h --output ./tests

📚 Docs
-------

More documentation and info at

* `gen_test.readthedocs.io <https://gen_test.readthedocs.io>`_
* `www.python.org <https://www.python.org/>`_

👥 Contributing
---------------

`Contributing to gen_test <https://github.com/vroncevic/gen_test/blob/dev/CONTRIBUTING.md>`_

📄 Copyright and licence
-------------------------

Copyright (C) 2026 by `vroncevic.github.io/gen_test <https://vroncevic.github.io/gen_test>`_

**gen_test** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.
