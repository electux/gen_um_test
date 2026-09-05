#pragma once

#include <cstddef>
#include <cstdint>
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
