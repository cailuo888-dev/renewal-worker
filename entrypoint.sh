#!/bin/bash
set -e
echo "Worker starting..."
exec python /worker.py
