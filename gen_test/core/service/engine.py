# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Defines core application service implementing IService.
'''

from __future__ import annotations

from collections.abc import Mapping
from ats_utilities.exceptions import ATSValueError, ATSTypeError
from ats_utilities.validation.check_value import not_none
from ats_utilities.validation.check_type import istype
from ats_utilities.utils.reflection import to_str

from gen_test.core.model.test_suite_config import TestSuiteConfig
from gen_test.core.model.generation_result import GenerationResult
from gen_test.core.service.isubprocessor import ISubProcessor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_test/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Service:
    '''
        Core application service implementing IService protocol.

        It defines:

            :attributes:
                | _subprocessor - The subprocessor adapter executing generation pipelines.
            :methods:
                | __init__ - Initializes the service with a subprocessor adapter.
                | generate_suite - Generates full test suite.
                | generate_mock - Generates GoogleMock header file.
                | generate_test - Generates GoogleTest test file.
                | generate_fake - Generates in-memory fake stub.
                | generate_cmake - Generates CMakeLists.txt build file.
                | is_initialized - Checks if service is initialized.
                | __str__ - Returns string representation of the service.
    '''

    _subprocessor: ISubProcessor[TestSuiteConfig, GenerationResult]

    def __init__(
        self,
        subprocessor: ISubProcessor[TestSuiteConfig, GenerationResult]
    ) -> None:
        '''
            Initializes the Service with a subprocessor.

            :param subprocessor: SubProcessor adapter instance.
            :exceptions:
                | ATSValueError: When subprocessor is None.
                | ATSTypeError: When subprocessor is not an ISubProcessor.
        '''
        ctx: str = 'gen_test_service::init(...)'
        not_none(subprocessor, ctx, 'subprocessor must be provided')
        istype(subprocessor, ISubProcessor, ctx, 'subprocessor must implement ISubProcessor')
        self._subprocessor = subprocessor

    def generate_suite(self, config: TestSuiteConfig) -> GenerationResult:
        '''
            Generates complete test suite for C++ interface.

            :param config: Generation configuration options.
            :return: GenerationResult object.
            :exceptions: None.
        '''
        return self._subprocessor.run(params=config)

    def generate_mock(self, config: TestSuiteConfig) -> GenerationResult:
        '''
            Generates GoogleMock header for C++ interface.

            :param config: Generation configuration options.
            :return: GenerationResult object.
            :exceptions: None.
        '''
        mock_config = TestSuiteConfig(
            interface_path=config.interface_path,
            output_dir=config.output_dir,
            include_prefix=config.include_prefix,
            interface_name=config.interface_name,
            cmake_target=config.cmake_target,
            generate_mock=True,
            generate_test=False,
            generate_fake=False,
            generate_cmake=False,
            generate_main=False,
            run_clang_format=config.run_clang_format
        )
        return self._subprocessor.run(params=mock_config)

    def generate_test(self, config: TestSuiteConfig) -> GenerationResult:
        '''
            Generates GoogleTest unit test file for C++ interface.

            :param config: Generation configuration options.
            :return: GenerationResult object.
            :exceptions: None.
        '''
        test_config = TestSuiteConfig(
            interface_path=config.interface_path,
            output_dir=config.output_dir,
            include_prefix=config.include_prefix,
            interface_name=config.interface_name,
            cmake_target=config.cmake_target,
            generate_mock=False,
            generate_test=True,
            generate_fake=False,
            generate_cmake=False,
            generate_main=False,
            run_clang_format=config.run_clang_format
        )
        return self._subprocessor.run(params=test_config)

    def generate_fake(self, config: TestSuiteConfig) -> GenerationResult:
        '''
            Generates in-memory fake stub for C++ interface.

            :param config: Generation configuration options.
            :return: GenerationResult object.
            :exceptions: None.
        '''
        fake_config = TestSuiteConfig(
            interface_path=config.interface_path,
            output_dir=config.output_dir,
            include_prefix=config.include_prefix,
            interface_name=config.interface_name,
            cmake_target=config.cmake_target,
            generate_mock=False,
            generate_test=False,
            generate_fake=True,
            generate_cmake=False,
            generate_main=False,
            run_clang_format=config.run_clang_format
        )
        return self._subprocessor.run(params=fake_config)

    def generate_cmake(self, config: TestSuiteConfig) -> GenerationResult:
        '''
            Generates CMakeLists.txt build file.

            :param config: Generation configuration options.
            :return: GenerationResult object.
            :exceptions: None.
        '''
        cmake_config = TestSuiteConfig(
            interface_path=config.interface_path,
            output_dir=config.output_dir,
            include_prefix=config.include_prefix,
            interface_name=config.interface_name,
            cmake_target=config.cmake_target,
            generate_mock=False,
            generate_test=False,
            generate_fake=False,
            generate_cmake=True,
            generate_main=False,
            run_clang_format=config.run_clang_format
        )
        return self._subprocessor.run(params=cmake_config)

    def is_initialized(self) -> bool:
        '''
            Checks if service is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
        return self._subprocessor is not None and self._subprocessor.is_initialized()

    def __str__(self) -> str:
        '''
            Returns string representation of the Service.

            :return: String representation.
            :exceptions: None.
        '''
        return to_str(self)
