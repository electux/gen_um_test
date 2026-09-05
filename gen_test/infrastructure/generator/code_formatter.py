# -*- coding: UTF-8 -*-

'''
Module
    code_formatter.py
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
    Adapter for formatting generated C++ files using clang-format.
'''

from __future__ import annotations

from shutil import which
from subprocess import run as run_process

from ats_utilities.utils.reflection import to_str

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_test/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CodeFormatter:
    '''
        Adapter for formatting generated C++ code files using clang-format.

        It defines:

            :methods:
                | format_file - Runs clang-format on specified file if tool is available.
                | is_initialized - Checks if formatter is initialized.
                | __str__ - Returns string representation of formatter.
    '''

    def __init__(self) -> None:
        '''
            Initializes CodeFormatter adapter.
        '''
        self._formatter_path: str | None = which('clang-format')
        self._initialized: bool = True

    def format_file(self, file_path: str) -> bool:
        '''
            Formats specified C++ file in-place using clang-format.

            :param file_path: Path to C++ file to format.
            :return: True if formatted successfully or tool not available, False on error.
            :exceptions: None.
        '''
        if not self._formatter_path:
            return True

        try:
            res = run_process(
                [self._formatter_path, '-i', file_path],
                check=False,
                capture_output=True
            )
            return res.returncode == 0
        except Exception:
            return False

    def is_initialized(self) -> bool:
        '''
            Checks if formatter is initialized.

            :return: True.
        '''
        return self._initialized

    def __str__(self) -> str:
        '''
            Returns string representation of the formatter.
        '''
        return to_str(self)
