# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for GenUmTestBundleFactory class.
'''

from __future__ import annotations

from unittest import TestCase

from ats_utilities.exceptions import ATSTypeError

from gen_um_test.setup.bundle import GenUmTestBundle
from gen_um_test.setup.factory import GenUmTestBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_um_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_um_test/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestGenUmTestBundleFactory(TestCase):
    '''
        Unit tests for GenUmTestBundleFactory.
    '''

    def test_create_bundle_default(self) -> None:
        '''
            Tests default bundle creation.
        '''
        bundle = GenUmTestBundleFactory.create_bundle()
        self.assertIsInstance(bundle, GenUmTestBundle)

    def test_create_bundle_with_options(self) -> None:
        '''
            Tests bundle creation with options.
        '''
        options = {'info_file': 'gen_um_test/infrastructure/config/gen_um_test.cfg'}
        bundle = GenUmTestBundleFactory.create_bundle(options)
        self.assertIsInstance(bundle, GenUmTestBundle)

    def test_create_bundle_invalid_options(self) -> None:
        '''
            Tests failure on invalid options.
        '''
        options = {'info_file': 123}
        with self.assertRaises(ATSTypeError):
            GenUmTestBundleFactory.create_bundle(options)  # type: ignore[arg-type]

    def test_get_version(self) -> None:
        '''
            Tests get_version method.
        '''
        self.assertEqual(GenUmTestBundleFactory.get_version(), '1.0.2')
