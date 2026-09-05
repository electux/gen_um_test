# -*- coding: UTF-8 -*-

'''
Module
    generation_result_test.py
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
    Unit tests for GenerationResult model.
'''

from __future__ import annotations

from unittest import TestCase

from gen_um_test.core.model.generation_result import GenerationResult

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_um_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_um_test/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestGenerationResult(TestCase):
    '''
        Unit tests for GenerationResult model.
    '''

    def test_result_creation_and_to_dict(self) -> None:
        '''
            Tests GenerationResult properties and to_dict conversion.
        '''
        res = GenerationResult(
            success=True,
            output_dir='/path/out',
            generated_files=('mock.h', 'test.cc'),
            message='done'
        )
        self.assertTrue(res.success)
        self.assertEqual(res.output_dir, '/path/out')
        self.assertEqual(res.generated_files, ('mock.h', 'test.cc'))
        self.assertEqual(res.message, 'done')

        d = res.to_dict()
        self.assertTrue(isinstance(d, dict))
        self.assertTrue(d.get('success'))
        self.assertEqual(d.get('returncode'), 0)

    def test_failed_result(self) -> None:
        '''
            Tests returncode when success is False.
        '''
        res = GenerationResult(
            success=False,
            output_dir='',
            generated_files=(),
            message='error occurred'
        )
        self.assertFalse(res.success)
        self.assertEqual(res.to_dict().get('returncode'), 1)
