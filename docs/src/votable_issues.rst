.. include:: common_links.inc

.. _votable_issues:

Votable Issues
==============

You can help us to prioritise development of new features by leaving a 👍
reaction on the first comment of any issue that has a label of
:link-badge:`https://github.com/SciTools/iris/issues?q=is%3Aopen+is%3Aissue+label%3A%22Feature%3A+Voteable%22+sort%3Areactions-%2B1-desc,"Feature: Voteable",cls=badge-info text-white`.


Below is a list of all current enhancement issues from our github
project ordered by the amount of 👍.

Please note that there is more development activity than what is on the below
table, this is focusing only on the voteable issues.

.. todo:: add link to the repo holding the json file

.. todo:: spell check "votable (this one) vs voteable" and update all occurences.

.. note:: The data in this table is updated daily and is sourced from HERE.
          For the latest data please see the `voteable issues on GitHub`_


.. raw:: html

   <table id="example" class="display" style="width:100%">
      <thead>
         <tr>
            <th>👍</th>
            <th>Issue</th>
            <th>Author</th>
            <th>Title</th>
         </tr>
      </thead>
   </table>

   <!-- JS to enable the datatable features: sortable, paging, search etc
           https://datatables.net/reference/option/
           https://datatables.net/  -->

   <script type="text/javascript">
        $(document).ready(function() {
           $('#example').DataTable( {
              <!-- "ajax": 'votable-issues.json', -->
              "ajax": 'https://gist.githubusercontent.com/tkknight/8a3fdf81b46554d0b107c5681b7c78e5/raw/dc8eff21a4c7fc465c4e5458dc3573d3dc5d222e/votable-issues.json',
              "pageLength": 20,
              "order": [[ 0, "desc" ]]
           } );
        } );
   </script>

