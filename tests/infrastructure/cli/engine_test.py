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
    Unit tests for CLI class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.exceptions import ATSRuntimeError
from ats_utilities.option.imanager import IOptionManager

from gen_um_test.infrastructure.cli.engine import CLI
from gen_um_test.infrastructure.cli.setup.bundle import CLIBundle
from gen_um_test.infrastructure.command.command import CommandBundle


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


class TestCLI(TestCase):
    '''
        Unit tests for CLI class.
    '''

    def test_cli_run_success(self) -> None:
        '''
            Tests CLI running command successfully.
        '''
        service = DummyService()
        parser = Mock(spec=IOptionManager)
        parser.parse_command.return_value = ('test_cmd', {'arg': 'val'})

        mock_def = Mock()
        mock_def.name = 'test_cmd'
        mock_exec = Mock()
        mock_exec.execute.return_value = {'returncode': 0, 'stdout': 'ok', 'stderr': ''}

        cmd_bundle = CommandBundle(definition=mock_def, executor=mock_exec)
        cli_bundle = CLIBundle(service=service, parser=parser, commands=[cmd_bundle])

        cli = CLI(cli_bundle)
        self.assertTrue(cli.is_initialized())
        self.assertIn('CLI', str(cli))

        res = cli.run()
        self.assertEqual(res['returncode'], 0)
        self.assertEqual(res['stdout'], 'ok')

    def test_cli_run_command_not_found(self) -> None:
        '''
            Tests CLI when parsed command is not recognized.
        '''
        service = DummyService()
        parser = Mock(spec=IOptionManager)
        parser.parse_command.return_value = ('unknown_cmd', {})

        cli_bundle = CLIBundle(service=service, parser=parser, commands=[])
        cli = CLI(cli_bundle)
        res = cli.run()
        self.assertEqual(res['returncode'], 1)
        self.assertIn('command not found', str(res['stderr']))

    def test_cli_run_exception(self) -> None:
        '''
            Tests CLI exception handling during run.
        '''
        service = DummyService()
        parser = Mock(spec=IOptionManager)
        parser.parse_command.side_effect = ATSRuntimeError('failed to parse')

        cli_bundle = CLIBundle(service=service, parser=parser, commands=[])
        cli = CLI(cli_bundle)
        res = cli.run()
        self.assertEqual(res['returncode'], 1)
        self.assertIn('failed to parse', str(res['stderr']))
