# -*- coding: UTF-8 -*-

'''
Module
    cpp_method_test.py
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
    Unit tests for CppMethod model.
'''

from __future__ import annotations

from unittest import TestCase

from gen_test.core.model.cpp_method import CppMethod

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_test/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCppMethod(TestCase):
    '''
        Unit tests for CppMethod dataclass.
    '''

    def test_method_creation(self) -> None:
        '''
            Tests standard CppMethod creation and properties.
        '''
        method = CppMethod(
            name='open',
            return_type='bool',
            parameters=(('const std::string&', 'port'), ('int', 'baud')),
            is_const=False,
            is_noexcept=True
        )
        self.assertEqual(method.name, 'open')
        self.assertEqual(method.return_type, 'bool')
        self.assertEqual(method.params_signature, 'const std::string& port, int baud')
        self.assertEqual(method.params_call, 'port, baud')
        self.assertEqual(method.default_return_value, 'true')

    def test_default_return_values(self) -> None:
        '''
            Tests default return values for diverse C++ types.
        '''
        cases = [
            ('void', ''),
            ('bool', 'true'),
            ('int', '0'),
            ('size_t', '0'),
            ('uint32_t', '0'),
            ('float', '0.0'),
            ('double', '0.0'),
            ('std::string', '""'),
            ('const std::string&', '""'),
            ('ISerialPort*', 'nullptr'),
            ('std::vector<int>', '{}')
        ]
        for ret_type, expected in cases:
            m = CppMethod(name='test_fn', return_type=ret_type)
            self.assertEqual(m.default_return_value, expected, f'Failed for type {ret_type}')

    def test_empty_parameters(self) -> None:
        '''
            Tests behavior when parameters tuple is empty.
        '''
        method = CppMethod(name='close', return_type='void', parameters=())
        self.assertEqual(method.params_signature, '')
        self.assertEqual(method.params_call, '')
        self.assertTrue(method.is_void)

    def test_parameters_without_names(self) -> None:
        '''
            Tests behavior when parameter names are empty.
        '''
        method = CppMethod(
            name='calc',
            return_type='int',
            parameters=(('int', ''), ('double', 'val'))
        )
        self.assertEqual(method.params_signature, 'int, double val')
        self.assertEqual(method.params_call, 'val')
