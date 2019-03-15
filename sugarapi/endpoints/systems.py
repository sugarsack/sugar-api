# coding: utf-8
"""
API for the systems.
"""
from sugarapi import apirouter


@apirouter.get("/systems")
def get_systems():
    return {"systems": ["one", "two", "three"]}
