class Reference:

    def __init__(self, reference):
        self._ref = reference

    @property
    def value(self) -> str:
        return self._ref

    def is_relative_reference(self):
        return self.is_remote_ref() and not self.is_url_reference()

    def is_url_reference(self):
        return self.is_remote_ref() and (self._ref.startswith('//', 0) or self._ref.startswith('http', 0))

    def is_remote_ref(self):
        return not self.is_local_ref()
 
    def is_local_ref(self):
        return self._ref.startswith('#', 0)


