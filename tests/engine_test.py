# -*- coding: UTF-8 -*-

'''
Module
    engine_test.py
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
    Unit tests for GenTest root engine class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock, patch

from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.factory import ContextBundleFactory
from ats_utilities.exceptions import ATSValueError

from gen_test.core.service.iservice import IService
from gen_test.core.service.isubprocessor import ISubProcessor
from gen_test.engine import GenTest
from gen_test.infrastructure.cli.icli import ICLI
from gen_test.setup.bundle import GenTestBundle
from gen_test.setup.factory import GenTestBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_test/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyService(IService):
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

    def __str__(self) -> str:
        return 'DummyService'


class DummySubProcessor(ISubProcessor):
    '''
        Dummy subprocessor implementing ISubProcessor protocol.
    '''

    def run(self, *, params: object) -> object:
        return None

    def is_initialized(self) -> bool:
        return True

    def __str__(self) -> str:
        return 'DummySubProcessor'


class DummyCLI(ICLI):
    '''
        Dummy CLI implementing ICLI protocol.
    '''

    def __init__(self, return_code: int = 0, stderr: str = '') -> None:
        self.return_code = return_code
        self.stderr = stderr

    def run(self) -> dict[str, object]:
        return {'returncode': self.return_code, 'stderr': self.stderr}

    def is_initialized(self) -> bool:
        return True

    def __str__(self) -> str:
        return 'DummyCLI'


class TestGenTest(TestCase):
    '''
        Unit tests for GenTest engine.
    '''

    def test_engine_init_success(self) -> None:
        '''
            Tests engine successful initialization.
        '''
        bundle = GenTestBundleFactory.create_bundle()
        engine = GenTest(bundle)
        self.assertTrue(engine.is_initialized())

    def test_engine_init_fail_validation(self) -> None:
        '''
            Tests engine initialization failure on invalid bundle.
        '''
        engine = GenTest(None)  # type: ignore[arg-type]
        self.assertFalse(engine.is_initialized())

    def test_engine_process_success(self) -> None:
        '''
            Tests engine process execution returning True.
        '''
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='gen_test/infrastructure/config/gen_test.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI(return_code=0)

        bundle = GenTestBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )

        engine = GenTest(bundle)
        self.assertTrue(engine.is_initialized())
        self.assertTrue(engine.process())

    def test_engine_process_cli_failure(self) -> None:
        '''
            Tests engine process execution failure when CLI returns non-zero code.
        '''
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='gen_test/infrastructure/config/gen_test.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI(return_code=1, stderr='CLI error')

        bundle = GenTestBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )

        engine = GenTest(bundle)
        self.assertTrue(engine.is_initialized())
        self.assertFalse(engine.process())

    def test_engine_process_not_initialized(self) -> None:
        '''
            Tests engine process execution when not initialized.
        '''
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='gen_test/infrastructure/config/gen_test.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI()

        mock_base.option_manager.is_initialized = Mock(return_value=False)

        bundle = GenTestBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )

        engine = GenTest(bundle)
        self.assertFalse(engine.is_initialized())
        self.assertFalse(engine.process())

    def test_engine_process_exception(self) -> None:
        '''
            Tests engine process handling generic exception.
        '''
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='gen_test/infrastructure/config/gen_test.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI()
        dummy_cli.run = Mock(side_effect=Exception('Unexpected error'))

        bundle = GenTestBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )

        engine = GenTest(bundle)
        self.assertTrue(engine.is_initialized())
        self.assertFalse(engine.process())

    def test_engine_process_validation_exception(self) -> None:
        '''
            Tests engine process handling ATS validation exception.
        '''
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='gen_test/infrastructure/config/gen_test.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI()
        dummy_cli.run = Mock(side_effect=ATSValueError('Validation error in run'))

        bundle = GenTestBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )

        engine = GenTest(bundle)
        self.assertTrue(engine.is_initialized())
        self.assertFalse(engine.process())

    @patch('gen_test.setup.validator.GenTestBundleValidator.validate')
    def test_engine_init_generic_exception(self, mock_validate: Mock) -> None:
        '''
            Tests engine init handling unexpected exception in validator.
        '''
        mock_validate.side_effect = Exception('Unexpected generic validation error')

        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='gen_test/infrastructure/config/gen_test.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI()

        bundle = GenTestBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )

        engine = GenTest(bundle)
        self.assertFalse(engine.is_initialized())
