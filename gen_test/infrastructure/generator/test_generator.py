# -*- coding: UTF-8 -*-

'''
Module
    test_generator.py
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
    Concrete synthesizer for GoogleTest C++ unit test files using template.
'''

from __future__ import annotations

from os.path import dirname, join
from string import Template
from ats_utilities.utils.reflection import to_str

from gen_test.core.model.cpp_interface import CppInterface
from gen_test.core.model.cpp_method import CppMethod

from gen_test.infrastructure.generator.template_provider import TemplateProvider

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_test/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestGenerator:
    '''
        Synthesizer for GoogleTest C++ unit test files using template interpolation.

        It defines:

            :methods:
                | generate - Generates GoogleTest C++ test source code.
                | is_initialized - Checks if generator is initialized.
                | __str__ - Returns string representation of generator.
    '''

    def __init__(
        self,
        template_provider: TemplateProvider | None = None,
        template_path: str | None = None
    ) -> None:
        '''
            Initializes TestGenerator adapter.

            :param template_provider: Optional custom template provider.
            :param template_path: Optional custom template file path.
        '''
        self._provider: TemplateProvider = template_provider or TemplateProvider()
        self._template_path: str | None = template_path
        self._initialized: bool = True

    def generate(self, interface: CppInterface, mock_header_name: str) -> str:
        '''
            Synthesizes GoogleTest C++ test file code.

            :param interface: Parsed CppInterface model.
            :param mock_header_name: File name of mock header to include.
            :return: Generated C++ test code string.
        '''
        if self._template_path:
            with open(self._template_path, 'r', encoding='utf-8') as handle:
                raw_template = handle.read()
        else:
            raw_template = self._provider.get_template('test')

        template = Template(raw_template)

        test_ns = f'{interface.namespace}::testing' if interface.namespace else 'testing'
        ns_open = f'namespace {test_ns} {{\n'
        ns_close = f'\n}}  // namespace {test_ns}'

        test_cases_list: list[str] = []
        for method in interface.methods:
            test_cases_list.extend(self._generate_test_case(interface, method))
            test_cases_list.append('')

        test_cases = '\n'.join(test_cases_list).rstrip()

        mapping = {
            'MOCK_HEADER': mock_header_name,
            'TEST_NAMESPACE_OPEN': ns_open,
            'TEST_NAMESPACE_CLOSE': ns_close,
            'TEST_FIXTURE_CLASS': interface.test_class_name,
            'MOCK_CLASS': interface.mock_class_name,
            'TEST_CASES': test_cases
        }

        return template.safe_substitute(mapping)

    def is_initialized(self) -> bool:
        '''
            Checks if generator is initialized.

            :return: True.
        '''
        return self._initialized

    def _generate_test_case(self, interface: CppInterface, method: CppMethod) -> list[str]:
        '''
            Generates a TEST_F unit test case for a method.
        '''
        test_case_name = f'Calls{method.name.capitalize()}'
        matchers = ', '.join('::testing::_' for _ in method.parameters)
        dummy_args = ', '.join(self._get_dummy_arg(p_type) for p_type, _ in method.parameters)

        lines: list[str] = [
            f'TEST_F({interface.test_class_name}, {test_case_name}) {{'
        ]

        if method.is_void:
            lines.append(f'  EXPECT_CALL(mock, {method.name}({matchers})).Times(1);')
            lines.append(f'  mock.{method.name}({dummy_args});')
        else:
            default_val = method.default_return_value
            lines.append(
                f'  EXPECT_CALL(mock, {method.name}({matchers}))'
                f'.WillOnce(::testing::Return({default_val}));'
            )
            if method.return_type.strip() == 'bool':
                lines.append(f'  EXPECT_TRUE(mock.{method.name}({dummy_args}));')
            else:
                lines.append(f'  EXPECT_EQ(mock.{method.name}({dummy_args}), {default_val});')

        lines.append('}')
        return lines

    def _get_dummy_arg(self, param_type: str) -> str:
        '''
            Returns a dummy value for calling the method in a test.
        '''
        ptype = param_type.strip()
        if '*' in ptype:
            return 'nullptr'
        if ptype in ('int', 'short', 'long', 'size_t', 'uint8_t', 'uint16_t', 'uint32_t', 'uint64_t'):
            return '0'
        if ptype in ('float', 'double'):
            return '0.0'
        if ptype == 'bool':
            return 'false'
        if 'std::string' in ptype:
            return '""'
        return '{}'

    def __str__(self) -> str:
        '''
            Returns string representation of the generator.
        '''
        return to_str(self)
