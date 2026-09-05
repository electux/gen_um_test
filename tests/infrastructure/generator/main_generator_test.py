# -*- coding: UTF-8 -*-

'''
Module
    main_generator_test.py
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
    Unit tests for MainGenerator class.
'''

from __future__ import annotations

from os import unlink
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase

from gen_um_test.infrastructure.generator.main_generator import MainGenerator


class TestMainGenerator(TestCase):
    '''
        Unit tests for MainGenerator class.
    '''

    def test_main_generation(self) -> None:
        '''
            Tests test_main.cc generation.
        '''
        gen = MainGenerator()
        self.assertTrue(gen.is_initialized())
        self.assertIn('MainGenerator', str(gen))

        code = gen.generate()
        self.assertIn('#include <gtest/gtest.h>', code)
        self.assertIn('::testing::InitGoogleTest(&argc, argv);', code)
        self.assertIn('return RUN_ALL_TESTS();', code)

    def test_main_generation_with_custom_template(self) -> None:
        '''
            Tests test_main.cc generation with custom template path.
        '''
        with NamedTemporaryFile(mode='w', suffix='.template', delete=False) as tmp:
            tmp.write('// custom main')
            tmp_path = tmp.name

        try:
            gen = MainGenerator(template_path=tmp_path)
            code = gen.generate()
            self.assertEqual(code, '// custom main')
        finally:
            if exists(tmp_path):
                unlink(tmp_path)
