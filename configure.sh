#!/bin/bash
if [ ! -d venv/ ]; then
  python3 -m venv venv
fi

if [ $# -gt 0 ] && [ $1 = "--update" ]; then
  echo "Updating..."
  rm -rf src/MPX/pysidex/
fi

if [ -d src/MPX/pysidex/ ]; then
  echo "It has already been configured!"
else
  mkdir -p src/MPX/pysidex/
  git clone https://github.com/reticulardev/pysidex.git src/MPX/pysidex/
  rm -rf src/MPX/pysidex/.git/
  . venv/bin/activate && python -m pip install --upgrade pip && python -m pip install -r src/MPX/pysidex/requirements.txt
  echo "..."
  echo "Done! To test run: python src/MPX/pysidex/src/demo.py"
fi
