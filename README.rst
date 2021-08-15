fastanalizer - Fast protein domain analysis tool
=============================================

Installation
------------

You can install fastanalize like any other Python package,
using ``pip`` to download it from PyPI_::

    $ pip install fastanalize

or using ``setup.py`` if you have downloaded the source package locally::

    $ python setup.py build
    $ sudo python setup.py install


Usage
-----

After installation, to use `` fastanalizer`` just invoke it in the folder where the multifasta is located:

    $ fastanalizer myfasta.fa

You may also define a title to your job:

    $ fastanalizer --title "Example" myfasta.fa

It is possible to define the type of image output. Default is HTML.

    $ fastanalizer --output SVG myfasta.fa

Example
-------

Fastanalizer performs protein sequence analysis in 5 steps:

1. **Fasta sequences analysis:**

    The first step analyzes basic metrics of the delivered multifast, such as quantity and size of sequences, shortest and longest sequences, standard deviation between sequences size and the amino acid distribution of the sequences. The results are saved in the ``general`` folder.

.. image:: https://github.com/alezanatta/fastanalizer/blob/main/example/svg/general/metrics.svg
:width: 800

.. image:: https://github.com/alezanatta/fastanalizer/blob/main/example/svg/general/aa.svg
:width: 800
:alt:

2. **Functional domains analysis:**

    The second step is the search for functional domains in the delivered proteins. The analysis is done using the NCBI Batch Cd-Search. The results are saved in the ``domainsearch`` folder. Each file inside the folder has a maximum information of 2000 sequences. There is no limit to the total number of sequences and the execution time of this step varies according to the number of sequences provided.

3. **Sequence trimming**

    Under construction

4. **Sequence alignment**

    Under construction

5. **Phylogenetic analysis**

.. image:: https://github.com/alezanatta/fastanalizer/blob/main/example/svg/tree/tree.svg
    :width: 1000


Changelog
---------

    Under construction