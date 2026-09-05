# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit tests for CLIBundle dataclass.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from gen_um_test.infrastructure.cli.setup.bundle import CLIBundle


class TestCLIBundle(TestCase):
    '''
        Unit tests for CLIBundle.
    '''

    def test_bundle_creation_and_to_dict(self) -> None:
        '''
            Tests bundle creation and to_dict conversion.
        '''
        mock_service = Mock()
        mock_parser = Mock()
        commands = []
        bundle = CLIBundle(service=mock_service, parser=mock_parser, commands=commands)
        self.assertEqual(bundle.service, mock_service)
        self.assertEqual(bundle.parser, mock_parser)
        self.assertEqual(bundle.commands, commands)

        d = bundle.to_dict()
        self.assertTrue(isinstance(d, dict))
        self.assertIn('service', d)
        self.assertIn('parser', d)
        self.assertIn('commands', d)
