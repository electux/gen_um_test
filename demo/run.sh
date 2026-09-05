#!/usr/bin/env bash
# -*- coding: UTF-8 -*-

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

export PYTHONPATH="${ROOT_DIR}:${PYTHONPATH}"

echo "================================================="
echo "  gen_test - Google C++ Test Suite Generation Demo"
echo "================================================="

# 1. Generate full test suite
echo ""
echo "[1/2] Generating complete test suite for ISerialPort.h..."
python3 "${ROOT_DIR}/main.py" suite \
    --interface "${SCRIPT_DIR}/ISerialPort.h" \
    --output "${SCRIPT_DIR}/generated/serial_port"

echo ""
echo "Generated files:"
ls -la "${SCRIPT_DIR}/generated/serial_port"

# 2. Check individual mock generation
echo ""
echo "[2/2] Generating standalone Mock for ISerialPort.h..."
python3 "${ROOT_DIR}/main.py" mock \
    --interface "${SCRIPT_DIR}/ISerialPort.h" \
    --output "${SCRIPT_DIR}/generated/standalone_mock"

echo "Standalone mock generated:"
ls -la "${SCRIPT_DIR}/generated/standalone_mock"

echo ""
echo "✅ Demo completed successfully!"
