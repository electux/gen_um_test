# -*- coding: UTF-8 -*-

'''
Module
    cpp_parser.py
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
    Concrete implementation of C++ interface parser.
'''

from __future__ import annotations

from os.path import isfile
from re import DOTALL, MULTILINE, Pattern, compile as re_compile, sub as re_sub

from ats_utilities.exceptions import ATSValueError
from ats_utilities.utils.reflection import to_str
from ats_utilities.validation.check_value import not_none

from gen_test.core.model.cpp_interface import CppInterface
from gen_test.core.model.cpp_method import CppMethod

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_test/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CppParser:
    '''
        Concrete adapter parsing C++ interface header files into domain models.

        It defines:

            :methods:
                | parse_file - Reads and parses a C++ header file.
                | parse_source - Parses raw C++ text.
                | is_initialized - Checks if parser is initialized.
                | __str__ - Returns string representation of parser.
    '''

    _COMMENT_RE: Pattern[str] = re_compile(r'//.*?$|/\*.*?\*/', DOTALL | MULTILINE)
    _INCLUDE_RE: Pattern[str] = re_compile(r'^\s*#include\s+([<"][^>"]+[>"])', MULTILINE)
    _NAMESPACE_RE: Pattern[str] = re_compile(r'namespace\s+([a-zA-Z0-9_:]+)\s*\{')
    _CLASS_RE: Pattern[str] = re_compile(
        r'(?:class|struct)\s+([A-Za-z0-9_]+)(?:\s*:\s*public\s+([A-Za-z0-9_:]+))?\s*\{([^}]*)\};',
        DOTALL
    )
    _PURE_VIRTUAL_RE: Pattern[str] = re_compile(
        r'virtual\s+([\w\s:*&<>]+?)\s+([A-Za-z0-9_]+)\s*\((.*?)\)\s*(const)?\s*(noexcept)?\s*=\s*0\s*;',
        MULTILINE
    )

    def __init__(self) -> None:
        '''
            Initializes CppParser adapter.
        '''
        self._initialized: bool = True

    def parse_file(self, file_path: str) -> tuple[CppInterface, ...]:
        '''
            Parses C++ interface header file.

            :param file_path: Absolute or relative path to C++ header.
            :return: Tuple of parsed CppInterface instances.
            :exceptions:
                | ATSValueError: When file does not exist.
        '''
        ctx: str = 'cpp_parser::parse_file(...)'
        not_none(file_path, ctx, 'file path must be provided')
        if not isfile(file_path):
            raise ATSValueError(f'file not found: {file_path}')

        with open(file_path, 'r', encoding='utf-8', errors='replace') as handle:
            content = handle.read()

        return self.parse_source(content, file_path=file_path)

    def parse_source(self, content: str, file_path: str = '') -> tuple[CppInterface, ...]:
        '''
            Parses C++ source content string.

            :param content: Raw C++ source code.
            :param file_path: Source file path for reference.
            :return: Tuple of parsed CppInterface instances.
            :exceptions: None.
        '''
        if not content:
            return ()

        clean_code = self._strip_comments(content)
        includes = tuple(self._INCLUDE_RE.findall(clean_code))
        namespace = self._extract_namespace(clean_code)

        interfaces: list[CppInterface] = []
        for match in self._CLASS_RE.finditer(clean_code):
            class_name = match.group(1).strip()
            base_class = match.group(2).strip() if match.group(2) else ''
            body = match.group(3)

            methods = self._extract_methods(body)
            if methods:
                base_classes = (base_class,) if base_class else ()
                interfaces.append(
                    CppInterface(
                        name=class_name,
                        namespace=namespace,
                        includes=includes,
                        methods=tuple(methods),
                        base_classes=base_classes,
                        header_path=file_path
                    )
                )

        return tuple(interfaces)

    def is_initialized(self) -> bool:
        '''
            Checks if parser is initialized.

            :return: True.
        '''
        return self._initialized

    def _strip_comments(self, code: str) -> str:
        '''
            Removes single-line and multi-line comments from C++ code.
        '''
        return self._COMMENT_RE.sub('', code)

    def _extract_namespace(self, code: str) -> str:
        '''
            Extracts namespace definition from code, e.g. "acme::hardware".
        '''
        ns_matches = self._NAMESPACE_RE.findall(code)
        if ns_matches:
            return '::'.join(ns_matches)
        return ''

    def _extract_methods(self, body: str) -> list[CppMethod]:
        '''
            Extracts pure virtual methods from class body.
        '''
        methods: list[CppMethod] = []
        for match in self._PURE_VIRTUAL_RE.finditer(body):
            ret_type = match.group(1).strip()
            # If "virtual" captured in return type, strip it
            ret_type = re_sub(r'\bvirtual\b', '', ret_type).strip()
            method_name = match.group(2).strip()
            params_raw = match.group(3).strip()
            is_const = bool(match.group(4))
            is_noexcept = bool(match.group(5))

            parsed_params = self._parse_parameters(params_raw)
            methods.append(
                CppMethod(
                    name=method_name,
                    return_type=ret_type,
                    parameters=tuple(parsed_params),
                    is_const=is_const,
                    is_noexcept=is_noexcept
                )
            )
        return methods

    def _parse_parameters(self, params_raw: str) -> list[tuple[str, str]]:
        '''
            Parses raw parameter string into list of (type, name) tuples.
        '''
        if not params_raw or params_raw.strip() == 'void':
            return []

        results: list[tuple[str, str]] = []
        parts = self._split_parameters(params_raw)
        for part in parts:
            item = part.strip()
            if not item:
                continue
            # Remove default arguments, e.g. "int timeout = 1000" -> "int timeout"
            if '=' in item:
                item = item.split('=', 1)[0].strip()

            # Split type and parameter name
            # Handle cases like "const uint8_t* buffer" or "size_t length"
            tokens = item.split()
            if len(tokens) == 1:
                results.append((tokens[0], ''))
            else:
                param_name = tokens[-1]
                param_type = ' '.join(tokens[:-1])
                # Handle pointer/ref attached to param name: "uint8_t *data" or "int &ref"
                if param_name.startswith('*') or param_name.startswith('&'):
                    prefix = param_name[0]
                    param_name = param_name[1:]
                    param_type = f'{param_type}{prefix}'
                results.append((param_type.strip(), param_name.strip()))

        return results

    def _split_parameters(self, params_raw: str) -> list[str]:
        '''
            Splits parameter string respecting template angle brackets.
        '''
        parts: list[str] = []
        depth = 0
        current: list[str] = []
        for char in params_raw:
            if char == '<':
                depth += 1
            elif char == '>':
                depth -= 1
            elif char == ',' and depth == 0:
                parts.append(''.join(current))
                current = []
                continue
            current.append(char)
        if current:
            parts.append(''.join(current))
        return parts

    def __str__(self) -> str:
        '''
            Returns string representation of the parser.
        '''
        return to_str(self)
