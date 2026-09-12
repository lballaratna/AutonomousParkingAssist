*****How to run the files under tests folder*****

==> pytest tests/test_park.py -v 
     (or)
python -m pytest tests/test_park.py -v

*****to run all tests*****
==> python -m pytest -v
   

*****How do you check whether pytest discovers your tests without executing them*****
==> python -m pytest --collect-only -q 

*****How do you run a specific test*****
==> python -m pytest tests/test_park.py::test_empty_space -v





