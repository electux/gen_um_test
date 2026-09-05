# -*- coding: UTF-8 -*-

'''
Module
    cpp_parser_test.py
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
    Unit tests for CppParser class.
'''

from __future__ import annotations

from os import unlink
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase

from ats_utilities.exceptions import ATSValueError

from gen_test.infrastructure.parser.cpp_parser import CppParser


class TestCppParser(TestCase):
    '''
        Unit tests for CppParser class.
    '''

    def test_parser_initialization_and_str(self) -> None:
        '''
            Tests parser initialization and string representation.
        '''
        parser = CppParser()
        self.assertTrue(parser.is_initialized())
        self.assertIn('CppParser', str(parser))

    def test_parse_source_basic_interface(self) -> None:
        '''
            Tests parsing basic interface with namespaces, methods, and types.
        '''
        parser = CppParser()
        source = '''
        #pragma once
        #include <string>
        #include <vector>

        namespace acme::devices {

        class ISensor : public IBaseSensor {
        public:
            virtual ~ISensor() = default;

            virtual bool initialize(const std::string& config_file, int timeout) = 0;
            virtual double read_value() const = 0;
            virtual void reset() noexcept = 0;
        };

        }  // namespace acme::devices
        '''

        interfaces = parser.parse_source(source, file_path='include/ISensor.h')
        self.assertEqual(len(interfaces), 1)

        sensor = interfaces[0]
        self.assertEqual(sensor.name, 'ISensor')
        self.assertEqual(sensor.namespace, 'acme::devices')
        self.assertIn('<string>', sensor.includes)
        self.assertIn('<vector>', sensor.includes)
        self.assertEqual(sensor.base_classes, ('IBaseSensor',))
        self.assertEqual(sensor.header_path, 'include/ISensor.h')

        self.assertEqual(len(sensor.methods), 3)

        m1 = sensor.methods[0]
        self.assertEqual(m1.name, 'initialize')
        self.assertEqual(m1.return_type, 'bool')
        self.assertEqual(len(m1.parameters), 2)
        self.assertEqual(m1.parameters[0], ('const std::string&', 'config_file'))
        self.assertEqual(m1.parameters[1], ('int', 'timeout'))
        self.assertFalse(m1.is_const)
        self.assertFalse(m1.is_noexcept)

        m2 = sensor.methods[1]
        self.assertEqual(m2.name, 'read_value')
        self.assertEqual(m2.return_type, 'double')
        self.assertTrue(m2.is_const)

        m3 = sensor.methods[2]
        self.assertEqual(m3.name, 'reset')
        self.assertEqual(m3.return_type, 'void')
        self.assertTrue(m3.is_noexcept)

    def test_parse_source_empty_or_non_pure_virtual(self) -> None:
        '''
            Tests parsing source with non-pure-virtual classes.
        '''
        parser = CppParser()
        source = '''
        class ConcreteClass {
        public:
            void regular_method() {}
        };
        '''
        interfaces = parser.parse_source(source)
        self.assertEqual(len(interfaces), 0)

    def test_parse_file_validation_error(self) -> None:
        '''
            Tests parse_file raises ATSValueError when file doesn't exist.
        '''
        parser = CppParser()
        with self.assertRaises(ATSValueError):
            parser.parse_file('/non/existent/interface.h')

    def test_parse_file_real(self) -> None:
        '''
            Tests parse_file on a real interface header file.
        '''
        parser = CppParser()
        content = '''#pragma once
#include <string>
#include <vector>

namespace hardware::comm {

class ISerialPort {
public:
    virtual ~ISerialPort() = default;
    virtual bool open(const std::string& port_name, uint32_t baud_rate) = 0;
    virtual void close() = 0;
    virtual bool is_open() const = 0;
    virtual size_t write(const std::vector<uint8_t>& data) = 0;
    virtual std::vector<uint8_t> read(size_t max_bytes) = 0;
    virtual uint32_t get_baud_rate() const = 0;
};

}  // namespace hardware::comm
'''
        with NamedTemporaryFile(mode='w', suffix='.h', delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            interfaces = parser.parse_file(tmp_path)
            self.assertEqual(len(interfaces), 1)
            self.assertEqual(interfaces[0].name, 'ISerialPort')
            self.assertEqual(len(interfaces[0].methods), 6)
        finally:
            if exists(tmp_path):
                unlink(tmp_path)

    def test_parse_source_empty(self) -> None:
        '''
            Tests parse_source with empty content returns empty tuple.
        '''
        parser = CppParser()
        self.assertEqual(parser.parse_source(''), ())

    def test_parse_parameters_variations(self) -> None:
        '''
            Tests parsing parameter edge cases: default values, unnamed params, pointer/ref attached to name.
        '''
        parser = CppParser()
        source = '''
        class IParamTest {
        public:
            virtual void complex_func(int timeout = 100, , uint8_t *buffer = nullptr, int &count, double) = 0;
        };
        '''
        interfaces = parser.parse_source(source)
        self.assertEqual(len(interfaces), 1)
        m = interfaces[0].methods[0]
        self.assertEqual(m.name, 'complex_func')
        self.assertEqual(m.parameters[0], ('int', 'timeout'))
        self.assertEqual(m.parameters[1], ('uint8_t*', 'buffer'))
        self.assertEqual(m.parameters[2], ('int&', 'count'))
        self.assertEqual(m.parameters[3], ('double', ''))
