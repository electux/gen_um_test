# -*- coding: UTF-8 -*-

'''
Module
    validator_test.py
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
    Unit tests for CLIBundleValidator class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.option.imanager import IOptionManager

from gen_test.infrastructure.cli.setup.bundle import CLIBundle
from gen_test.infrastructure.cli.setup.validator import CLIBundleValidator


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


class TestCLIBundleValidator(TestCase):
    '''
        Unit tests for CLIBundleValidator.
    '''

    def test_validate_success(self) -> None:
        '''
            Tests successful bundle validation.
        '''
        service = DummyService()
        parser = Mock(spec=IOptionManager)
        bundle = CLIBundle(service=service, parser=parser, commands=[])
        CLIBundleValidator.validate(bundle)
        self.assertTrue(CLIBundleValidator.is_valid(bundle))

    def test_validate_none_or_invalid_type(self) -> None:
        '''
            Tests failure when bundle is None or invalid type.
        '''
        with self.assertRaises(ATSValueError):
            CLIBundleValidator.validate(None)  # type: ignore[arg-type]
        self.assertFalse(CLIBundleValidator.is_valid(None))  # type: ignore[arg-type]

        with self.assertRaises(ATSTypeError):
            CLIBundleValidator.validate('invalid')  # type: ignore[arg-type]
        self.assertFalse(CLIBundleValidator.is_valid('invalid'))  # type: ignore[arg-type]
