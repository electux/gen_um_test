#pragma once

#include "ISerialPort.h"
#include <gmock/gmock.h>

namespace hardware::comm {

class MockSerialPort : public ISerialPort {
public:
  ~MockSerialPort() override = default;

  MOCK_METHOD(bool, open, (const std::string &port_name, uint32_t baud_rate),
              (override));
  MOCK_METHOD(void, close, (), (override));
  MOCK_METHOD(bool, is_open, (), (const, override));
  MOCK_METHOD(size_t, write, (const std::vector<uint8_t> &data), (override));
  MOCK_METHOD(std::vector<uint8_t>, read, (size_t max_bytes), (override));
  MOCK_METHOD(uint32_t, get_baud_rate, (), (const, override));
};

using NiceMockSerialPort = ::testing::NiceMock<MockSerialPort>;
using StrictMockSerialPort = ::testing::StrictMock<MockSerialPort>;

} // namespace hardware::comm
