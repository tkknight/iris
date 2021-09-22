import csv
import logging
import os
from pathlib import Path

from github import Github

# set logging level (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL)
logging.basicConfig(level=logging.INFO)

TOKEN_FILE = "github-token.txt"
ISSUE_RST = ":issue_only:`{number}`"
AUTHOR_RST = ":author:`{author}`"


def autolog_info(message):
    # Dump the message + the name of this function to the log.
    logging.info(" --> {}".format(message))


def get_token(filename):
    """load the github api token from disk"""
    token_file = Path(filename)
    if not token_file.exists():
        raise IOError(
            "Please create a token at github.com, and save "
            + "it in {}".format(token_file)
        )

    token = token_file.read_text().strip()
    return token


full_path_token = os.path.join(os.getenv("HOME"), ".api_keys", TOKEN_FILE)
autolog_info(f"Loading GitHub API token from: {full_path_token}")
token = get_token(full_path_token)

# https://pygithub.readthedocs.io/en/latest/github.html?highlight=page
g = Github(token, per_page=100)


# -- get issues --------------------------------------------------------------
# curl -i "https://api.github.com/repos/scitools/iris/issues"
repo = g.get_repo("scitools/iris")

# https://pygithub.readthedocs.io/en/latest/github_objects/Issue.html#github.Issue.Issue
issues = repo.get_issues(state="open", labels=["Feature: Voteable"])
total_issues = issues.totalCount

autolog_info(
    f"GitHub API: Issues (including pull requests) to process: {total_issues}"
)

# setup csv output file
csv_file = csv.writer(open("votable-issues.csv", "w"))
CSV_HEADER = ["👍", "Issue", "Author", "Title"]
csv_file.writerow(CSV_HEADER)


for i, issue in enumerate(issues):
    plus_one_count = 0
    foo = issue.get_reactions()

    for r in issue.get_reactions():

        if r.content == "+1":
            plus_one_count = plus_one_count + 1

    autolog_info(
        f"Number = {issue.number :>5}  "
        f"Likes = {plus_one_count :>4}  "
        f"Author = {issue.user.login :<20}  "
        f"Title = {issue.title}"
    )
    csv_file.writerow(
        [
            plus_one_count,
            ISSUE_RST.format(number=issue.number),
            AUTHOR_RST.format(author=issue.user.login),
            issue.title,
        ]
    )
