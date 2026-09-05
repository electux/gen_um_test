# -*- coding: UTF-8 -*-

'''
Module
    registry.py
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
    Encapsulates core components for simplification of gen_test bundle.
'''

from __future__ import annotations

from gen_test.setup.bundle import GenTestBundle
from gen_test.setup.dependencies import GenTestBundleDependencies
from gen_test.setup.dep_validator import GenTestBundleDependenciesValidator
from gen_test.setup.keys import GenTestBundleKeys
from gen_test.setup.validator import GenTestBundleValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_test/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GenTestBundleRegistry:
    '''
        Encapsulates core components for simplification of gen_test bundle.

        It defines:

            :methods:
                | create_bundle - Creates a gen_test bundle.
                | get_version - Returns the registry version.
    '''

    @classmethod
    def create_bundle(cls, dependencies: GenTestBundleDependencies) -> GenTestBundle:
        '''
            Creates a gen_test bundle.

            :param dependencies: The gen_test bundle dependencies.
            :return: GenTest bundle.
            :exceptions:
                | ATSValueError: The gen_test bundle dependencies must be provided and have proper values.
                | ATSTypeError:  The gen_test bundle dependencies must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
                | ATSValueError: The gen_test bundle must be provided and have proper values.
                | ATSTypeError:  The gen_test bundle must be an instance of GenTestBundle and
                |                its attributes must be instances of their respective types.
        '''
        GenTestBundleDependenciesValidator.validate(dependencies)

        bundle: GenTestBundle = GenTestBundle(
            base=dependencies.get(GenTestBundleKeys.DEPENDENCY_BASE) if dependencies else None,
            service=dependencies.get(GenTestBundleKeys.DEPENDENCY_SERVICE) if dependencies else None,
            subprocessor=dependencies.get(GenTestBundleKeys.DEPENDENCY_SUBPROCESSOR) if dependencies else None,
            cli=dependencies.get(GenTestBundleKeys.DEPENDENCY_CLI) if dependencies else None
        )

        GenTestBundleValidator.validate(bundle)

        return bundle

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the registry version.

            :return: The registry version.
            :exceptions: None.
        '''
        return __version__
