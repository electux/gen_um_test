# -*- coding: UTF-8 -*-

'''
Module
    registry_test.py
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
    Unit tests for CLIBundleRegistry class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.option.imanager import IOptionManager

from gen_test.infrastructure.cli.setup.dependencies import CLIBundleDependencies
from gen_test.infrastructure.cli.setup.registry import CLIBundleRegistry


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


class TestCLIBundleRegistry(TestCase):
    '''
        Unit tests for CLIBundleRegistry.
    '''

    def test_create_bundle_and_version(self) -> None:
        '''
            Tests creating CLIBundle via registry.
        '''
        deps: CLIBundleDependencies = {
            'service': DummyService(),
            'parser': Mock(spec=IOptionManager),
            'commands': []
        }
        bundle = CLIBundleRegistry.create_bundle(deps)
        self.assertIsNotNone(bundle)
        self.assertTrue(bool(CLIBundleRegistry.get_version()))
