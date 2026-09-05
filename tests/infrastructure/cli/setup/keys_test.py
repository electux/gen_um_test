# -*- coding: UTF-8 -*-

'''
Module
    keys_test.py
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
    Unit tests for CLIBundleKeys class.
'''

from __future__ import annotations

from unittest import TestCase

from gen_um_test.infrastructure.cli.setup.keys import CLIBundleKeys


class TestCLIBundleKeys(TestCase):
    '''
        Unit tests for CLIBundleKeys class.
    '''

    def test_constants_and_types_mappings(self) -> None:
        '''
            Tests constants and type mappings of CLIBundleKeys.
        '''
        self.assertEqual(CLIBundleKeys.DEPENDENCY_SERVICE, 'service')
        self.assertEqual(CLIBundleKeys.DEPENDENCY_PARSER, 'parser')
        self.assertEqual(CLIBundleKeys.DEPENDENCY_COMMANDS, 'commands')
        self.assertEqual(CLIBundleKeys.OPTION_SERVICE, 'service')
        self.assertEqual(CLIBundleKeys.OPTION_PARSER, 'parser')

        dep_types = CLIBundleKeys.get_dependency_to_type()
        self.assertIn('service', dep_types)
        self.assertIn('parser', dep_types)
        self.assertIn('commands', dep_types)

        opt_types = CLIBundleKeys.get_option_to_type()
        self.assertIn('service', opt_types)
        self.assertIn('parser', opt_types)
