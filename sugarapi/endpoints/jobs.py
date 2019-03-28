# coding: utf-8
"""
API for managing/viewing jobs.
"""

from fastapi import APIRouter
from sugarapi import get_master
from sugar.transport.serialisable import ObjectGate


apirouter = APIRouter()


@apirouter.get("/job/all")
def get_all_jobs(limit: int = 25, offset: int = 0) -> dict:
    """
    Get all known jobs.

    :param limit: limit per page
    :param offset: offset of the page

    :returns: jobs structure
    """
    return {
        "jobs": [ObjectGate(job).to_dict()
                 for job in get_master().job_store.get_all_overview(limit=limit, offset=offset)]
    }
