.. LunaticAI documentation master file, created by
   sphinx-quickstart on Tue Apr 16 15:02:44 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
   For more infos see: https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html

LunaticAI Documentation
=======================

.. Add Link to Github
.. include:: _include.md
  :parser: myst_parser.sphinx_
  :start-after: ## $$ GitHubRepoLink
  :end-before: ## $$

.. toctree::
   :hidden:

   Home <self>

.. toctree::
   :maxdepth: 1
   :caption: Getting Started:

   Installation <docs/Install>
   Quickstart

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   docs/Agents 
   Configuration <conf/ConfigFiles>
   docs/Rules

.. toctree::
   :maxdepth: 2
   :caption: Code and API:

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Readme
======

.. include:: _readme_link.rst
.. _readme-workflow: