run:
    cd tests && /usr/local/bin/python3 test_integration.py

install BRANCH="develop":
    pip install git+https://github.com/fast-crawler/fastcrawler.git@{{BRANCH}} --force-reinstall

test arg=".": 
    pytest  --tb=short  -v --show-capture stdout -k {{arg}}
