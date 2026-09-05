#pragma once

#include "ISerialPort.h"
#include <cstddef>

namespace hardware::comm {

class FakeSerialPort : public ISerialPort {
public:
  ~FakeSerialPort() override = default;

  mutable size_t open_calls{0};
  mutable size_t close_calls{0};
  mutable size_t is_open_calls{0};
  mutable size_t write_calls{0};
  mutable size_t read_calls{0};
  mutable size_t get_baud_rate_calls{0};

  bool open(const std::string &port_name, uint32_t baud_rate) override {
    ++open_calls;
    return true;
  }

  void close() override { ++close_calls; }

  bool is_open() const override {
    ++is_open_calls;
    return true;
  }

  size_t write(const std::vector<uint8_t> &data) override {
    ++write_calls;
    return 0;
  }

  std::vector<uint8_t> read(size_t max_bytes) override {
    ++read_calls;
    return {};
  }

  uint32_t get_baud_rate() const override {
    ++get_baud_rate_calls;
    return 0;
  }
};

} // namespace hardware::comm
