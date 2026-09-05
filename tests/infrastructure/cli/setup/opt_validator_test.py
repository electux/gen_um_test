# -*- coding: UTF-8 -*-

'''
Module
    opt_validator_test.py
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
    Unit tests for CLIBundleOptionsValidator class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.option.imanager import IOptionManager

from gen_um_test.infrastructure.cli.setup.opt_validator import CLIBundleOptionsValidator
from gen_um_test.infrastructure.cli.setup.options import CLIBundleOptions


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


class TestCLIBundleOptionsValidator(TestCase):
    '''
        Unit tests for CLIBundleOptionsValidator.
    '''

    def test_validate_success(self) -> None:
        '''
            Tests successful options validation.
        '''
        opts: CLIBundleOptions = {
            'service': DummyService(),
            'parser': Mock(spec=IOptionManager)
        }
        CLIBundleOptionsValidator.validate(opts)
        self.assertTrue(CLIBundleOptionsValidator.is_valid(opts))

    def test_validate_none_or_invalid(self) -> None:
        '''
            Tests failure on None or invalid options.
        '''
        with self.assertRaises(ATSValueError):
            CLIBundleOptionsValidator.validate(None)  # type: ignore[arg-type]
        self.assertFalse(CLIBundleOptionsValidator.is_valid(None))  # type: ignore[arg-type]

        with self.assertRaises(ATSTypeError):
            CLIBundleOptionsValidator.validate('invalid')  # type: ignore[arg-type]
        self.assertFalse(CLIBundleOptionsValidator.is_valid('invalid'))  # type: ignore[arg-type]
