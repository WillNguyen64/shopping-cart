from .common.app import create_app
from .common.logger import get_logger
from . import models

logger = get_logger(__name__)

logger.info("Starting Shopping Cart API")
models.Base.metadata.create_all(bind=models.engine)
app = create_app()
