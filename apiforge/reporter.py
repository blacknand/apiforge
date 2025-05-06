import logging
from typing import Dict, Any

class TestReporter:
    # logger = logging.getLogger(__name__)

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("APIForge")

    def log_result(self, test: Dict[str, Any], result: Any, success: bool):
        status = "PASS" if success else "FAIL"
        self.logger.info(f"Test {test['method']} {test['endpoint']}: {status} - Result: {result}")