# -*- coding: UTF-8 -*-

'''
Module
    subprocessor_test.py
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
    Unit tests for SubProcessor adapter.
'''

from __future__ import annotations

from os.path import exists, join
from tempfile import TemporaryDirectory
from unittest import TestCase

from ats_utilities.exceptions import ATSTypeError, ATSValueError

from gen_test.core.model.test_suite_config import TestSuiteConfig
from gen_test.infrastructure.generator.cmake_generator import CMakeGenerator
from gen_test.infrastructure.generator.code_formatter import CodeFormatter
from gen_test.infrastructure.generator.fake_generator import FakeGenerator
from gen_test.infrastructure.generator.main_generator import MainGenerator
from gen_test.infrastructure.generator.mock_generator import MockGenerator
from gen_test.infrastructure.generator.template_provider import TemplateProvider
from gen_test.infrastructure.generator.test_generator import TestGenerator
from gen_test.infrastructure.parser.cpp_parser import CppParser
from gen_test.infrastructure.subprocessor import SubProcessor


class TestSubProcessor(TestCase):
    '''
        Unit tests for SubProcessor adapter.
    '''

    def setUp(self) -> None:
        '''
            Sets up test dependencies for subprocessor.
        '''
        self.provider = TemplateProvider()
        self.parser = CppParser()
        self.mock_gen = MockGenerator(template_provider=self.provider)
        self.fake_gen = FakeGenerator(template_provider=self.provider)
        self.test_gen = TestGenerator(template_provider=self.provider)
        self.cmake_gen = CMakeGenerator(template_provider=self.provider)
        self.main_gen = MainGenerator(template_provider=self.provider)
        self.formatter = CodeFormatter()

        self.fixture_dir = TemporaryDirectory()
        self.interface_path = join(self.fixture_dir.name, 'ISerialPort.h')
        with open(self.interface_path, 'w', encoding='utf-8') as handle:
            handle.write('''#pragma once
#include <string>
#include <vector>

namespace hardware::comm {

class ISerialPort {
public:
    virtual ~ISerialPort() = default;
    virtual bool open(const std::string& port_name, uint32_t baud_rate) = 0;
    virtual void close() = 0;
    virtual bool is_open() const = 0;
    virtual size_t write(const std::vector<uint8_t>& data) = 0;
    virtual std::vector<uint8_t> read(size_t max_bytes) = 0;
    virtual uint32_t get_baud_rate() const = 0;
};

}  // namespace hardware::comm
''')

        self.subprocessor = SubProcessor(
            parser=self.parser,
            mock_gen=self.mock_gen,
            test_gen=self.test_gen,
            fake_gen=self.fake_gen,
            cmake_gen=self.cmake_gen,
            main_gen=self.main_gen,
            formatter=self.formatter
        )

    def tearDown(self) -> None:
        '''
            Cleans up temporary fixture directory.
        '''
        self.fixture_dir.cleanup()

    def test_initialization_and_str(self) -> None:
        '''
            Tests SubProcessor initialization and string representation.
        '''
        self.assertTrue(self.subprocessor.is_initialized())
        self.assertIn('SubProcessor', str(self.subprocessor))

    def test_initialization_validation_errors(self) -> None:
        '''
            Tests SubProcessor validation on bad arguments.
        '''
        with self.assertRaises(ATSValueError):
            SubProcessor(
                parser=None,  # type: ignore[arg-type]
                mock_gen=self.mock_gen,
                test_gen=self.test_gen,
                fake_gen=self.fake_gen,
                cmake_gen=self.cmake_gen,
                main_gen=self.main_gen,
                formatter=self.formatter
            )

        with self.assertRaises(ATSTypeError):
            SubProcessor(
                parser="invalid",  # type: ignore[arg-type]
                mock_gen=self.mock_gen,
                test_gen=self.test_gen,
                fake_gen=self.fake_gen,
                cmake_gen=self.cmake_gen,
                main_gen=self.main_gen,
                formatter=self.formatter
            )

    def test_run_complete_suite(self) -> None:
        '''
            Tests generating a complete test suite from real demo interface.
        '''
        with TemporaryDirectory() as temp_dir:
            config = TestSuiteConfig(
                interface_path=self.interface_path,
                output_dir=temp_dir
            )
            result = self.subprocessor.run(params=config)
            self.assertTrue(result.success)
            self.assertEqual(len(result.generated_files), 5)

    def test_run_filtered_interface_name(self) -> None:
        '''
            Tests generating only matching interface name.
        '''
        with TemporaryDirectory() as temp_dir:
            config = TestSuiteConfig(
                interface_path=self.interface_path,
                output_dir=temp_dir,
                interface_name='ISerialPort'
            )
            result = self.subprocessor.run(params=config)
            self.assertTrue(result.success)

    def test_run_interface_not_found(self) -> None:
        '''
            Tests when specified interface_name does not match any interface in file.
        '''
        with TemporaryDirectory() as temp_dir:
            config = TestSuiteConfig(
                interface_path=self.interface_path,
                output_dir=temp_dir,
                interface_name='NonExistentInterface'
            )
            result = self.subprocessor.run(params=config)
            self.assertFalse(result.success)
            self.assertIn('not found', result.message)

    def test_run_parse_failure(self) -> None:
        '''
            Tests when interface file does not exist.
        '''
        config = TestSuiteConfig(
            interface_path='/non/existent/file.h',
            output_dir='/tmp/out'
        )
        result = self.subprocessor.run(params=config)
        self.assertFalse(result.success)

    def test_run_no_interfaces_found(self) -> None:
        '''
            Tests when header file exists but has no pure virtual interfaces.
        '''
        with TemporaryDirectory() as temp_dir:
            empty_header = join(temp_dir, 'Empty.h')
            with open(empty_header, 'w', encoding='utf-8') as handle:
                handle.write('// No interfaces here\nstruct Point { int x; int y; };\n')

            config = TestSuiteConfig(
                interface_path=empty_header,
                output_dir=join(temp_dir, 'out')
            )
            result = self.subprocessor.run(params=config)
            self.assertFalse(result.success)
            self.assertIn('No C++ pure virtual interfaces found in', result.message)

    def test_write_file_creates_parent_directory(self) -> None:
        '''
            Tests _write_file automatically creates non-existent parent directories.
        '''
        with TemporaryDirectory() as temp_dir:
            nested_file = join(temp_dir, 'level1', 'level2', 'output.txt')
            self.subprocessor._write_file(nested_file, 'test content')
            self.assertTrue(exists(nested_file))
