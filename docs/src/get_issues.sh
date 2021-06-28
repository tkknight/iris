# https://github.com/SciTools/iris/issues?q=is%3Aopen+label%3A%22Feature%3A+Voteable%22+sort%3Areactions-%2B1-desc+reactions%3A%3E1
# https://api.github.com/repos/scitools/iris/issues
rm -f issues.json

# https://docs.github.com/en/rest/reference/issues
curl https://api.github.com/repos/scitools/iris/issues?state=open > issues.json

python create_issue_csv.py
