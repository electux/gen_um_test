# -*- coding: UTF-8 -*-

'''
Module
    cmake_generator_test.py
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
    Unit tests for CMakeGenerator class.
'''

from __future__ import annotations

from os import unlink
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase

from gen_test.infrastructure.generator.cmake_generator import CMakeGenerator


class TestCMakeGenerator(TestCase):
    '''
        Unit tests for CMakeGenerator class.
    '''

    def test_cmake_generation(self) -> None:
        '''
            Tests CMakeLists.txt generation.
        '''
        gen = CMakeGenerator()
        self.assertTrue(gen.is_initialized())
        self.assertIn('CMakeGenerator', str(gen))

        code = gen.generate(
            target_name='serial_port_test',
            sources=('serial_port_test.cc', 'test_main.cc'),
            headers=('mock_serial_port.h',)
        )
        self.assertIn('project(serial_port_test LANGUAGES CXX)', code)
        self.assertIn('add_executable(serial_port_test', code)
        self.assertIn('serial_port_test.cc', code)
        self.assertIn('test_main.cc', code)
        self.assertIn('mock_serial_port.h', code)
        self.assertIn('GTest::gtest', code)
        self.assertIn('GTest::gmock', code)
        self.assertIn('gtest_discover_tests(serial_port_test)', code)

    def test_cmake_generation_with_custom_template(self) -> None:
        '''
            Tests CMakeLists.txt generation with custom template path.
        '''
        with NamedTemporaryFile(mode='w', suffix='.template', delete=False) as tmp:
            tmp.write('project(${TARGET_NAME})\n# custom cmake template')
            tmp_path = tmp.name

        try:
            gen = CMakeGenerator(template_path=tmp_path)
            code = gen.generate(
                target_name='custom_test',
                sources=('test.cc',),
                headers=()
            )
            self.assertIn('project(custom_test)', code)
            self.assertIn('# custom cmake template', code)
        finally:
            if exists(tmp_path):
                unlink(tmp_path)
