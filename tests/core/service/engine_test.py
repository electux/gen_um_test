# -*- coding: UTF-8 -*-

'''
Module
    engine_test.py
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
    Unit tests for core Service class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.exceptions import ATSTypeError, ATSValueError

from gen_um_test.core.model.generation_result import GenerationResult
from gen_um_test.core.model.test_suite_config import TestSuiteConfig
from gen_um_test.core.service.engine import Service


class DummySubProcessor:
    '''
        Mock dummy subprocessor implementing ISubProcessor protocol.
    '''

    def run(self, *, params: TestSuiteConfig) -> GenerationResult:
        '''
            Executes dummy run.
        '''
        return GenerationResult(
            success=True,
            output_dir=params.output_dir,
            generated_files=(),
            message='dummy'
        )

    def is_initialized(self) -> bool:
        '''
            Checks dummy initialization.
        '''
        return True


class TestService(TestCase):
    '''
        Unit tests for core Service class.
    '''

    def test_service_initialization_success(self) -> None:
        '''
            Tests successful Service initialization.
        '''
        sub = DummySubProcessor()
        srv = Service(subprocessor=sub)
        self.assertTrue(srv.is_initialized())
        self.assertIn('Service', str(srv))

    def test_service_initialization_errors(self) -> None:
        '''
            Tests validation errors during initialization.
        '''
        with self.assertRaises(ATSValueError):
            Service(subprocessor=None)  # type: ignore[arg-type]

        with self.assertRaises(ATSTypeError):
            Service(subprocessor="invalid")  # type: ignore[arg-type]

    def test_generate_suite(self) -> None:
        '''
            Tests generate_suite delegation.
        '''
        sub = DummySubProcessor()
        expected = GenerationResult(success=True, output_dir='out', generated_files=(), message='ok')
        sub.run = Mock(return_value=expected)

        srv = Service(subprocessor=sub)
        cfg = TestSuiteConfig(interface_path='I.h', output_dir='out')
        res = srv.generate_suite(cfg)
        self.assertEqual(res, expected)
        sub.run.assert_called_once_with(params=cfg)

    def test_generate_mock(self) -> None:
        '''
            Tests generate_mock delegation.
        '''
        sub = DummySubProcessor()
        expected = GenerationResult(success=True, output_dir='out', generated_files=(), message='mock')
        sub.run = Mock(return_value=expected)

        srv = Service(subprocessor=sub)
        cfg = TestSuiteConfig(interface_path='I.h', output_dir='out')
        res = srv.generate_mock(cfg)
        self.assertEqual(res, expected)

    def test_generate_test(self) -> None:
        '''
            Tests generate_test delegation.
        '''
        sub = DummySubProcessor()
        expected = GenerationResult(success=True, output_dir='out', generated_files=(), message='test')
        sub.run = Mock(return_value=expected)

        srv = Service(subprocessor=sub)
        cfg = TestSuiteConfig(interface_path='I.h', output_dir='out')
        res = srv.generate_test(cfg)
        self.assertEqual(res, expected)

    def test_generate_fake(self) -> None:
        '''
            Tests generate_fake delegation.
        '''
        sub = DummySubProcessor()
        expected = GenerationResult(success=True, output_dir='out', generated_files=(), message='fake')
        sub.run = Mock(return_value=expected)

        srv = Service(subprocessor=sub)
        cfg = TestSuiteConfig(interface_path='I.h', output_dir='out')
        res = srv.generate_fake(cfg)
        self.assertEqual(res, expected)

    def test_generate_cmake(self) -> None:
        '''
            Tests generate_cmake delegation.
        '''
        sub = DummySubProcessor()
        expected = GenerationResult(success=True, output_dir='out', generated_files=(), message='cmake')
        sub.run = Mock(return_value=expected)

        srv = Service(subprocessor=sub)
        cfg = TestSuiteConfig(interface_path='I.h', output_dir='out')
        res = srv.generate_cmake(cfg)
        self.assertEqual(res, expected)
