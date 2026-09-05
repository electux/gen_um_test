# -*- coding: UTF-8 -*-

'''
Module
    ifake_generator.py
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
    Defines abstract interface for Fake stub synthesizer.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from gen_um_test.core.model.cpp_interface import CppInterface

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_um_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_um_test/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IFakeGenerator(Protocol):
    '''
        Defines abstract interface for Fake stub synthesizer.

        It defines:

            :methods:
                | generate - Synthesizes Fake in-memory stub C++ header code.
                | is_initialized - Checks if generator is initialized.
    '''

    def generate(self, interface: CppInterface, include_prefix: str = '') -> str:
        '''
            Synthesizes Fake in-memory stub header code.

            :param interface: Parsed CppInterface model.
            :param include_prefix: Optional custom include prefix for interface header.
            :return: Generated C++ header code.
            :exceptions: None.
        '''

    def is_initialized(self) -> bool:
        '''
            Checks if generator is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
