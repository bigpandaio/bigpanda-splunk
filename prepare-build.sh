#!/bin/bash
TAG=${TRAVIS_TAG:-"unknown"}
if [[ "${TAG}" = "unknown" ]]; then
    TAG=`git describe`
    if [[ "$?" != "0" ]]; then
        TAG="v0.0.0"
    fi
fi
echo ${TAG} | cut -c 1- > VERSION
