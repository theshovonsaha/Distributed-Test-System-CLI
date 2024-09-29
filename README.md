# Distributed System Testing Framework

This framework provides tools for testing distributed systems, with a focus on a key-value store implementation.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/distributed-testing-framework.git
   ```
2. Navigate to the project directory:
   ```
   cd distributed-testing-framework
   ```
3. Create a virtual environment:
   ```
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   - On Unix or MacOS:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```
5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running Tests

To run all tests:

```
python -m cli.main run
```

To run a specific test suite:

```
python -m cli.main run --suite integration
```

### Using the Key-Value Store

To set a value:

```
python -m cli.main kv --key mykey --value myvalue
```

To get a value:

```
python -m cli.main kv --key mykey
```

### Generating Reports

To generate a test report:

```
python -m cli.main report --output myreport.txt
```

## Creating New Tests

1. Create a new test file in the appropriate directory (e.g., `tests/unit/test_new_feature.py`).
2. Define your test functions. For example:
   ```python
   async def test_new_feature():
       # Your test code here
       assert True
   ```
3. Add your test to a test suite in `cli/main.py`:
   ```python
   test_suite.add_test(TestCase("New Feature Test", test_new_feature))
   ```

## Advanced Testing Techniques

### Property-Based Testing

We use the `hypothesis` library for property-based testing. See `advanced_testing/property_based.py` for examples.

### Fuzz Testing

Our fuzz testing implementation randomly generates input data to test the robustness of the system. See `advanced_testing/fuzz_testing.py` for details.

## Performance Monitoring

To run a performance test and generate charts:

```
python -m monitoring.performance
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Shovon Saha - theshovonsaha@gmail.com

Project Link: [https://github.com/theshovonsaha/Distributed-Test-System-CLI](https://github.com/theshovonsaha/Distributed-Test-System-CLI)
