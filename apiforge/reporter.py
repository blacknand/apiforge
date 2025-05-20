import logging
from typing import Dict, Any
from colorama import Fore, Style

class Reporter:
    def __init__(self, output_dir: str = "reports"):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("APIForge")
        self.output_dir = output_dir
        self.results = []

    def log_generic_output(self, output: Any):
        self.logger.info("______________________________________________________ generic output _______________________________________________________")
        self.logger.info(output)
        self.logger.info("______________________________________________________ generic output _______________________________________________________")

    def log_api_result(self, test: Dict[str, Any], result: Any, success: bool):
        status = "PASS" if success else "FAIL"
        self.logger.info(f"Test {test['method']} {test['endpoint']}: {status} - Result: {result}")

    def log_util_response(self, test: Dict[str, Any], result: Any, success: bool):
        status = "PASS" if success else "FAIL"
        self.logger.info(f"[TEST_UTIL] payload: {test}: {status} - Result: {result}")

    def log_error(self, method: str, error: str):
        self.logger.info(f"{Fore.RED}[ERROR] {Style.RESET_ALL} {method}: {error}")