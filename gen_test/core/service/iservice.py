# -*- coding: UTF-8 -*-

'''
Module
    iservice.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    gen_test is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    gen_test is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines abstract interface for gen_test core service.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from gen_test.core.model.test_suite_config import TestSuiteConfig
from gen_test.core.model.generation_result import GenerationResult

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_test/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IService(Protocol):
    '''
        Defines abstract interface for gen_test core service.

        It defines:

            :methods:
                | generate_suite - Generates complete test suite (mock, test, fake, cmake, main).
                | generate_mock - Generates GoogleMock header for interface.
                | generate_test - Generates GoogleTest test file for interface.
                | generate_fake - Generates in-memory fake stub for interface.
                | generate_cmake - Generates CMakeLists.txt for interface tests.
                | is_initialized - Checks if service is initialized.
    '''

    def generate_suite(self, config: TestSuiteConfig) -> GenerationResult:
        '''
            Generates complete test suite.

            :param config: Generation configuration options.
            :return: GenerationResult object.
            :exceptions: None.
        '''

    def generate_mock(self, config: TestSuiteConfig) -> GenerationResult:
        '''
            Generates GoogleMock header file.

            :param config: Generation configuration options.
            :return: GenerationResult object.
            :exceptions: None.
        '''

    def generate_test(self, config: TestSuiteConfig) -> GenerationResult:
        '''
            Generates GoogleTest unit test file.

            :param config: Generation configuration options.
            :return: GenerationResult object.
            :exceptions: None.
        '''

    def generate_fake(self, config: TestSuiteConfig) -> GenerationResult:
        '''
            Generates Fake in-memory stub header.

            :param config: Generation configuration options.
            :return: GenerationResult object.
            :exceptions: None.
        '''

    def generate_cmake(self, config: TestSuiteConfig) -> GenerationResult:
        '''
            Generates CMakeLists.txt build file.

            :param config: Generation configuration options.
            :return: GenerationResult object.
            :exceptions: None.
        '''

    def is_initialized(self) -> bool:
        '''
            Checks if service is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
