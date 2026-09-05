# -*- coding: UTF-8 -*-

'''
Module
    suite_command_definition.py
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
    Defines SuiteCommandDefinition class.
'''

from __future__ import annotations

from collections.abc import Sequence
from ats_utilities.option.command.data import OptionData
from ats_utilities.utils.reflection import to_str

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_um_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_um_test/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SuiteCommandDefinition:
    '''
        CLI subcommand metadata definition for generating complete C++ test suites.

        It defines:

            :methods:
                | name - Returns command name.
                | help_text - Returns command help text.
                | options - Returns sequence of command options.
                | __str__ - Returns string representation of definition.
    '''

    @property
    def name(self) -> str:
        '''
            Returns command name.
        '''
        return 'suite'

    @property
    def help_text(self) -> str:
        '''
            Returns command help text.
        '''
        return 'Generate complete C++ test suite (mock, test fixture, fake, cmake, main)'

    @property
    def options(self) -> Sequence[OptionData]:
        '''
            Returns command options.
        '''
        return [
            OptionData(
                name='--interface',
                help_text='Path to C++ interface header file (.h / .hpp)',
                action=None,
                default=None,
                required=True,
                choices=None,
                nargs=None
            ),
            OptionData(
                name='--output',
                help_text='Output directory for generated test suite',
                action=None,
                default='./tests',
                required=False,
                choices=None,
                nargs=None
            ),
            OptionData(
                name='--prefix',
                help_text='Include path prefix for interface header',
                action=None,
                default='',
                required=False,
                choices=None,
                nargs=None
            ),
            OptionData(
                name='--name',
                help_text='Specific interface name to generate if file contains multiple',
                action=None,
                default=None,
                required=False,
                choices=None,
                nargs=None
            ),
            OptionData(
                name='--target',
                help_text='Custom CMake target name',
                action=None,
                default=None,
                required=False,
                choices=None,
                nargs=None
            )
        ]

    def __str__(self) -> str:
        '''
            Returns string representation of definition.
        '''
        return to_str(self)
