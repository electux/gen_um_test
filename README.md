# Generate GoogleTest/GoogleMock Test Suites for C++ Interfaces

<img align="right" src="https://raw.githubusercontent.com/electux/gen_test/dev/docs/gen_test_logo.png" width="25%">

**gen_test** is a toolset for automatic generation of GoogleTest and GoogleMock test suites from C++ pure virtual interface headers.

Developed in **[python](https://www.python.org/)** code.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![gen_test python checker](https://github.com/electux/gen_test/actions/workflows/gen_test_python_checker.yml/badge.svg)](https://github.com/electux/gen_test/actions/workflows/gen_test_python_checker.yml) [![gen_test package checker](https://github.com/electux/gen_test/actions/workflows/gen_test_package_checker.yml/badge.svg)](https://github.com/electux/gen_test/actions/workflows/gen_test_package.yml) [![gen_test interface checker](https://github.com/electux/gen_test/actions/workflows/gen_test_interface_checker.yml/badge.svg)](https://github.com/electux/gen_test/actions/workflows/gen_test_interface_checker.yml) [![gen_test isp checker](https://github.com/electux/gen_test/actions/workflows/gen_test_isp_checker.yml/badge.svg)](https://github.com/electux/gen_test/actions/workflows/gen_test_isp_checker.yml) [![gen_test srp checker](https://github.com/electux/gen_test/actions/workflows/gen_test_srp_checker.yml/badge.svg)](https://github.com/electux/gen_test/actions/workflows/gen_test_srp_checker.yml) [![GitHub issues open](https://img.shields.io/github/issues/electux/gen_test.svg)](https://github.com/electux/gen_test/issues) [![GitHub contributors](https://img.shields.io/github/contributors/electux/gen_test.svg)](https://github.com/electux/gen_test/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [🚀 Installation](#-installation)
    - [Install using pip](#install-using-pip)
    - [Install using build](#install-using-build)
    - [Install using py setup](#install-using-py-setup)
    - [Install using docker](#install-using-docker)
- [📦 Dependencies](#-dependencies)
- [📁 Tool structure](#-tool-structure)
  - [✨ Features](#-features)
- [📊 Code coverage](#-code-coverage)
- [🛠 Usage](#-usage)
- [📚 Docs](#-docs)
- [👥 Contributing](#-contributing)
- [📄 Copyright and licence](#-copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### 🚀 Installation

Used next development environment

![debian linux os](https://raw.githubusercontent.com/electux/gen_test/dev/docs/debtux.png)

[![gen_test python3 build](https://github.com/electux/gen_test/actions/workflows/gen_test_python3_build.yml/badge.svg)](https://github.com/electux/gen_test/actions/workflows/gen_test_python3_build.yml)

Currently there are three ways to install package
* Install process based on using pip mechanism
* Install process based on build mechanism
* Install process based on setup.py mechanism
* Install process based on docker mechanism

##### Install using pip

**gen_test** is located at **[pypi.org](https://pypi.org/project/gen_test/)**.

You can install by using pip

```bash
# python3
pip3 install gen_test
```

##### Install using build

Navigate to release **[page](https://github.com/electux/gen_test/releases/)** download and extract release archive.

To install **gen_test** type the following

```bash
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
```

##### Install using py setup

Navigate to **[release page](https://github.com/electux/gen_test/releases)** download and extract release archive.

To install **gen_test** locate and run setup.py with arguments

```bash
tar xvzf gen_test-x.y.z.tar.gz
cd gen_test-x.y.z
# python3
pip3 install -r requirements.txt
python3 setup.py install_lib
python3 setup.py install_egg_info
```

##### Install using docker

You can use Dockerfile to create image/container.

### 📦 Dependencies

**gen_test** requires next modules and libraries

* [ats-utilities - Python App/Tool/Script Utilities](https://pypi.org/project/ats-utilities/)

### 📁 Tool structure

**gen_test** is based on OOP.

Tool structure

<details>
<summary><b>Click to expand framework structure</b></summary>

```bash
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
```
</details>

#### ✨ Features

* Parses C++ pure virtual interface header files (`.h` / `.hpp`).
* Synthesizes modern GoogleMock header mocks using `MOCK_METHOD(...)` with `#pragma once`.
* Generates unit test suites (`<interface>_test.cc`), in-memory fake stubs (`fake_<interface>.h`), and test runners (`test_main.cc`).
* Generates standalone `CMakeLists.txt` build scripts integrated with GoogleTest and GoogleMock.
* Configurable template engine structured in `templates.tgz` with `scheme.json` schema validation.
* Provides a modular and extensible architecture based on OOP, SOLID, and Hexagonal principles.
* Includes command line interface (CLI) support via a command/executor structure.
* High code quality with full type checking and 100% unit test coverage.

### 📊 Code coverage

<details>
<summary><b>Click to expand code coverage</b></summary>

| Name | Stmts | Miss | Cover |
|------|-------|------|-------|
| `gen_test/__init__.py` | 9 | 0 | 100%|
| `gen_test/core/__init__.py` | 9 | 0 | 100%|
| `gen_test/core/model/__init__.py` | 9 | 0 | 100%|
| `gen_test/core/model/cpp_interface.py` | 43 | 0 | 100%|
| `gen_test/core/model/cpp_method.py` | 43 | 0 | 100%|
| `gen_test/core/model/generation_result.py` | 19 | 0 | 100%|
| `gen_test/core/model/test_suite_config.py` | 23 | 0 | 100%|
| `gen_test/core/service/__init__.py` | 9 | 0 | 100%|
| `gen_test/core/service/engine.py` | 42 | 0 | 100%|
| `gen_test/core/service/icmake_generator.py` | 14 | 0 | 100%|
| `gen_test/core/service/icpp_parser.py` | 16 | 0 | 100%|
| `gen_test/core/service/ifake_generator.py` | 15 | 0 | 100%|
| `gen_test/core/service/imock_generator.py` | 15 | 0 | 100%|
| `gen_test/core/service/iservice.py` | 20 | 0 | 100%|
| `gen_test/core/service/isubprocessor.py` | 14 | 0 | 100%|
| `gen_test/core/service/itest_generator.py` | 15 | 0 | 100%|
| `gen_test/engine.py` | 57 | 0 | 100%|
| `gen_test/infrastructure/__init__.py` | 9 | 0 | 100%|
| `gen_test/infrastructure/cli/__init__.py` | 9 | 0 | 100%|
| `gen_test/infrastructure/cli/engine.py` | 39 | 0 | 100%|
| `gen_test/infrastructure/cli/icli.py` | 14 | 0 | 100%|
| `gen_test/infrastructure/cli/setup/__init__.py` | 9 | 0 | 100%|
| `gen_test/infrastructure/cli/setup/bundle.py` | 22 | 0 | 100%|
| `gen_test/infrastructure/cli/setup/dep_validator.py` | 36 | 0 | 100%|
| `gen_test/infrastructure/cli/setup/dependencies.py` | 18 | 0 | 100%|
| `gen_test/infrastructure/cli/setup/factory.py` | 49 | 0 | 100%|
| `gen_test/infrastructure/cli/setup/keys.py` | 26 | 0 | 100%|
| `gen_test/infrastructure/cli/setup/opt_validator.py` | 36 | 0 | 100%|
| `gen_test/infrastructure/cli/setup/options.py` | 15 | 0 | 100%|
| `gen_test/infrastructure/cli/setup/registry.py` | 24 | 0 | 100%|
| `gen_test/infrastructure/cli/setup/validator.py` | 43 | 0 | 100%|
| `gen_test/infrastructure/command/__init__.py` | 9 | 0 | 100%|
| `gen_test/infrastructure/command/cmake_command_definition.py` | 24 | 0 | 100%|
| `gen_test/infrastructure/command/cmake_command_executor.py` | 28 | 0 | 100%|
| `gen_test/infrastructure/command/command.py` | 16 | 0 | 100%|
| `gen_test/infrastructure/command/fake_command_definition.py` | 24 | 0 | 100%|
| `gen_test/infrastructure/command/fake_command_executor.py` | 28 | 0 | 100%|
| `gen_test/infrastructure/command/icommand_definition.py` | 14 | 0 | 100%|
| `gen_test/infrastructure/command/icommand_executor.py` | 14 | 0 | 100%|
| `gen_test/infrastructure/command/mock_command_definition.py` | 24 | 0 | 100%|
| `gen_test/infrastructure/command/mock_command_executor.py` | 28 | 0 | 100%|
| `gen_test/infrastructure/command/suite_command_definition.py` | 24 | 0 | 100%|
| `gen_test/infrastructure/command/suite_command_executor.py` | 28 | 0 | 100%|
| `gen_test/infrastructure/command/test_command_definition.py` | 24 | 0 | 100%|
| `gen_test/infrastructure/command/test_command_executor.py` | 28 | 0 | 100%|
| `gen_test/infrastructure/generator/__init__.py` | 9 | 0 | 100%|
| `gen_test/infrastructure/generator/cmake_generator.py` | 32 | 0 | 100%|
| `gen_test/infrastructure/generator/code_formatter.py` | 28 | 0 | 100%|
| `gen_test/infrastructure/generator/fake_generator.py` | 57 | 0 | 100%|
| `gen_test/infrastructure/generator/main_generator.py` | 26 | 0 | 100%|
| `gen_test/infrastructure/generator/mock_generator.py` | 46 | 0 | 100%|
| `gen_test/infrastructure/generator/template_provider.py` | 75 | 0 | 100%|
| `gen_test/infrastructure/generator/test_generator.py` | 68 | 0 | 100%|
| `gen_test/infrastructure/parser/__init__.py` | 9 | 0 | 100%|
| `gen_test/infrastructure/parser/cpp_parser.py` | 110 | 0 | 100%|
| `gen_test/infrastructure/subprocessor.py` | 122 | 0 | 100%|
| `gen_test/setup/__init__.py` | 9 | 0 | 100%|
| `gen_test/setup/bundle.py` | 23 | 0 | 100%|
| `gen_test/setup/dep_validator.py` | 36 | 0 | 100%|
| `gen_test/setup/dependencies.py` | 19 | 0 | 100%|
| `gen_test/setup/factory.py` | 58 | 0 | 100%|
| `gen_test/setup/keys.py` | 27 | 0 | 100%|
| `gen_test/setup/opt_validator.py` | 36 | 0 | 100%|
| `gen_test/setup/options.py` | 12 | 0 | 100%|
| `gen_test/setup/registry.py` | 24 | 0 | 100%|
| `gen_test/setup/validator.py` | 48 | 0 | 100%|
| **Total** | 1908 | 0 | 100% |

</details>

### 🛠 Usage

Install package

```bash
pip3 install gen_test
```

Prepare main entry point by downloading [main.py](https://raw.githubusercontent.com/electux/gen_test/main/main.py) or create your own.


```bash
wget -O main.py https://raw.githubusercontent.com/electux/gen_test/main/main.py
```

Running tool for generating complete GoogleTest suite:

```bash
python3 main.py suite --interface include/ISerialPort.h --output ./tests --prefix comm
```

Running tool for generating individual components:

```bash
python3 main.py mock --interface include/ISerialPort.h --output ./tests
python3 main.py test --interface include/ISerialPort.h --output ./tests
python3 main.py fake --interface include/ISerialPort.h --output ./tests
python3 main.py cmake --interface include/ISerialPort.h --output ./tests
```

### 📚 Docs

[![Documentation Status](https://readthedocs.org/projects/gen_test/badge/?version=latest)](https://gen_test.readthedocs.io/en/latest/?badge=latest)

More documentation and info at

* [gen_test.readthedocs.io](https://gen_test.readthedocs.io)
* [www.python.org](https://www.python.org/)

### 👥 Contributing

[Contributing to gen_test](CONTRIBUTING.md)

### 📄 Copyright and licence

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Copyright (C) 2026 by [vroncevic.github.io/gen_test](https://vroncevic.github.io/gen_test)

**gen_test** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.

[![Python Software Foundation](https://raw.githubusercontent.com/electux/gen_test/dev/docs/psf-logo-alpha.png)](https://www.python.org/psf/)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.python.org/psf/donations/)
