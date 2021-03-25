.. Probe-Ably documentation master file, created by
   sphinx-quickstart on Mon Mar 22 23:07:40 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Probe-Ably |parrot|
=======================================================================================================================

Probe-Ably is a framework designed for PyTorch to support researchers in the implementation of probes for neural representations in a flexible and extensible way.

The core facility provided by Probe-Ably is the encapsulation of the end-to-end experimental probing pipeline. Specifically, Probe-Ably provides a complete implementation of the core tasks necessary for probing neural representations, starting from the configuration and training of heterogeneous probe models, to the calculation and visualization of metrics for the evaluation.

The probing pipeline and the core tasks operate on a set of abstract classes, making the whole framework agnostic to the specific representation, auxiliary task, probe model, and metrics used in the concrete experiments.


Architectural Design
^^^^^^^^^^^^^^^^^^^^

.. |parrot| image:: everythingsfineparrot.gif
   :scale: 20 %
.. image:: diagram.png

This architectural design allows the user to:

- Configure and run probing experiments on different representations and auxiliary tasks in parallel;
- Automatically generate control tasks for the probing, allowing the computation of inter-model metrics such as Selectivity;
- Extend the suite of probes with new models without the need to change the core probing pipeline;
- Customize, implement and adopt novel evaluation metrics for the experiments.

.. toctree::
   :maxdepth: 2
   :caption: Get started

   installation
   quicktour

.. toctree::
   :maxdepth: 2
   :caption: Advanced

   advanced/configurations
   advanced/inter_metrics
   advanced/intra_metrics

.. toctree::
   :maxdepth: 2
   :caption: Utils

   utils/grid_factory

.. toctree::
   :maxdepth: 1
   :caption: About Us

   contacts

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
