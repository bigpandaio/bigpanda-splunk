#!/bin/bash
TAG=${TRAVIS_TAG:-"unknown"}
if [[ "${TAG}" = "unknown" ]]; then
    TAG=`git describe --always`
fi
echo ${TAG} | cut -c 1- > VERSION
