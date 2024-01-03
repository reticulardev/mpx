#!/bin/bash
if [ $# -gt 0 ] && [ $1 = "--update" ]; then
  echo "Updating..."
  rm -rf src/pysidex/
fi

if [ -d src/pysidex/ ]; then
  echo "It has already been configured!"
else
  mkdir -p src/pysidex/
  git clone https://github.com/reticulardev/pysidex.git src/pysidex/
  . ../venv/bin/activate && python -m pip install --upgrade pip && python -m pip install -r src/pysidex/requirements.txt
  echo
  echo "Done! To test use:"
  echo "python src/pysidex/src/demo.py"
fi
