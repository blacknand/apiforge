- to run without tests
```bash
python3 -c "from apiforge.core import APIForge; forge = APIForge.from_config('configs/api_config.yaml'); results = forge.run_config_tests('configs/api_config.yaml')"
```
- to run with tests
```bash
pytest tests/ -vv
```