#include "mock_serial_port.h"
#include <gtest/gtest.h>

namespace hardware::comm::testing {

class SerialPortTest : public ::testing::Test {
protected:
  MockSerialPort mock;
};

TEST_F(SerialPortTest, CallsOpen) {
  EXPECT_CALL(mock, open(::testing::_, ::testing::_))
      .WillOnce(::testing::Return(true));
  EXPECT_TRUE(mock.open("", 0));
}

TEST_F(SerialPortTest, CallsClose) {
  EXPECT_CALL(mock, close()).Times(1);
  mock.close();
}

TEST_F(SerialPortTest, CallsIs_open) {
  EXPECT_CALL(mock, is_open()).WillOnce(::testing::Return(true));
  EXPECT_TRUE(mock.is_open());
}

TEST_F(SerialPortTest, CallsWrite) {
  EXPECT_CALL(mock, write(::testing::_)).WillOnce(::testing::Return(0));
  EXPECT_EQ(mock.write({}), 0);
}

TEST_F(SerialPortTest, CallsRead) {
  EXPECT_CALL(mock, read(::testing::_)).WillOnce(::testing::Return({}));
  EXPECT_EQ(mock.read(0), {});
}

TEST_F(SerialPortTest, CallsGet_baud_rate) {
  EXPECT_CALL(mock, get_baud_rate()).WillOnce(::testing::Return(0));
  EXPECT_EQ(mock.get_baud_rate(), 0);
}

} // namespace hardware::comm::testing
