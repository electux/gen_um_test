# -*- coding: UTF-8 -*-

'''
Module
    cpp_method.py
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
    Defines CppMethod domain model representing a C++ interface method.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_test/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class CppMethod:
    '''
        Domain model representing a C++ interface member method.

        :param name: Name of the method.
        :param return_type: Return type of the method.
        :param parameters: Sequence of (type, name) tuples for parameters.
        :param is_const: Whether the method is const qualified.
        :param is_noexcept: Whether the method is noexcept qualified.
    '''

    name: str
    return_type: str
    parameters: tuple[tuple[str, str], ...] = ()
    is_const: bool = False
    is_noexcept: bool = False

    @property
    def params_signature(self) -> str:
        '''
            Returns parameter signature string, e.g. "int a, const std::string& b".
        '''
        return ', '.join(
            f'{param_type} {param_name}'.strip()
            for param_type, param_name in self.parameters
        )

    @property
    def params_call(self) -> str:
        '''
            Returns parameter names string for forwarding calls, e.g. "a, b".
        '''
        return ', '.join(param_name for _, param_name in self.parameters if param_name)

    @property
    def is_void(self) -> bool:
        '''
            Returns True if method returns void.
        '''
        return self.return_type.strip() == 'void'

    @property
    def default_return_value(self) -> str:
        '''
            Returns sensible default return value for stub/fake implementations.
        '''
        ret = self.return_type.strip()
        if ret == 'void':
            return ''
        if ret == 'bool':
            return 'true'
        int_types = (
            'int', 'short', 'long', 'long long', 'size_t', 'uint8_t',
            'uint16_t', 'uint32_t', 'uint64_t', 'int8_t', 'int16_t', 'int32_t', 'int64_t'
        )
        if ret in int_types:
            return '0'
        if ret in ('float', 'double'):
            return '0.0'
        if 'std::string' in ret:
            return '""'
        if '*' in ret:
            return 'nullptr'
        return '{}'
