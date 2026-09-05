# -*- coding: UTF-8 -*-

'''
Module
    cpp_interface.py
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
    Defines CppInterface domain model representing a C++ interface class.
'''

from __future__ import annotations

from dataclasses import dataclass
from re import sub

from gen_test.core.model.cpp_method import CppMethod

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_test/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class CppInterface:
    '''
        Domain model representing a parsed C++ interface.

        :param name: Name of the interface class/struct.
        :param namespace: Namespace of the interface (e.g. "acme::hw" or "").
        :param includes: Sequence of include header directives.
        :param methods: Sequence of pure virtual CppMethod objects.
        :param base_classes: Sequence of base classes if any.
        :param header_path: Original path to the interface header file.
    '''

    name: str
    namespace: str = ''
    includes: tuple[str, ...] = ()
    methods: tuple[CppMethod, ...] = ()
    base_classes: tuple[str, ...] = ()
    header_path: str = ''

    @property
    def clean_name(self) -> str:
        '''
            Returns class name without leading 'I' if followed by uppercase letter,
            e.g. ISerialPort -> SerialPort, Reader -> Reader.
        '''
        if len(self.name) > 1 and self.name.startswith('I') and self.name[1].isupper():
            return self.name[1:]
        return self.name

    @property
    def mock_class_name(self) -> str:
        '''
            Returns GoogleMock class name, e.g. MockSerialPort.
        '''
        return f'Mock{self.clean_name}'

    @property
    def fake_class_name(self) -> str:
        '''
            Returns Fake class name, e.g. FakeSerialPort.
        '''
        return f'Fake{self.clean_name}'

    @property
    def test_class_name(self) -> str:
        '''
            Returns GoogleTest fixture class name, e.g. SerialPortTest.
        '''
        return f'{self.clean_name}Test'

    @property
    def snake_name(self) -> str:
        '''
            Converts clean name into snake_case, e.g. SerialPort -> serial_port.
        '''
        s1 = sub('(.)([A-Z][a-z]+)', r'\1_\2', self.clean_name)
        return sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @property
    def full_qualified_name(self) -> str:
        '''
            Returns fully qualified C++ name including namespace.
        '''
        if self.namespace:
            return f'{self.namespace}::{self.name}'
        return self.name
