#!/bin/bash
#
# @brief   gen_um_test
# @version 1.0.2
# @date    Sat Sep 05 08:02:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 coverage/ats_coverage.py gen_um_test
pylint gen_um_test > gen_um_test.report
echo "Done"
