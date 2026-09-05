#!/bin/bash
#
# @brief   gen_test
# @version 1.0.0
# @date    Sat Sep 05 08:02:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 gates/gates/interfaces_checker.py gen_test
python3 gates/gates/isp_checker.py gen_test
python3 gates/gates/limits_checker.py gen_test
python3 gates/gates/srp_checker.py gen_test

echo "Done"
