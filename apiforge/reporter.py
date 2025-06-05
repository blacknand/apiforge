import logging
import threading
from typing import Dict, Any
from colorama import Fore, Style

class Reporter:
    def __init__(self, output_dir: str = "reports"):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("APIForge")
        self.output_dir = output_dir
        self.results = []

    def log_generic_output(self, output: Any, method: str = "null_method"):
        if method: self.logger.info(f"[INFO] {method} -> {output}")
        else: self.logger.info(f"[INFO] {output}")

    def log_api_result(self, test: Dict[str, Any], result: Any, success: bool):
        status = "PASS" if success else "FAIL"
        color = "\033[32m" if success else "\033[31m"  
        reset = "\033[0m"  
        thread_name = threading.current_thread().name
        self.logger.info(f"({thread_name}) Test {test['method']} {test['endpoint']} [{test['params']}]: {status} - Result: {color}{result}{reset}")

    def log_util_response(self, test: Dict[str, Any], result: Any, success: bool):
        status = "PASS" if success else "FAIL"
        color = "\033[32m" if success else "\033[31m"  
        reset = "\033[0m"  
        self.logger.info(f"[TEST_UTIL] payload: {test}: {status} - Result: {color}{result}{reset}")

    def log_error(self, method: str, error: str):
        self.logger.info(f"{Fore.RED}[ERROR] {Style.RESET_ALL} {method}: {error}")