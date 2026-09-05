# -*- coding: UTF-8 -*-

'''
Module
    fake_generator_test.py
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
    Unit tests for FakeGenerator class.
'''

from __future__ import annotations

from os import unlink
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase

from gen_um_test.core.model.cpp_interface import CppInterface
from gen_um_test.core.model.cpp_method import CppMethod
from gen_um_test.infrastructure.generator.fake_generator import FakeGenerator


class TestFakeGenerator(TestCase):
    '''
        Unit tests for FakeGenerator class.
    '''

    def test_fake_generation(self) -> None:
        '''
            Tests Fake stub class generation.
        '''
        gen = FakeGenerator()
        self.assertTrue(gen.is_initialized())
        self.assertIn('FakeGenerator', str(gen))

        interface = CppInterface(
            name='ISerialPort',
            namespace='hardware::comm',
            methods=(
                CppMethod(name='open', return_type='bool', parameters=(('const std::string&', 'port'),)),
                CppMethod(name='close', return_type='void', parameters=()),
                CppMethod(name='reset', return_type='void', parameters=(), is_const=True, is_noexcept=True)
            ),
            header_path='hardware/ISerialPort.h'
        )

        code = gen.generate(interface, include_prefix='comm')
        self.assertIn('#pragma once', code)
        self.assertIn('class FakeSerialPort : public ISerialPort', code)
        self.assertIn('mutable size_t open_calls{0};', code)
        self.assertIn('mutable size_t close_calls{0};', code)
        self.assertIn('++open_calls;', code)
        self.assertIn('return true;', code)
        self.assertIn('++close_calls;', code)
        self.assertIn('const noexcept override', code)

    def test_fake_generation_with_custom_template(self) -> None:
        '''
            Tests Fake stub class generation with custom template path.
        '''
        with NamedTemporaryFile(mode='w', suffix='.template', delete=False) as tmp:
            tmp.write('// custom fake ${FAKE_CLASS}')
            tmp_path = tmp.name

        try:
            gen = FakeGenerator(template_path=tmp_path)
            interface = CppInterface(
                name='ISensor',
                namespace='acme',
                methods=(),
                header_path='ISensor.h'
            )
            code = gen.generate(interface)
            self.assertIn('// custom fake FakeSensor', code)
        finally:
            if exists(tmp_path):
                unlink(tmp_path)
