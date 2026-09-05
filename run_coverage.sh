#!/bin/bash
#
# @brief   gen_test
# @version 1.0.1
# @date    Sat Sep 05 08:02:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 coverage/ats_coverage.py gen_test
pylint gen_test > gen_test.report
echo "Done"
