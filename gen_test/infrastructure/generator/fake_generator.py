# -*- coding: UTF-8 -*-

'''
Module
    fake_generator.py
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
    Concrete synthesizer for Fake in-memory stub C++ header files using template.
'''

from __future__ import annotations

from os.path import basename, dirname, join
from string import Template

from ats_utilities.utils.reflection import to_str

from gen_test.core.model.cpp_interface import CppInterface
from gen_test.core.model.cpp_method import CppMethod
from gen_test.infrastructure.generator.template_provider import TemplateProvider

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_test/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FakeGenerator:
    '''
        Synthesizer for Fake in-memory stub C++ header files using template interpolation.

        It defines:

            :methods:
                | generate - Synthesizes Fake C++ header code.
                | is_initialized - Checks if generator is initialized.
                | __str__ - Returns string representation of generator.
    '''

    def __init__(
        self,
        template_provider: TemplateProvider | None = None,
        template_path: str | None = None
    ) -> None:
        '''
            Initializes FakeGenerator adapter.

            :param template_provider: Optional custom template provider.
            :param template_path: Optional custom template file path.
        '''
        self._provider: TemplateProvider = template_provider or TemplateProvider()
        self._template_path: str | None = template_path
        self._initialized: bool = True

    def generate(self, interface: CppInterface, include_prefix: str = '') -> str:
        '''
            Synthesizes Fake C++ header code.

            :param interface: Parsed CppInterface model.
            :param include_prefix: Optional custom include prefix for interface header.
            :return: Generated C++ header string.
        '''
        header_file = basename(interface.header_path) if interface.header_path else f'{interface.name}.h'
        include_path = f'{include_prefix.rstrip("/")}/{header_file}' if include_prefix else header_file

        if self._template_path:
            with open(self._template_path, 'r', encoding='utf-8') as handle:
                raw_template = handle.read()
        else:
            raw_template = self._provider.get_template('fake')

        template = Template(raw_template)

        ns_open = f'namespace {interface.namespace} {{\n' if interface.namespace else ''
        ns_close = f'\n}}  // namespace {interface.namespace}' if interface.namespace else ''

        call_counters = '\n'.join(
            f'  mutable size_t {m.name}_calls{{0}};' for m in interface.methods
        )

        stub_methods_list: list[str] = []
        for m in interface.methods:
            stub_methods_list.extend(self._generate_stub_method(m))
            stub_methods_list.append('')

        stub_methods = '\n'.join(stub_methods_list).rstrip()

        mapping = {
            'INCLUDE_PATH': include_path,
            'NAMESPACE_OPEN': ns_open,
            'NAMESPACE_CLOSE': ns_close,
            'FAKE_CLASS': interface.fake_class_name,
            'INTERFACE_NAME': interface.name,
            'CALL_COUNTERS': call_counters,
            'STUB_METHODS': stub_methods
        }

        return template.safe_substitute(mapping)

    def is_initialized(self) -> bool:
        '''
            Checks if generator is initialized.

            :return: True.
        '''
        return self._initialized

    def _generate_stub_method(self, method: CppMethod) -> list[str]:
        '''
            Generates stub implementation for a method.
        '''
        qualifiers = []
        if method.is_const:
            qualifiers.append('const')
        if method.is_noexcept:
            qualifiers.append('noexcept')
        qualifiers.append('override')
        qual_str = ' '.join(qualifiers)

        signature = f'  {method.return_type} {method.name}({method.params_signature}) {qual_str} {{'
        lines = [signature, f'    ++{method.name}_calls;']

        if not method.is_void:
            default_val = method.default_return_value
            lines.append(f'    return {default_val};')

        lines.append('  }')
        return lines

    def __str__(self) -> str:
        '''
            Returns string representation of the generator.
        '''
        return to_str(self)
