# -*- coding: UTF-8 -*-

'''
Module
    dep_validator_test.py
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
    Unit tests for CLIBundleDependenciesValidator class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.option.imanager import IOptionManager

from gen_um_test.infrastructure.cli.setup.dep_validator import CLIBundleDependenciesValidator
from gen_um_test.infrastructure.cli.setup.dependencies import CLIBundleDependencies


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


class TestCLIBundleDependenciesValidator(TestCase):
    '''
        Unit tests for CLIBundleDependenciesValidator.
    '''

    def test_validate_success(self) -> None:
        '''
            Tests successful dependencies validation.
        '''
        deps: CLIBundleDependencies = {
            'service': DummyService(),
            'parser': Mock(spec=IOptionManager),
            'commands': []
        }
        CLIBundleDependenciesValidator.validate(deps)
        self.assertTrue(CLIBundleDependenciesValidator.is_valid(deps))

    def test_validate_none_or_missing(self) -> None:
        '''
            Tests failure on None or missing dependencies.
        '''
        with self.assertRaises(ATSValueError):
            CLIBundleDependenciesValidator.validate(None)  # type: ignore[arg-type]
        self.assertFalse(CLIBundleDependenciesValidator.is_valid(None))  # type: ignore[arg-type]

        with self.assertRaises(ATSTypeError):
            CLIBundleDependenciesValidator.validate('invalid')  # type: ignore[arg-type]
        self.assertFalse(CLIBundleDependenciesValidator.is_valid('invalid'))  # type: ignore[arg-type]
