import secrets
import string

from .models import FaultReport


def generate_tracking_code() -> str:
    alphabet = string.ascii_uppercase + string.digits
    for _ in range(40):
        tail = "".join(secrets.choice(alphabet) for _ in range(8))
        code = f"CMSA-{tail}"
        if not FaultReport.objects.filter(tracking_code=code).exists():
            return code
    raise RuntimeError("Could not allocate a unique tracking code")
