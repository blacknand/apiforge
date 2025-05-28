- To run and capture stdout
```bash
pytest tests/ --log-cli-level=INFO -vv
```


- To run only failing tests
```bash
pytest tests/ --log-cli-level=INFO -vv --lf --new-first
```