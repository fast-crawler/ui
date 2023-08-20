#  use PowerShell instead of sh:
# set shell := ["powershell.exe", "-c"]

run:
    cd tests && python atest_integration.py

install BRANCH="develop":
    pip install git+https://github.com/fast-crawler/fastcrawler.git@{{BRANCH}} --force-reinstall

test arg=".":
    pytest  --tb=short  -v --show-capture stdout --cov=fastcrawler_ui --cov-report term-missing -k {{arg}}
