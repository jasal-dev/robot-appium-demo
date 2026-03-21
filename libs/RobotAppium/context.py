from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError


class ApplicationCache:
    def __init__(self):
        self._applications = {}
        self._current = None

    @property
    def current(self):
        return self._current

    def register(self, application, alias=None):
        key = alias or f"application-{len(self._applications) + 1}"
        self._applications[key] = application
        self._current = application
        return application

    def close_all(self):
        for application in list(self._applications.values()):
            try:
                application.quit()
            except Exception:
                pass
        self._applications.clear()
        self._current = None


class Context:
    def __init__(self):
        self._cache = ApplicationCache()

    def current_application(self):
        if not self._cache.current:
            raise RuntimeError('No application is open')
        return self._cache.current