# -*- coding: UTF-8 -*-

'''
Module
    command_test.py
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
    Unit tests for CLI commands and executors.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from gen_test.core.model.generation_result import GenerationResult
from gen_test.infrastructure.command.cmake_command_definition import CMakeCommandDefinition
from gen_test.infrastructure.command.cmake_command_executor import CMakeCommandExecutor
from gen_test.infrastructure.command.command import CommandBundle
from gen_test.infrastructure.command.fake_command_definition import FakeCommandDefinition
from gen_test.infrastructure.command.fake_command_executor import FakeCommandExecutor
from gen_test.infrastructure.command.mock_command_definition import MockCommandDefinition
from gen_test.infrastructure.command.mock_command_executor import MockCommandExecutor
from gen_test.infrastructure.command.suite_command_definition import SuiteCommandDefinition
from gen_test.infrastructure.command.suite_command_executor import SuiteCommandExecutor
from gen_test.infrastructure.command.test_command_definition import TestCommandDefinition
from gen_test.infrastructure.command.test_command_executor import TestCommandExecutor


class TestCommands(TestCase):
    '''
        Unit tests for Command definitions and executors.
    '''

    def test_command_bundle_and_definitions(self) -> None:
        '''
            Tests instantiation and properties of command definitions.
        '''
        suite_def = SuiteCommandDefinition()
        suite_exec = SuiteCommandExecutor(suite_def)
        bundle = CommandBundle(definition=suite_def, executor=suite_exec)
        self.assertEqual(bundle.definition.name, 'suite')
        self.assertTrue(bool(bundle.definition.help_text))
        self.assertTrue(bool(bundle.definition.options))
        self.assertIn('SuiteCommandExecutor', str(bundle.executor))
        self.assertEqual(suite_exec.get_definition(), suite_def)

        mock_def = MockCommandDefinition()
        mock_exec = MockCommandExecutor(mock_def)
        self.assertEqual(mock_def.name, 'mock')
        self.assertIn('MockCommandExecutor', str(mock_exec))
        self.assertEqual(mock_exec.get_definition(), mock_def)

        test_def = TestCommandDefinition()
        test_exec = TestCommandExecutor(test_def)
        self.assertEqual(test_def.name, 'test')
        self.assertIn('TestCommandExecutor', str(test_exec))
        self.assertEqual(test_exec.get_definition(), test_def)

        fake_def = FakeCommandDefinition()
        fake_exec = FakeCommandExecutor(fake_def)
        self.assertEqual(fake_def.name, 'fake')
        self.assertIn('FakeCommandExecutor', str(fake_exec))
        self.assertEqual(fake_exec.get_definition(), fake_def)

        cmake_def = CMakeCommandDefinition()
        cmake_exec = CMakeCommandExecutor(cmake_def)
        self.assertEqual(cmake_def.name, 'cmake')
        self.assertIn('CMakeCommandExecutor', str(cmake_exec))
        self.assertEqual(cmake_exec.get_definition(), cmake_def)

    def test_executors_execution(self) -> None:
        '''
            Tests executing each command executor with mock service.
        '''
        mock_service = Mock()
        success_res = GenerationResult(success=True, output_dir='out', generated_files=(), message='ok')
        fail_res = GenerationResult(success=False, output_dir='out', generated_files=(), message='failed')

        params = {'interface': 'ISerialPort.h', 'output': 'out'}

        # Suite executor
        suite_exec = SuiteCommandExecutor(SuiteCommandDefinition())
        mock_service.generate_suite.return_value = success_res
        res = suite_exec.execute(params=params, service=mock_service)
        self.assertEqual(res['returncode'], 0)

        mock_service.generate_suite.return_value = fail_res
        res = suite_exec.execute(params=params, service=mock_service)
        self.assertEqual(res['returncode'], 1)

        # Mock executor
        mock_exec = MockCommandExecutor(MockCommandDefinition())
        mock_service.generate_mock.return_value = success_res
        res = mock_exec.execute(params=params, service=mock_service)
        self.assertEqual(res['returncode'], 0)

        # Test executor
        test_exec = TestCommandExecutor(TestCommandDefinition())
        mock_service.generate_test.return_value = success_res
        res = test_exec.execute(params=params, service=mock_service)
        self.assertEqual(res['returncode'], 0)

        # Fake executor
        fake_exec = FakeCommandExecutor(FakeCommandDefinition())
        mock_service.generate_fake.return_value = success_res
        res = fake_exec.execute(params=params, service=mock_service)
        self.assertEqual(res['returncode'], 0)

        # CMake executor
        cmake_exec = CMakeCommandExecutor(CMakeCommandDefinition())
        mock_service.generate_cmake.return_value = success_res
        res = cmake_exec.execute(params=params, service=mock_service)
        self.assertEqual(res['returncode'], 0)

    def test_executors_service_not_initialized(self) -> None:
        '''
            Tests executing executors when service is uninitialized.
        '''
        mock_service = Mock()
        mock_service.is_initialized.return_value = False
        params = {'interface': 'ISerialPort.h', 'output': 'out'}

        executors = (
            SuiteCommandExecutor(SuiteCommandDefinition()),
            MockCommandExecutor(MockCommandDefinition()),
            TestCommandExecutor(TestCommandDefinition()),
            FakeCommandExecutor(FakeCommandDefinition()),
            CMakeCommandExecutor(CMakeCommandDefinition())
        )

        for executor in executors:
            res = executor.execute(params=params, service=mock_service)
            self.assertEqual(res['returncode'], 1)
            self.assertEqual(res['stderr'], 'service not initialized')
