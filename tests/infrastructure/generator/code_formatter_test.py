# -*- coding: UTF-8 -*-

'''
Module
    code_formatter_test.py
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
    Unit tests for CodeFormatter class.
'''

from __future__ import annotations

from os import remove
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest.mock import patch

from gen_test.infrastructure.generator.code_formatter import CodeFormatter


class TestCodeFormatter(TestCase):
    '''
        Unit tests for CodeFormatter class.
    '''

    def test_formatter_initialization_and_str(self) -> None:
        '''
            Tests formatter initialization and string representation.
        '''
        formatter = CodeFormatter()
        self.assertTrue(formatter.is_initialized())
        self.assertIn('CodeFormatter', str(formatter))

    def test_format_file_real_or_stub(self) -> None:
        '''
            Tests formatting a real temporary file.
        '''
        formatter = CodeFormatter()
        with NamedTemporaryFile(mode='w', suffix='.h', delete=False) as temp:
            temp.write('int   main ( ) { return 0 ; }\n')
            temp_path = temp.name

        try:
            res = formatter.format_file(temp_path)
            self.assertTrue(res)
        finally:
            if exists(temp_path):
                remove(temp_path)

    def test_format_file_no_tool(self) -> None:
        '''
            Tests when clang-format is not available.
        '''
        formatter = CodeFormatter()
        formatter._formatter_path = None
        self.assertTrue(formatter.format_file('any_file.h'))

    def test_format_file_exception(self) -> None:
        '''
            Tests exception handling in format_file.
        '''
        formatter = CodeFormatter()
        with patch('gen_test.infrastructure.generator.code_formatter.run_process') as mock_run:
            mock_run.side_effect = OSError('Execution failed')
            self.assertFalse(formatter.format_file('any_file.h'))
