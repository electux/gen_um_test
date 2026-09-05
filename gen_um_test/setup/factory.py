# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory for creating the gen_um_test bundle.
'''

from __future__ import annotations

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from gen_um_test.core.service.engine import Service
from gen_um_test.infrastructure.cli.engine import CLI
from gen_um_test.infrastructure.cli.setup.factory import CLIBundleFactory
from gen_um_test.infrastructure.cli.setup.options import CLIBundleOptions
from gen_um_test.infrastructure.generator.cmake_generator import CMakeGenerator
from gen_um_test.infrastructure.generator.code_formatter import CodeFormatter
from gen_um_test.infrastructure.generator.fake_generator import FakeGenerator
from gen_um_test.infrastructure.generator.main_generator import MainGenerator
from gen_um_test.infrastructure.generator.mock_generator import MockGenerator
from gen_um_test.infrastructure.generator.template_provider import TemplateProvider
from gen_um_test.infrastructure.generator.test_generator import TestGenerator
from gen_um_test.infrastructure.parser.cpp_parser import CppParser
from gen_um_test.infrastructure.subprocessor import SubProcessor
from gen_um_test.setup.bundle import GenUmTestBundle
from gen_um_test.setup.dependencies import GenUmTestBundleDependencies
from gen_um_test.setup.keys import GenUmTestBundleKeys
from gen_um_test.setup.opt_validator import GenUmTestBundleOptionsValidator
from gen_um_test.setup.options import GenUmTestBundleOptions
from gen_um_test.setup.registry import GenUmTestBundleRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_um_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_um_test/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GenUmTestBundleFactory:
    '''
        Factory for creating the gen_um_test bundle.

        It defines:

            :attributes:
                | _info_file - Path to the gen_um_test info file.
            :methods:
                | create_bundle - Creates the gen_um_test bundle with optional pre-configured options.
                | get_version - Returns the factory version.
    '''

    _info_file: str = 'gen_um_test/infrastructure/config/gen_um_test.cfg'

    @classmethod
    def create_bundle(cls, options: GenUmTestBundleOptions | None = None) -> GenUmTestBundle:
        '''
            Creates the gen_um_test bundle with optional pre-configured options.

            :param options: The pre-configured options for the gen_um_test bundle.
            :return: The gen_um_test bundle.
            :exceptions:
                | ATSValueError: The gen_um_test bundle options must be provided and have proper values.
                | ATSTypeError:  The gen_um_test bundle options must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
                | ATSValueError: The gen_um_test bundle dependencies must be provided and have proper values.
                | ATSTypeError:  The gen_um_test bundle dependencies must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
                | ATSValueError: The gen_um_test bundle must be provided and have proper values.
                | ATSTypeError:  The gen_um_test bundle must be an instance of GenUmTestBundle and
                |                its attributes must be instances of their respective types.
        '''
        if options is not None:
            GenUmTestBundleOptionsValidator.validate(options)

        info_file = options.get(GenUmTestBundleKeys.OPTION_INFO_FILE) if options else cls._info_file

        context_bundle: ContextBundle = ContextBundleFactory.create_bundle()

        base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=info_file,
                use_generator=True,
                context_bundle=context_bundle
            )
        )

        template_provider: TemplateProvider = TemplateProvider()
        parser: CppParser = CppParser()
        mock_gen: MockGenerator = MockGenerator(template_provider=template_provider)
        fake_gen: FakeGenerator = FakeGenerator(template_provider=template_provider)
        test_gen: TestGenerator = TestGenerator(template_provider=template_provider)
        cmake_gen: CMakeGenerator = CMakeGenerator(template_provider=template_provider)
        main_gen: MainGenerator = MainGenerator(template_provider=template_provider)
        formatter: CodeFormatter = CodeFormatter()

        subprocessor: SubProcessor = SubProcessor(
            parser=parser,
            mock_gen=mock_gen,
            test_gen=test_gen,
            fake_gen=fake_gen,
            cmake_gen=cmake_gen,
            main_gen=main_gen,
            formatter=formatter
        )

        service: Service = Service(subprocessor=subprocessor)

        cli_bundle = CLIBundleFactory.create_bundle(
            CLIBundleOptions(
                service=service,
                parser=base_bundle.option_manager
            )
        )

        cli: CLI = CLI(cli_bundle)

        return GenUmTestBundleRegistry.create_bundle(
            dependencies=GenUmTestBundleDependencies(
                base=base_bundle,
                service=service,
                subprocessor=subprocessor,
                cli=cli
            )
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version.

            :return: The factory version.
            :exceptions: None.
        '''
        return __version__
