# -*- coding: UTF-8 -*-

'''
Module
    test_command_executor.py
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
    Defines TestCommandExecutor class.
'''

from __future__ import annotations

from collections.abc import Mapping
from ats_utilities.utils.reflection import to_str

from gen_um_test.core.model.test_suite_config import TestSuiteConfig
from gen_um_test.core.service.iservice import IService
from gen_um_test.infrastructure.command.icommand_definition import ICommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_um_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_um_test/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCommandExecutor:
    '''
        Command executor strategy for generating GoogleTest unit test file.

        It defines:

            :methods:
                | execute - Executes the subcommand.
                | get_definition - Returns command definition metadata.
                | __str__ - Returns string representation of executor.
    '''

    definition: ICommandDefinition

    def __init__(self, definition: ICommandDefinition) -> None:
        '''
            Initializes TestCommandExecutor.

            :param definition: Command definition metadata.
        '''
        self.definition = definition

    def execute(self, *, params: Mapping[str, object], service: IService) -> Mapping[str, object]:
        '''
            Executes test subcommand.

            :param params: Subcommand parameters from CLI parser.
            :param service: Core service instance.
            :return: Execution result dictionary.
        '''
        if not service.is_initialized():
            return {'returncode': 1, 'stdout': '', 'stderr': 'service not initialized'}

        config = TestSuiteConfig(
            interface_path=str(params.get('interface') or ''),
            output_dir=str(params.get('output') or './tests'),
            include_prefix=str(params.get('prefix') or ''),
            interface_name=str(params.get('name')) if params.get('name') else None
        )

        res = service.generate_test(config)
        return {
            'returncode': 0 if res.success else 1,
            'stdout': res.message,
            'stderr': '' if res.success else res.message
        }

    def get_definition(self) -> ICommandDefinition:
        '''
            Returns command definition metadata.
        '''
        return self.definition

    def __str__(self) -> str:
        '''
            Returns string representation of executor.
        '''
        return to_str(self)
