# -*- coding: UTF-8 -*-

'''
Module
    keys_test.py
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
    Unit tests for GenTestBundleKeys class.
'''

from __future__ import annotations

from unittest import TestCase

from gen_test.setup.keys import GenTestBundleKeys


class TestGenTestBundleKeys(TestCase):
    '''
        Unit tests for GenTestBundleKeys.
    '''

    def test_constants_and_types_mappings(self) -> None:
        '''
            Tests constants and type mappings of GenTestBundleKeys.
        '''
        self.assertEqual(GenTestBundleKeys.DEPENDENCY_BASE, 'base')
        self.assertEqual(GenTestBundleKeys.DEPENDENCY_SERVICE, 'service')
        self.assertEqual(GenTestBundleKeys.DEPENDENCY_SUBPROCESSOR, 'subprocessor')
        self.assertEqual(GenTestBundleKeys.DEPENDENCY_CLI, 'cli')
        self.assertEqual(GenTestBundleKeys.OPTION_INFO_FILE, 'info_file')

        dep_types = GenTestBundleKeys.get_dependency_to_type()
        self.assertIn('base', dep_types)
        self.assertIn('service', dep_types)
        self.assertIn('subprocessor', dep_types)
        self.assertIn('cli', dep_types)

        opt_types = GenTestBundleKeys.get_option_to_type()
        self.assertIn('info_file', opt_types)
