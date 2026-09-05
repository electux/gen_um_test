# -*- coding: UTF-8 -*-

'''
Module
    test_suite_config.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    gen_um_test is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    gen_um_test is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines TestSuiteConfig domain model for test generation configuration.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_um_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_um_test/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class TestSuiteConfig:
    '''
        Configuration model controlling code synthesis options.

        :param interface_path: Path to the input C++ interface header.
        :param output_dir: Target output directory for generated files.
        :param include_prefix: Optional custom include prefix, e.g. "hardware/".
        :param interface_name: Optional filter for a specific interface in file.
        :param cmake_target: Optional custom CMake target name.
        :param generate_mock: Whether to generate GoogleMock header.
        :param generate_test: Whether to generate GoogleTest unit test file.
        :param generate_fake: Whether to generate Fake stub header.
        :param generate_cmake: Whether to generate CMakeLists.txt.
        :param generate_main: Whether to generate test_main.cc.
        :param run_clang_format: Whether to attempt formatting with clang-format.
    '''

    interface_path: str
    output_dir: str
    include_prefix: str = ''
    interface_name: str | None = None
    cmake_target: str | None = None
    generate_mock: bool = True
    generate_test: bool = True
    generate_fake: bool = True
    generate_cmake: bool = True
    generate_main: bool = True
    run_clang_format: bool = True
