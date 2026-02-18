import os
import secrets
import logging

logger = logging.getLogger(__name__)

_secret_key = os.getenv('FLASK_SECRET_KEY')
if not _secret_key:
    _secret_key = secrets.token_hex(32)
    logger.warning(
        "FLASK_SECRET_KEY is not set. A temporary key has been generated. "
        "Sessions will not persist across restarts."
    )

FLASK_SECRET_KEY: str = _secret_key
FLASK_DEBUG: bool = os.getenv(
    'FLASK_DEBUG', 'False').strip().lower() in ('true', '1', 'yes')
FLASK_RUN_PORT: int = int(os.getenv('FLASK_RUN_PORT', '8080'))
FLASK_RUN_HOST: str = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
