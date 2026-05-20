#!/usr/bin/env bash
set -euo pipefail

python run_all.py --frameworks langchain crewai autogen llamaindex --repeats 1 --mode mock --output-dir logs --log-level INFO --timeout 60
