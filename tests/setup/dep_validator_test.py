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
    Unit tests for GenUmTestBundleDependenciesValidator class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.exceptions import ATSTypeError, ATSValueError

from gen_um_test.setup.dep_validator import GenUmTestBundleDependenciesValidator
from gen_um_test.setup.dependencies import GenUmTestBundleDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_um_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_um_test/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


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


class DummySubProcessor:
    '''
        Dummy subprocessor implementing ISubProcessor protocol.
    '''

    def run(self, *, params: object) -> object:
        return None

    def is_initialized(self) -> bool:
        return True


class DummyCLI:
    '''
        Dummy CLI implementing ICLI protocol.
    '''

    def run(self) -> dict[str, object]:
        return {}

    def is_initialized(self) -> bool:
        return True


class TestGenUmTestBundleDependenciesValidator(TestCase):
    '''
        Unit tests for GenUmTestBundleDependenciesValidator.
    '''

    def test_validate_success(self) -> None:
        '''
            Tests successful dependency validation.
        '''
        mock_base = Mock(spec=BaseBundle)
        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI()

        deps: GenUmTestBundleDependencies = {
            'base': mock_base,
            'service': dummy_service,
            'subprocessor': dummy_subprocessor,
            'cli': dummy_cli
        }
        GenUmTestBundleDependenciesValidator.validate(deps)
        self.assertTrue(GenUmTestBundleDependenciesValidator.is_valid(deps))

    def test_validate_none_or_invalid_type(self) -> None:
        '''
            Tests failure when dependencies is None or wrong type.
        '''
        with self.assertRaises(ATSValueError):
            GenUmTestBundleDependenciesValidator.validate(None)  # type: ignore[arg-type]
        self.assertFalse(GenUmTestBundleDependenciesValidator.is_valid(None))  # type: ignore[arg-type]

        with self.assertRaises(ATSTypeError):
            GenUmTestBundleDependenciesValidator.validate('invalid')  # type: ignore[arg-type]
        self.assertFalse(GenUmTestBundleDependenciesValidator.is_valid('invalid'))  # type: ignore[arg-type]

    def test_validate_missing_dependency(self) -> None:
        '''
            Tests failure when a required dependency is missing.
        '''
        deps = {
            'base': Mock(spec=BaseBundle),
            'service': DummyService(),
            'subprocessor': DummySubProcessor()
        }
        with self.assertRaises(ATSValueError):
            GenUmTestBundleDependenciesValidator.validate(deps)  # type: ignore[arg-type]
        self.assertFalse(GenUmTestBundleDependenciesValidator.is_valid(deps))  # type: ignore[arg-type]
