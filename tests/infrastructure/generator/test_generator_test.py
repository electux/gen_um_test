# -*- coding: UTF-8 -*-

'''
Module
    test_generator_test.py
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
    Unit tests for TestGenerator class.
'''

from __future__ import annotations

from os import unlink
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase

from gen_um_test.core.model.cpp_interface import CppInterface
from gen_um_test.core.model.cpp_method import CppMethod
from gen_um_test.infrastructure.generator.test_generator import TestGenerator


class TestTestGenerator(TestCase):
    '''
        Unit tests for TestGenerator class.
    '''

    def test_test_generation(self) -> None:
        '''
            Tests GoogleTest test fixture generation.
        '''
        gen = TestGenerator()
        self.assertTrue(gen.is_initialized())
        self.assertIn('TestGenerator', str(gen))

        interface = CppInterface(
            name='ISerialPort',
            namespace='hardware::comm',
            methods=(
                CppMethod(name='open', return_type='bool', parameters=(('const std::string&', 'port'),)),
                CppMethod(name='close', return_type='void', parameters=()),
                CppMethod(name='calc', return_type='int', parameters=(('int', 'x'),)),
                CppMethod(
                    name='process',
                    return_type='void',
                    parameters=(('const uint8_t*', 'buf'), ('double', 'rate'), ('bool', 'flag'))
                )
            )
        )

        code = gen.generate(interface, mock_header_name='mock_serial_port.h')
        self.assertIn('#include "mock_serial_port.h"', code)
        self.assertIn('class SerialPortTest : public ::testing::Test', code)
        self.assertIn('TEST_F(SerialPortTest, CallsOpen)', code)
        self.assertIn('EXPECT_CALL(mock, open(::testing::_))', code)
        self.assertIn('TEST_F(SerialPortTest, CallsClose)', code)
        self.assertIn('EXPECT_CALL(mock, close()).Times(1);', code)
        self.assertIn('TEST_F(SerialPortTest, CallsCalc)', code)
        self.assertIn('TEST_F(SerialPortTest, CallsProcess)', code)
        self.assertIn('mock.process(nullptr, 0.0, false);', code)

    def test_test_generation_with_custom_template(self) -> None:
        '''
            Tests GoogleTest test fixture generation with custom template path.
        '''
        with NamedTemporaryFile(mode='w', suffix='.template', delete=False) as tmp:
            tmp.write('// custom test ${TEST_FIXTURE_CLASS}')
            tmp_path = tmp.name

        try:
            gen = TestGenerator(template_path=tmp_path)
            interface = CppInterface(
                name='ISensor',
                namespace='acme',
                methods=(),
                header_path='ISensor.h'
            )
            code = gen.generate(interface, mock_header_name='mock_sensor.h')
            self.assertIn('// custom test SensorTest', code)
        finally:
            if exists(tmp_path):
                unlink(tmp_path)
