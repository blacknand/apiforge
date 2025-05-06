import logging
from typing import Dict, Any

class Reporter:
    # logger = logging.getLogger(__name__)

    def __init__(self, output_dir: str = "reports"):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("APIForge")
        self.output_dir = output_dir
        self.results = []

    def log_result(self, test: Dict[str, Any], result: Any, success: bool):
        status = "PASS" if success else "FAIL"
        self.logger.info(f"Test {test['method']} {test['endpoint']}: {status} - Result: {result}")