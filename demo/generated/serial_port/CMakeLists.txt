cmake_minimum_required(VERSION 3.16)
project(serial_port_test LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(GTest REQUIRED)

add_executable(serial_port_test
    serial_port_test.cc
    test_main.cc
    mock_serial_port.h
)

target_include_directories(serial_port_test PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/../..
)

target_link_libraries(serial_port_test PRIVATE
    GTest::gtest
    GTest::gmock
)

include(GoogleTest)
gtest_discover_tests(serial_port_test)
