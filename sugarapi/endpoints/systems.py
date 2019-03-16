# coding: utf-8
"""
API for the systems.
"""
from fastapi import APIRouter
from sugarapi import MasterRef


apirouter = APIRouter()


@apirouter.get("/systems")
def get_systems():
    return {"systems": ["one", "two", "three"]}


@apirouter.get("/systems/master")
def get_ref():
    return {"peers": MasterRef().ref.core.peer_registry.get_targets(":a")}
