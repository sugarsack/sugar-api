# coding: utf-8
"""
API for the systems.
"""
from fastapi import APIRouter
apirouter = APIRouter()


@apirouter.get("/systems")
def get_systems():
    return {"systems": ["one", "two", "three"]}
