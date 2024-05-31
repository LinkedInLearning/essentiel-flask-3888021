#!/bin/bash

if [ ! -d ".venv" ]; then
  python -m venv .venv
fi
if [ ! -d "instance" ]; then
  mkdir instance
  if [ -f "doc/config.py.exemple" ]; then
    cp doc/config.py.exemple instance/config.py
  fi
fi
source .venv/bin/activate
pip install -r requirements.txt
if [ -d "alembic" ]; then
  alembic upgrade head
fi
