# -*- coding: UTF-8 -*-

'''
Module
    cpp_interface_test.py
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
    Unit tests for CppInterface model.
'''

from __future__ import annotations

from unittest import TestCase

from gen_um_test.core.model.cpp_interface import CppInterface
from gen_um_test.core.model.cpp_method import CppMethod

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_um_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_um_test/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCppInterface(TestCase):
    '''
        Unit tests for CppInterface domain model.
    '''

    def test_clean_name_and_naming_conventions(self) -> None:
        '''
            Tests name derivations from interface name.
        '''
        interface = CppInterface(
            name='ISerialPort',
            namespace='hardware::comm',
            includes=('<string>',),
            methods=(CppMethod(name='open', return_type='bool'),),
            header_path='hardware/ISerialPort.h'
        )
        self.assertEqual(interface.clean_name, 'SerialPort')
        self.assertEqual(interface.mock_class_name, 'MockSerialPort')
        self.assertEqual(interface.fake_class_name, 'FakeSerialPort')
        self.assertEqual(interface.test_class_name, 'SerialPortTest')
        self.assertEqual(interface.snake_name, 'serial_port')
        self.assertEqual(interface.full_qualified_name, 'hardware::comm::ISerialPort')

    def test_clean_name_without_i_prefix(self) -> None:
        '''
            Tests clean_name when interface doesn't start with 'I'.
        '''
        interface = CppInterface(name='DeviceReader', namespace='')
        self.assertEqual(interface.clean_name, 'DeviceReader')
        self.assertEqual(interface.mock_class_name, 'MockDeviceReader')
        self.assertEqual(interface.full_qualified_name, 'DeviceReader')

    def test_clean_name_with_single_i(self) -> None:
        '''
            Tests clean_name when name is simply 'I' or starts with lowercase.
        '''
        i_only = CppInterface(name='I')
        self.assertEqual(i_only.clean_name, 'I')
        item = CppInterface(name='Item')
        self.assertEqual(item.clean_name, 'Item')
