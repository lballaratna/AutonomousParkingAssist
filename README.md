*****How to run the files under tests folder*****

1) pytest tests/test_park.py -v 
     (or)
python -m pytest tests/test_park.py -v

*****to run all tests*****
2) python -m pytest -v
   

*****How do you check whether pytest discovers your tests without executing them*****
3) python -m pytest --collect-only -q 

*****How do you run a specific test*****
4) python -m pytest tests/test_park.py::test_empty_space -v





