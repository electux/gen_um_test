# -*- coding: UTF-8 -*-

'''
Module
    subprocessor.py
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
    Defines SubProcessor adapter implementing ISubProcessor protocol.
'''

from __future__ import annotations

from os import makedirs
from os.path import dirname, exists, join

from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.utils.reflection import to_str
from ats_utilities.validation.check_type import istype
from ats_utilities.validation.check_value import not_none

from gen_test.core.model.cpp_interface import CppInterface
from gen_test.core.model.test_suite_config import TestSuiteConfig
from gen_test.core.model.generation_result import GenerationResult
from gen_test.core.service.icpp_parser import ICppParser
from gen_test.core.service.imock_generator import IMockGenerator
from gen_test.core.service.itest_generator import ITestGenerator
from gen_test.core.service.ifake_generator import IFakeGenerator
from gen_test.core.service.icmake_generator import ICMakeGenerator
from gen_test.infrastructure.generator.main_generator import MainGenerator
from gen_test.infrastructure.generator.code_formatter import CodeFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_test/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SubProcessor:
    '''
        SubProcessor orchestrating C++ interface parsing and test suite code generation.

        It defines:

            :methods:
                | __init__ - Initializes SubProcessor with parsers and generators.
                | run - Executes generation pipeline.
                | is_initialized - Checks if subprocessor is initialized.
                | __str__ - Returns string representation of SubProcessor.
    '''

    _parser: ICppParser
    _mock_gen: IMockGenerator
    _test_gen: ITestGenerator
    _fake_gen: IFakeGenerator
    _cmake_gen: ICMakeGenerator
    _main_gen: MainGenerator
    _formatter: CodeFormatter

    def __init__(
        self,
        parser: ICppParser,
        mock_gen: IMockGenerator,
        test_gen: ITestGenerator,
        fake_gen: IFakeGenerator,
        cmake_gen: ICMakeGenerator,
        main_gen: MainGenerator,
        formatter: CodeFormatter
    ) -> None:
        '''
            Initializes SubProcessor with required adapter ports.

            :param parser: ICppParser instance.
            :param mock_gen: IMockGenerator instance.
            :param test_gen: ITestGenerator instance.
            :param fake_gen: IFakeGenerator instance.
            :param cmake_gen: ICMakeGenerator instance.
            :param main_gen: MainGenerator instance.
            :param formatter: CodeFormatter instance.
        '''
        ctx: str = 'subprocessor::init(...)'
        not_none(parser, ctx, 'parser must be provided')
        istype(parser, ICppParser, ctx, 'parser must implement ICppParser')
        not_none(mock_gen, ctx, 'mock_gen must be provided')
        istype(mock_gen, IMockGenerator, ctx, 'mock_gen must implement IMockGenerator')
        not_none(test_gen, ctx, 'test_gen must be provided')
        istype(test_gen, ITestGenerator, ctx, 'test_gen must implement ITestGenerator')
        not_none(fake_gen, ctx, 'fake_gen must be provided')
        istype(fake_gen, IFakeGenerator, ctx, 'fake_gen must implement IFakeGenerator')
        not_none(cmake_gen, ctx, 'cmake_gen must be provided')
        istype(cmake_gen, ICMakeGenerator, ctx, 'cmake_gen must implement ICMakeGenerator')

        self._parser = parser
        self._mock_gen = mock_gen
        self._test_gen = test_gen
        self._fake_gen = fake_gen
        self._cmake_gen = cmake_gen
        self._main_gen = main_gen
        self._formatter = formatter

    def run(self, *, params: TestSuiteConfig) -> GenerationResult:
        '''
            Executes C++ test suite synthesis pipeline.

            :param params: TestSuiteConfig model.
            :return: GenerationResult model.
        '''
        ctx: str = 'subprocessor::run(...)'
        not_none(params, ctx, 'params must be provided')
        istype(params, TestSuiteConfig, ctx, 'params must be instance of TestSuiteConfig')

        try:
            interfaces = self._parser.parse_file(params.interface_path)
            if not interfaces:
                return GenerationResult(
                    success=False,
                    message=f'No C++ pure virtual interfaces found in: {params.interface_path}'
                )

            if params.interface_name:
                interfaces = tuple(i for i in interfaces if i.name == params.interface_name)
                if not interfaces:
                    return GenerationResult(
                        success=False,
                        message=f'Interface "{params.interface_name}" not found in {params.interface_path}'
                    )

            makedirs(params.output_dir, exist_ok=True)
            generated_files: list[str] = []

            for interface in interfaces:
                files = self._generate_for_interface(interface, params)
                generated_files.extend(files)

            if params.run_clang_format:
                for file_path in generated_files:
                    if file_path.endswith(('.h', '.cc')):
                        self._formatter.format_file(file_path)

            return GenerationResult(
                success=True,
                output_dir=params.output_dir,
                generated_files=tuple(generated_files),
                message=f'Successfully generated test suite with {len(generated_files)} file(s)',
                interfaces_count=len(interfaces)
            )

        except Exception as err:
            return GenerationResult(
                success=False,
                output_dir=params.output_dir,
                message=f'Generation failed: {str(err)}'
            )

    def is_initialized(self) -> bool:
        '''
            Checks if subprocessor is initialized.
        '''
        return (
            self._parser.is_initialized() and
            self._mock_gen.is_initialized() and
            self._test_gen.is_initialized() and
            self._fake_gen.is_initialized() and
            self._cmake_gen.is_initialized() and
            self._main_gen.is_initialized() and
            self._formatter.is_initialized()
        )

    def _generate_for_interface(
        self,
        interface: CppInterface,
        params: TestSuiteConfig
    ) -> list[str]:
        '''
            Generates requested artifacts for a single C++ interface.
        '''
        created_files: list[str] = []
        mock_file_name = f'mock_{interface.snake_name}.h'
        mock_file_path = join(params.output_dir, mock_file_name)

        fake_file_name = f'fake_{interface.snake_name}.h'
        fake_file_path = join(params.output_dir, fake_file_name)

        test_file_name = f'{interface.snake_name}_test.cc'
        test_file_path = join(params.output_dir, test_file_name)

        main_file_name = 'test_main.cc'
        main_file_path = join(params.output_dir, main_file_name)

        cmake_file_name = 'CMakeLists.txt'
        cmake_file_path = join(params.output_dir, cmake_file_name)

        if params.generate_mock:
            content = self._mock_gen.generate(interface, params.include_prefix)
            self._write_file(mock_file_path, content)
            created_files.append(mock_file_path)

        if params.generate_fake:
            content = self._fake_gen.generate(interface, params.include_prefix)
            self._write_file(fake_file_path, content)
            created_files.append(fake_file_path)

        if params.generate_test:
            content = self._test_gen.generate(interface, mock_file_name)
            self._write_file(test_file_path, content)
            created_files.append(test_file_path)

        if params.generate_main:
            content = self._main_gen.generate()
            self._write_file(main_file_path, content)
            created_files.append(main_file_path)

        if params.generate_cmake:
            target = params.cmake_target or f'{interface.snake_name}_test'
            sources = (test_file_name, main_file_name) if params.generate_main else (test_file_name,)
            headers = (mock_file_name,)
            content = self._cmake_gen.generate(target, sources, headers)
            self._write_file(cmake_file_path, content)
            created_files.append(cmake_file_path)

        return created_files

    def _write_file(self, file_path: str, content: str) -> None:
        '''
            Writes content string to file.
        '''
        parent = dirname(file_path)
        if parent and not exists(parent):
            makedirs(parent, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as handle:
            handle.write(content)

    def __str__(self) -> str:
        '''
            Returns string representation of SubProcessor.
        '''
        return to_str(self)
