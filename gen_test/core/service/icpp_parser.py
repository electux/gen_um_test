# -*- coding: UTF-8 -*-

'''
Module
    icpp_parser.py
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
    Defines abstract interface for C++ interface parser.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from gen_test.core.model.cpp_interface import CppInterface

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_test/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICppParser(Protocol):
    '''
        Defines abstract interface for C++ interface parser.

        It defines:

            :methods:
                | parse_file - Parses C++ interface header file.
                | parse_source - Parses C++ source code text.
                | is_initialized - Checks if parser is initialized.
    '''

    def parse_file(self, file_path: str) -> tuple[CppInterface, ...]:
        '''
            Parses C++ interface header file and returns discovered interfaces.

            :param file_path: Path to the C++ header file.
            :return: Tuple of parsed CppInterface models.
            :exceptions: None.
        '''

    def parse_source(self, content: str, file_path: str = '') -> tuple[CppInterface, ...]:
        '''
            Parses C++ source code text and returns discovered interfaces.

            :param content: C++ source text.
            :param file_path: Optional source file path for metadata.
            :return: Tuple of parsed CppInterface models.
            :exceptions: None.
        '''

    def is_initialized(self) -> bool:
        '''
            Checks if parser is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
