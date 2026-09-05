# -*- coding: UTF-8 -*-

'''
Module
    main_generator.py
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
    Concrete synthesizer for test_main.cc test runner using template.
'''

from __future__ import annotations

from os.path import dirname, join
from ats_utilities.utils.reflection import to_str

from gen_test.infrastructure.generator.template_provider import TemplateProvider

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_test/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MainGenerator:
    '''
        Synthesizer for test_main.cc test runner using template file.

        It defines:

            :methods:
                | generate - Synthesizes test_main.cc content.
                | is_initialized - Checks if generator is initialized.
                | __str__ - Returns string representation of generator.
    '''

    def __init__(
        self,
        template_provider: TemplateProvider | None = None,
        template_path: str | None = None
    ) -> None:
        '''
            Initializes MainGenerator adapter.

            :param template_provider: Optional custom template provider.
            :param template_path: Optional custom template file path.
        '''
        self._provider: TemplateProvider = template_provider or TemplateProvider()
        self._template_path: str | None = template_path
        self._initialized: bool = True

    def generate(self) -> str:
        '''
            Synthesizes test_main.cc source code.

            :return: Generated C++ code string.
        '''
        if self._template_path:
            with open(self._template_path, 'r', encoding='utf-8') as handle:
                return handle.read()

        return self._provider.get_template('main')

    def is_initialized(self) -> bool:
        '''
            Checks if generator is initialized.

            :return: True.
        '''
        return self._initialized

    def __str__(self) -> str:
        '''
            Returns string representation of the generator.
        '''
        return to_str(self)
