# -*- coding: UTF-8 -*-

'''
Module
    test_suite_config_test.py
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
    Unit tests for TestSuiteConfig model.
'''

from __future__ import annotations

from unittest import TestCase

from gen_um_test.core.model.test_suite_config import TestSuiteConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_um_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_um_test/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTestSuiteConfig(TestCase):
    '''
        Unit tests for TestSuiteConfig model.
    '''

    def test_default_values(self) -> None:
        '''
            Tests default property values of TestSuiteConfig.
        '''
        config = TestSuiteConfig(
            interface_path='path/to/interface.h',
            output_dir='path/to/output'
        )
        self.assertEqual(config.interface_path, 'path/to/interface.h')
        self.assertEqual(config.output_dir, 'path/to/output')
        self.assertEqual(config.include_prefix, '')
        self.assertIsNone(config.interface_name)
        self.assertIsNone(config.cmake_target)
        self.assertTrue(config.generate_mock)
        self.assertTrue(config.generate_test)
        self.assertTrue(config.generate_fake)
        self.assertTrue(config.generate_cmake)
        self.assertTrue(config.generate_main)
        self.assertTrue(config.run_clang_format)

    def test_custom_values(self) -> None:
        '''
            Tests custom property values of TestSuiteConfig.
        '''
        config = TestSuiteConfig(
            interface_path='path/to/interface.h',
            output_dir='path/to/output',
            generate_fake=False,
            cmake_target='my_test'
        )
        self.assertFalse(config.generate_fake)
        self.assertEqual(config.cmake_target, 'my_test')
