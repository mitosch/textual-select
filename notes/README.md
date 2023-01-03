# Development Notes

## Todos

* [ ] Optimize error message, when `picker_mount` selector can't find element
* [ ] Fulfill 100% test coverage

## Testing

```bash
# run tests
poetry run pytest

# run tests with coverage report:
poetry run pytest --cov=textual_select/ tests/
poetry run coverage html
```
