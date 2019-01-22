from typing import Any

from rx.core import Disposable, typing
from rx.disposables import SingleAssignmentDisposable, CompositeDisposable
from rx.concurrency.schedulerbase import SchedulerBase


class TkinterScheduler(SchedulerBase):
    """A scheduler that schedules work via the Tkinter main event loop.

    http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/universal.html
    http://effbot.org/tkinterbook/widget.htm"""

    def __init__(self, master):
        self.master = master

    def schedule(self, action: typing.ScheduledAction, state: Any = None) -> typing.Disposable:
        """Schedules an action to be executed."""

        return self.schedule_relative(0.0, action, state)

    def schedule_relative(self, duetime: typing.RelativeTime, action: typing.ScheduledAction,
                          state: Any = None) -> typing.Disposable:
        """Schedules an action to be executed after duetime.

        Args:
            duetime: Relative time after which to execute the action.
            action: Action to be executed.

        Returns:
            The disposable object used to cancel the scheduled action
            (best effort).
        """

        msecs = int(self.to_seconds(duetime)*1000.0)
        disposable = SingleAssignmentDisposable()

        def invoke_action():
            disposable.disposable = self.invoke_action(action, state)

        alarm = self.master.after(msecs, invoke_action)

        def dispose():
            self.master.after_cancel(alarm)

        return CompositeDisposable(disposable, Disposable.create(dispose))

    def schedule_absolute(self, duetime: typing.AbsoluteTime, action: typing.ScheduledAction,
                          state: Any = None) -> typing.Disposable:
        """Schedules an action to be executed at duetime.

        Args:
            duetime: Absolute time after which to execute the action.
            action: Action to be executed.

        Returns:
            The disposable object used to cancel the scheduled action
            (best effort).
        """

        duetime = self.to_datetime(duetime)
        return self.schedule_relative(duetime - self.now, action, state)
