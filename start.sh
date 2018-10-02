#!/bin/sh

if [ "$HISTORIAL" = true ];then
    PYTHONPATH="." python sniim/cli.py --historial
fi

if [ "$HISTORIAL" = false ];then
    PYTHONPATH="." python sniim/cli.py --no-historial
fi
