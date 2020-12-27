# Copyright Iris contributors
#
# This file is part of Iris and is released under the LGPL license.
# See COPYING and COPYING.LESSER in the root of the repository for full
# licensing details.

"""
Scan the directory of iep files and extract their metadata.  The
metadata is passed to Jinja for filling out `index.rst.tmpl`.
"""

import glob
import jinja2
import logging
import re

# set logging level (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL)
logging.basicConfig(level=logging.INFO)

# the only place the IEP status needs to be defined
IEP_STATUS_LIST = [
    "Draft",
    "Accepted",
    "Rejected",
    "Withdrawn",
    "Deferred",
    "Final",
]


def autolog_info(message):
    """Automatically log the current function details.

    Parameters
    ----------
    message: Message to log
    """

    # Dump the message + the name of this function to the log.
    logging.info(" --> {}".format(message))


def iep_collect_details():
    """Scan the IEP files an extract the tags

    Returns
    --------
    return: dict of variables containing the IEP tags, to pass into a template
    """

    sources = sorted(glob.glob("IEP[0-9][0-9][0-9][0-9]-*.rst"))

    # regular expression for a tag, ie ":Author: Joe Bloggs"
    meta_re = ":([a-zA-Z\-]*): (.*)"

    ieps = {}
    source_count = len(sources)

    autolog_info("Found {} IEPs.  Extracting metadata...".format(source_count))

    for idx, source in enumerate(sources):
        autolog_info("   ({}/{}) {}".format(idx + 1, source_count, source))

        nr = int(re.match("IEP([0-9]{4}).*\.rst", source).group(1))

        with open(source) as f:
            lines = f.readlines()

            # use regex to find the colon separated tags
            tags = [re.match(meta_re, line) for line in lines]

            # remove empty entries
            tags = [match.groups() for match in tags if match is not None]

            # convert list into a dict
            tags = {tag[0]: tag[1] for tag in tags}

            # find the title, should be the line after the first '===' header.
            for idx, line in enumerate(lines[:-1]):
                if line[0] == "=":
                    break
            else:
                raise RuntimeError(
                    "IEP title not found.  Should have a equals '=' line before and after the title."
                )

            tags["IEP"] = source.split("-", 1)[:1][0]
            tags["Title"] = lines[idx + 1].strip().split("-", 1)[1]
            tags["Filename"] = source

        ieps[nr] = tags

    return {"ieps": ieps}


if __name__ == "__main__":
    iep_dict = iep_collect_details()

    autolog_info("Generating index...")

    # create a dict showing the count of each status for use in the
    # jinja template
    iep_status_count_dict = {}

    for iep_status in IEP_STATUS_LIST:
        counter = 0
        for iep in iep_dict["ieps"]:
            if iep_dict["ieps"][iep]["Status"] not in IEP_STATUS_LIST:
                msg = "IEP Status '{}' invalid.  Valid values are: {}".format(
                    iep_dict["ieps"][iep]["Status"], IEP_STATUS_LIST
                )
                raise RuntimeError(msg)

            if iep_dict["ieps"][iep]["Status"] == iep_status:
                counter += 1
        iep_status_count_dict[iep_status] = counter

    iep_dict["iep_status_count"] = iep_status_count_dict

    # render the rst and write to file
    template_file = "index.rst.tmpl"
    out_file = "index.rst"

    index = (
        jinja2.Environment(loader=jinja2.FileSystemLoader("./"))
        .get_template(template_file)
        .render(iep_dict)
    )

    with open(out_file, "w") as f:
        f.write(index)

    autolog_info("Done.")
