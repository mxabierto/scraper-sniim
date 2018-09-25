#!/bin/sh

if [ "$HISTORIAL" = true ];then
    PYTHONPATH="." python precios/cli.py --historial
fi

if [ "$HISTORIAL" = false ];then
    PYTHONPATH="." python precios/cli.py --no-historial
fi