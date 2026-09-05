# -*- coding: UTF-8 -*-

'''
Module
    mock_generator_test.py
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
    Unit tests for MockGenerator class.
'''

from __future__ import annotations

from os import unlink
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase

from gen_test.core.model.cpp_interface import CppInterface
from gen_test.core.model.cpp_method import CppMethod
from gen_test.infrastructure.generator.mock_generator import MockGenerator


class TestMockGenerator(TestCase):
    '''
        Unit tests for MockGenerator class.
    '''

    def test_mock_generation(self) -> None:
        '''
            Tests GoogleMock header generation with methods and qualifiers.
        '''
        gen = MockGenerator()
        self.assertTrue(gen.is_initialized())
        self.assertIn('MockGenerator', str(gen))

        interface = CppInterface(
            name='ISerialPort',
            namespace='hardware::comm',
            methods=(
                CppMethod(
                    name='open',
                    return_type='bool',
                    parameters=(('const std::string&', 'port'), ('int', 'baud')),
                    is_const=False,
                    is_noexcept=True
                ),
                CppMethod(
                    name='is_open',
                    return_type='bool',
                    parameters=(),
                    is_const=True
                )
            ),
            header_path='hardware/ISerialPort.h'
        )

        code = gen.generate(interface, include_prefix='comm')
        self.assertIn('#pragma once', code)
        self.assertIn('#include "comm/ISerialPort.h"', code)
        self.assertIn('class MockSerialPort : public ISerialPort', code)
        self.assertIn('MOCK_METHOD(bool, open, (const std::string& port, int baud), (noexcept, override));', code)
        self.assertIn('MOCK_METHOD(bool, is_open, (), (const, override));', code)
        self.assertIn('using NiceMockSerialPort = ::testing::NiceMock<MockSerialPort>;', code)
        self.assertIn('using StrictMockSerialPort = ::testing::StrictMock<MockSerialPort>;', code)

    def test_mock_generation_without_namespace_or_header_path(self) -> None:
        '''
            Tests generation when interface has no namespace or explicit header path.
        '''
        gen = MockGenerator()
        interface = CppInterface(
            name='SimpleInterface',
            namespace='',
            methods=(CppMethod(name='execute', return_type='void'),)
        )
        code = gen.generate(interface)
        self.assertIn('class MockSimpleInterface : public SimpleInterface', code)
        self.assertIn('#include "SimpleInterface.h"', code)
        self.assertNotIn('namespace', code)

    def test_mock_generation_with_custom_template(self) -> None:
        '''
            Tests GoogleMock generation with custom template path.
        '''
        with NamedTemporaryFile(mode='w', suffix='.template', delete=False) as tmp:
            tmp.write('// custom mock ${MOCK_CLASS}')
            tmp_path = tmp.name

        try:
            gen = MockGenerator(template_path=tmp_path)
            interface = CppInterface(
                name='ISensor',
                namespace='acme',
                methods=(),
                header_path='ISensor.h'
            )
            code = gen.generate(interface)
            self.assertIn('// custom mock MockSensor', code)
        finally:
            if exists(tmp_path):
                unlink(tmp_path)
