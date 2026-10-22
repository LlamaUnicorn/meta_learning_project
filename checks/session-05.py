import sys; sys.dont_write_bytecode = True

import asyncio
import traceback
from types import SimpleNamespace
from uuid import UUID, uuid4

from src.application.dto.person import PersonUpdateDTO, UpdateEntryDTO
from src.application.person_requests.update import update_person
from src.domain.aggregates import Person
from src.domain.value_objects import PK, JournalInputOperationType, ProfileStatus, ValueType
from src.infrastructure.other.crypto_cipher import CipherAES

CIPHER = CipherAES("s" * 32, "h" * 32)
SYSTEM = UUID("00000000-0000-0000-0000-00000000000a")
BIRTH = "11111111-1111-1111-1111-111111111111"
CHILDREN = "22222222-2222-2222-2222-222222222222"
TYPES = {
    BIRTH: SimpleNamespace(name="birth_date", value_type=ValueType.DATE, is_multivalue=False,
                           is_sensitive=True, validation_schema=None),
    CHILDREN: SimpleNamespace(name="children", value_type=ValueType.INTEGER, is_multivalue=False,
                              is_sensitive=False, validation_schema=None),
}
ALLOW = {PK(UUID(k)): SimpleNamespace(is_allowed=True) for k in TYPES}


class Repo:
    def __init__(self, name, log):
        self.name, self.log = name, log

    async def get(self, key):
        return TYPES[key]

    async def create(self, obj):
        self.log.append(f"{self.name}.create")
        return uuid4()

    async def update(self, obj):
        self.log.append(f"{self.name}.update")


def new_person():
    return Person(id=PK(uuid4()), status=ProfileStatus.ACTIVE, merged_into_person_id=None,
                  identifiers=[], attributes=[])


def run(label, person, field_id, value):
    log = []
    r = lambda n: Repo(n, log)
    dto = PersonUpdateDTO(system_id=SYSTEM, identifiers_check={}, identifiers_update=[],
                          attributes_update=[UpdateEntryDTO(JournalInputOperationType.CREATE, field_id, value)])
    try:
        asyncio.run(update_person(r("types"), r("attributes"), r("types"), r("identifiers"),
                                  r("journal"), r("notifications"), person, dto, ALLOW, {}, CIPHER))
    except Exception as exc:
        frame = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename.endswith("update.py")][-1]
        print(f"{label}: {type(exc).__name__}, update.py:{frame.lineno}")
    else:
        print(f"{label}: ok")
    print("  вызовы:", ", ".join(log) or "—")
    for a in person.attributes:
        print(f"  {a.attribute_type.name}: {CIPHER.decrypt(a.value)!r}, {a.status.name}, "
              f"valid_to={'задан' if a.valid_to else None}")
