from enum import Enum


class ArgumentStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    REINSTATED = "reinstated"


class ArgumentStrength(Enum):
    WEAK = 0.25
    MODERATE = 0.5
    STRONG = 0.75
    DEFINITIVE = 1.0