# -*- coding: UTF-8 -*-

'''
Module
    registry.py
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
    Encapsulates core components for simplification of gen_um_test bundle.
'''

from __future__ import annotations

from gen_um_test.setup.bundle import GenUmTestBundle
from gen_um_test.setup.dependencies import GenUmTestBundleDependencies
from gen_um_test.setup.dep_validator import GenUmTestBundleDependenciesValidator
from gen_um_test.setup.keys import GenUmTestBundleKeys
from gen_um_test.setup.validator import GenUmTestBundleValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/gen_um_test'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_um_test/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GenUmTestBundleRegistry:
    '''
        Encapsulates core components for simplification of gen_um_test bundle.

        It defines:

            :methods:
                | create_bundle - Creates a gen_um_test bundle.
                | get_version - Returns the registry version.
    '''

    @classmethod
    def create_bundle(cls, dependencies: GenUmTestBundleDependencies) -> GenUmTestBundle:
        '''
            Creates a gen_um_test bundle.

            :param dependencies: The gen_um_test bundle dependencies.
            :return: GenUmTest bundle.
            :exceptions:
                | ATSValueError: The gen_um_test bundle dependencies must be provided and have proper values.
                | ATSTypeError:  The gen_um_test bundle dependencies must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
                | ATSValueError: The gen_um_test bundle must be provided and have proper values.
                | ATSTypeError:  The gen_um_test bundle must be an instance of GenUmTestBundle and
                |                its attributes must be instances of their respective types.
        '''
        GenUmTestBundleDependenciesValidator.validate(dependencies)

        bundle: GenUmTestBundle = GenUmTestBundle(
            base=dependencies.get(GenUmTestBundleKeys.DEPENDENCY_BASE) if dependencies else None,
            service=dependencies.get(GenUmTestBundleKeys.DEPENDENCY_SERVICE) if dependencies else None,
            subprocessor=dependencies.get(GenUmTestBundleKeys.DEPENDENCY_SUBPROCESSOR) if dependencies else None,
            cli=dependencies.get(GenUmTestBundleKeys.DEPENDENCY_CLI) if dependencies else None
        )

        GenUmTestBundleValidator.validate(bundle)

        return bundle

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the registry version.

            :return: The registry version.
            :exceptions: None.
        '''
        return __version__
