# -*- coding: UTF-8 -*-

'''
Module
    template_provider.py
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
    Template provider using scheme.json and templates.tgz archive via ats_utilities loader.
'''

from __future__ import annotations

from os.path import dirname, exists, join, realpath
from tarfile import open as tar_open
from typing import ClassVar

from ats_utilities.config_io.loader.engine import Loader
from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.options import ConfigIOBundleOptions
from ats_utilities.context.factory import ContextBundleFactory
from ats_utilities.utils.reflection import to_str

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_um_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_um_test/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TemplateProvider:
    '''
        Provides template contents from templates.tgz referenced by scheme.json.

        It defines:

            :attributes:
                | _scheme_file - Path to scheme.json configuration file.
                | _archive_file - Path to templates.tgz archive file.
                | _cache - In-memory cache of loaded templates.
            :methods:
                | __init__ - Initializes the template provider.
                | get_template - Retrieves template text by key.
                | is_initialized - Checks if template provider is initialized.
                | __str__ - String representation of provider.
    '''

    _DEFAULT_CONFIG_DIR: ClassVar[str] = join(dirname(dirname(realpath(__file__))), 'config')

    def __init__(self, config_dir: str | None = None) -> None:
        '''
            Initializes template provider.

            :param config_dir: Optional custom configuration directory path.
        '''
        base_dir = config_dir or self._DEFAULT_CONFIG_DIR
        self._scheme_file: str = join(base_dir, 'scheme.json')
        self._archive_file: str = join(base_dir, 'templates.tgz')
        self._templates_dir: str = join(dirname(dirname(realpath(__file__))), 'templates')
        self._cache: dict[str, str] = {}
        self._scheme_data: dict[str, object] = self._load_scheme()

    def _load_scheme(self) -> dict[str, object]:
        '''
            Loads scheme.json using ats_utilities Loader.

            :return: Loaded configuration dictionary or empty dictionary.
        '''
        if not exists(self._scheme_file):
            return {}

        try:
            ctx = ContextBundleFactory.create_bundle()
            opts = ConfigIOBundleOptions(file_path=self._scheme_file, context_bundle=ctx)
            bundle = ConfigIOBundleFactory.create_bundle(opts)
            loader = Loader(bundle)
            return loader.load_configuration()

        except Exception:
            return {}

    def get_template(self, template_key: str) -> str:
        '''
            Retrieves template content by key.

            :param template_key: Key of template ('mock', 'fake', 'test', 'cmake', 'main').
            :return: Template string content.
        '''
        if template_key in self._cache:
            return self._cache[template_key]

        content = self._extract_from_archive(template_key)
        if not content:
            content = self._read_from_filesystem(template_key)

        if content:
            self._cache[template_key] = content

        return content

    def _extract_from_archive(self, template_key: str) -> str:
        '''
            Extracts template file content directly from templates.tgz.

            :param template_key: Key of template.
            :return: Template text or empty string.
        '''
        if not exists(self._archive_file):
            return ''

        templates_cfg = self._scheme_data.get('templates', {}) if isinstance(self._scheme_data, dict) else {}
        files_map = templates_cfg.get('files', {}) if isinstance(templates_cfg, dict) else {}
        file_name = files_map.get(template_key, f'{template_key}.template') if isinstance(files_map, dict) else f'{template_key}.template'

        try:
            with tar_open(self._archive_file, 'r:gz') as archive:
                entry = f'templates/{file_name}'
                member = archive.getmember(entry)
                extracted = archive.extractfile(member)
                if extracted is not None:
                    return extracted.read().decode('utf-8')

        except Exception:
            return ''

        return ''

    def _read_from_filesystem(self, template_key: str) -> str:
        '''
            Fallback reader from filesystem templates directory.

            :param template_key: Key of template.
            :return: Template text or empty string.
        '''
        fallback_file = join(self._templates_dir, f'{template_key}.template')
        if exists(fallback_file):
            try:
                with open(fallback_file, 'r', encoding='utf-8') as handle:
                    return handle.read()
            except Exception:
                return ''
        return ''

    def is_initialized(self) -> bool:
        '''
            Checks if provider is initialized.

            :return: True if ready to serve templates, False otherwise.
        '''
        return True

    def __str__(self) -> str:
        '''
            Returns string representation of TemplateProvider.

            :return: String representation.
        '''
        return to_str(self)
