# -*- coding: UTF-8 -*-

'''
Module
    template_provider_test.py
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
    Unit tests for TemplateProvider class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import patch

from gen_um_test.infrastructure.generator.template_provider import TemplateProvider


class TestTemplateProvider(TestCase):
    '''
        Unit tests for TemplateProvider class.
    '''

    def test_provider_initialization_and_str(self) -> None:
        '''
            Tests provider initialization and string representation.
        '''
        tp = TemplateProvider()
        self.assertTrue(tp.is_initialized())
        self.assertIn('TemplateProvider', str(tp))

    def test_get_templates_from_archive(self) -> None:
        '''
            Tests retrieving all standard templates from templates.tgz archive.
        '''
        tp = TemplateProvider()
        for key in ['mock', 'fake', 'test', 'cmake', 'main']:
            content = tp.get_template(key)
            self.assertTrue(bool(content), f'Template {key} was empty')
            # Test caching: second call returns same cached string
            cached = tp.get_template(key)
            self.assertEqual(content, cached)

    def test_nonexistent_config_dir(self) -> None:
        '''
            Tests fallback when config dir does not exist.
        '''
        tp = TemplateProvider(config_dir='/non/existent/dir')
        self.assertEqual(tp._scheme_data, {})
        # Should fallback to filesystem templates directory
        content = tp.get_template('mock')
        self.assertTrue(bool(content))

    def test_unknown_template_key(self) -> None:
        '''
            Tests retrieving an unknown template key returns empty string.
        '''
        tp = TemplateProvider()
        self.assertEqual(tp.get_template('unknown_template_key_xyz'), '')

    def test_load_scheme_exception(self) -> None:
        '''
            Tests exception handling during scheme loading.
        '''
        with patch('gen_um_test.infrastructure.generator.template_provider.Loader') as mock_loader:
            mock_loader.side_effect = RuntimeError('boom')
            tp = TemplateProvider()
            self.assertEqual(tp._scheme_data, {})

    def test_extract_from_archive_none_extracted(self) -> None:
        '''
            Tests extraction when tar member extractfile returns None.
        '''
        tp = TemplateProvider()
        with patch('tarfile.TarFile.extractfile', return_value=None):
            content = tp._extract_from_archive('mock')
            self.assertEqual(content, '')

    def test_read_from_filesystem_read_error(self) -> None:
        '''
            Tests reading from filesystem when open raises OSError.
        '''
        tp = TemplateProvider()
        with patch('builtins.open', side_effect=OSError('read failure')):
            content = tp._read_from_filesystem('mock')
            self.assertEqual(content, '')
