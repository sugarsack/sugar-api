# coding: utf-8
"""
API for the systems.
"""
from fastapi import APIRouter
from sugarapi import get_master


apirouter = APIRouter()


@apirouter.get("/clients/online")
def query_systems(query=None):
    """
    Query systems. If query is omitting, all online systems are returned.
    """
    return {
        "systems": get_master().ref.core.peer_registry.get_targets(query or "*")
    }


@apirouter.get("/clients/all")
def get_all_systems():
    """
    Return all systems with p-data, including offline.
    """
    return {
        "systems": list(get_master().pdata_store.clients())
    }


@apirouter.get("/clients/status")
def get_all_status():
    """
    Return all systems status. P-Data is not included.
    """
    return {
        "systems": get_master().ref.core.peer_registry.get_status()
    }
