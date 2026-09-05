# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for CLIBundleFactory class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.option.imanager import IOptionManager

from gen_test.infrastructure.cli.setup.factory import CLIBundleFactory
from gen_test.infrastructure.cli.setup.options import CLIBundleOptions


class DummyService:
    '''
        Dummy service implementing IService protocol.
    '''

    def generate_suite(self, config: object) -> object:
        return None

    def generate_mock(self, config: object) -> object:
        return None

    def generate_test(self, config: object) -> object:
        return None

    def generate_fake(self, config: object) -> object:
        return None

    def generate_cmake(self, config: object) -> object:
        return None

    def is_initialized(self) -> bool:
        return True


class TestCLIBundleFactory(TestCase):
    '''
        Unit tests for CLIBundleFactory.
    '''

    def test_create_bundle_and_version(self) -> None:
        '''
            Tests factory create_bundle with options.
        '''
        opts: CLIBundleOptions = {
            'service': DummyService(),
            'parser': Mock(spec=IOptionManager)
        }
        bundle = CLIBundleFactory.create_bundle(opts)
        self.assertIsNotNone(bundle)
        self.assertEqual(len(bundle.commands), 5)
        self.assertTrue(bool(CLIBundleFactory.get_version()))
