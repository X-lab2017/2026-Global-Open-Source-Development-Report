#!/bin/sh
case "$1" in
*Username*) echo "will-ww" ;;
*) echo "$GH_TOKEN" ;;
esac
