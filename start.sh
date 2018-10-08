#!/bin/sh

if [ "$HISTORIAL" = true ];then
    if [ "$SOLOAGRICULTURA" = true ];then
        PYTHONPATH="." python sniim/cli.py --historial --solo-agricultura
    fi
    if [ "$SOLOGANADO" = true ];then
        PYTHONPATH="." python sniim/cli.py --historial --solo-ganado
    fi

    if [ "$SOLOAGRICULTURA" = false ] && [ "$SOLOGANADO" = false ];then
        PYTHONPATH="." python sniim/cli.py --historial
    fi
fi

if [ "$HISTORIAL" = false ];then
    if [ "$SOLOAGRICULTURA" = true ];then
        PYTHONPATH="." python sniim/cli.py --solo-agricultura
    fi

    if [ "$SOLOGANADO" = true ];then
        PYTHONPATH="." python sniim/cli.py --solo-ganado
    fi

    if [ "$SOLOAGRICULTURA" = false ] && [ "$SOLOGANADO" = false ];then 
        PYTHONPATH="." python sniim/cli.py
    fi
fi
