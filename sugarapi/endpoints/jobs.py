# coding: utf-8
"""
API for managing/viewing jobs.
"""
import pytz
import datetime
from fastapi import APIRouter
from sugarapi import get_master
from sugar.transport.serialisable import ObjectGate
import sugar.utils.timeutils


apirouter = APIRouter()


@apirouter.get("/job/all")
def get_all_jobs(limit: int = 25, offset: int = 0) -> dict:
    """
    Get all known jobs.

    Parameters:
        limit: limit per page
        offset: offset of the page
    """
    return {
        "jobs": [ObjectGate(job).to_dict()
                 for job in get_master().job_store.get_all_overview(limit=limit, offset=offset)]
    }


@apirouter.get("/job/expire")
def expire(dt=None):
    """
    Expire jobs by date/time.

    Parameters:
        dt: datetime
    """
    get_master().job_store.expire(
        dtm=sugar.utils.timeutils.from_iso(dtm=dt) if dt is not None else datetime.datetime.now(tz=pytz.UTC))


@apirouter.get("/job/details")
def get_job_details(jid):
    """
    Get job details.

    Parameters:
        jid: Job ID
    """
    job = get_master().job_store.get_by_jid(jid=jid)
    return ObjectGate(job).to_dict() if job is not None else {}
