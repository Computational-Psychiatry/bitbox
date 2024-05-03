.. testingSphinx documentation master file, created by
   sphinx-quickstart on Fri Mar 29 02:51:34 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. 
   Download autodoc, then go to file -> preferences -> 
   "autoDocstring.docstringFormat": "sphinx"
.. 
   SETUP
   sphinx-quickstart -> make html 

   cd into the docs folder. To make updates, you need to run make html.
   1. make html
   2. sphinx-autobuild . _build/html

   Run this if you need to do occasioanl updates?
   In the src folder though.
   sphinx-apidoc -o docs bitbox

bitbox
=========================================

1. Home
-----------------------------------------

2. Installation
-----------------------------------------

3. Tutorials
-----------------------------------------

4. Advanced Topics
-----------------------------------------

5. API 
-----------------------------------------
.. toctree::
   :maxdepth: 2
   :caption: 5.1 API Reference

   index_references/face_backend
   index_references/utilities
   
   index_references/coordination
   index_references/expressions
   index_references/kinematics

.. include references the '.rst' files

6. Development
-----------------------------------------


