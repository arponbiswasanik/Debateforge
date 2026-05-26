class DebateForgeError(Exception):
    pass


class AgentError(DebateForgeError):
    pass


class ArgumentError(DebateForgeError):
    pass


class DebateEngineError(DebateForgeError):
    pass


class RetrievalError(DebateForgeError):
    pass