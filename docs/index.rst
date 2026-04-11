*************************
peaker Documentation
*************************

This is the documentation for ``peaker``,
a package that creates a PDF report for the regression tests that
track memory peak and run times during a desired period of
time. The report has a two plots per test, one of the peak
memory versus dates and another for runtimes versus
dates. It also contains a table with all tests, the instrument
mode tested, the corresponding latest memory peak, the number
of data points during that period, the difference of the median
at the end of the period minus the median at the start of the
period, and the page in the PDF where the plot can be found.
The table is ordered by largest positive differences (memory
increases at the end of the period with respect to the start) to
lowest (if the differences are negative, it means an improvement
at the end of the period with respect to the start of the period).


.. toctree::
   :maxdepth: 2

   peaker.description.rst


Reference/API
=============

.. automodapi:: peaker
