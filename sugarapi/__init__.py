# coding: utf-8

from fastapi import FastAPI
from sugar.utils.objects import Singleton
from sugar.config import get_config
from sugar.components.server.pdatastore import PDataStore
from sugar.lib.jobstore import JobStorage


apirouter = FastAPI(title="Sugar API", version="0.0.0 Alpha")


class Traverser:
    """
    Object traverser for IPC.

    Since API is running its own server in a separate process
    and thus different memory segment, there should be IPC
    enabled. Traverser just allows to have an elegant way of
    calling exposed stuff on the parent process.

    Here how it works:

    1. Parent process is running a pipe between two processes.

    2. Child process is calling something and Traverser turning
       that into a path. E.g. foo.bar.blah gets ["foo", "bar", "blah"]
       It also allows to distinguish callable and property.

    3. Once something was called, it is compiled into a result
       object, called CallTarget. This call target instance with
       all the required information what is going to be called
       on the parent process is sent over Pipe, serialised.

    4. Parent receives that object, and calls it over the exposed
       target. The CallTarget does the job to traverse attributes
       and call the final endpoint and gather the result.

    5. The result of call_object() is returned back over the Pipe
       to the static API requester.
    """

    PROPERTY = "__property"

    class CallTarget:
        """
        Summary object.
        """
        def __init__(self):
            self.attrs = []
            self.args = []
            self.kwargs = {}
            self.is_callable = True

        def __call__(self, *args, **kwargs):
            return self.__call_target_method(*args, **kwargs)

        def __call_target_method(self, target):
            """
            Call the object attributes and methods.

            :param obj: target object over IPC
            :return:
            """
            for node_name in self.attrs:
                target = getattr(target, node_name)
            if target is not None:
                if self.is_callable:
                    target = target(*self.args, **self.kwargs)
            return target

    def __init__(self, ref, id, parent=None):
        self.__ref = ref
        self.__parent = parent
        self.__id = id

    def __path(self, node, path=None):
        if path is None:
            path = []
        if node.__id is not None:
            path.insert(0, node.__id)
        if node.__parent is not None:
            self.__path(node.__parent, path)
        return path

    def __call__(self, *args, **kwargs):
        ctgt = Traverser.CallTarget()
        ctgt.attrs = self.__path(self)
        ctgt.args = list(args)
        ctgt.kwargs = kwargs
        ctgt.is_callable = Traverser.PROPERTY not in args

        if not ctgt.is_callable:
            ctgt.args.pop(ctgt.args.index(Traverser.PROPERTY))
        ctgt.args = tuple(ctgt.args)

        return self.__ref.get(ctgt)

    def __getattr__(self, item):
        if item not in self.__dict__:
            self.__dict__[item] = Traverser(ref=self.__ref, id=item, parent=self)
        return self.__dict__[item]


@Singleton
class MasterRef:
    """
    Master reference object.
    """
    def __init__(self, channel=None):
        self.receiver, self.sender = channel if channel else (None, None)
        self.pdata_store = PDataStore(get_config().cache.path)
        self.job_store = JobStorage(get_config())

    @property
    def ref(self):
        """
        Reference to the target object.
        :return:
        """
        return Traverser(ref=self, id=None)

    def get(self, call_target):
        """
        Get an attribute.

        :param call_target: compiled call target Object
        :return:
        """
        self.sender.send(call_target)
        return self.sender.recv()


def get_master():
    """
    Get master IPC.

    :return:
    """
    return MasterRef()
