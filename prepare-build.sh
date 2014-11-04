#!/bin/bash
TAG=${TRAVIS_TAG:-"unknown"}
if [[ "${TAG}" = "unknown" ]]; then
    TAG=`git describe`
    if [[ "$?" != "0" ]]; then
        TAG=`git describe --always`
    fi
fi
echo ${TAG} | cut -c 1- > VERSION
