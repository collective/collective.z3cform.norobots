#!/bin/bash
# ./test-coverage.sh

bin/coverage
bin/report
open htmlcov/index.html