|Actions Status| |Coveralls Status| |Updates|

api
===

- Deploy to AWS Lambda with ``zappa deploy dev`` and ensure that the ``remote_env.json`` at the ``s3`` path given in the settings contains the correct db credentials.
- Deploy locally by running the ``app.py``. Be sure to provide a Postgres instance to talk to, and pass the credentials via the environment, f.ex: ``PG_CREDS=postgresql://user:pass@host:port/database python app.py`` and visit ``127.0.0.1:5000``

Running
-------

Run locally after installing Python 3.6 (Zappa doesn't currently support higher than that) by simply running app.py

.. |Actions Status| image:: https://github.com/multiplechoice/api/workflows/pytest/badge.svg
.. |Coveralls Status| image:: https://coveralls.io/repos/github/multiplechoice/api/badge.svg?branch=master
  :target: https://coveralls.io/github/multiplechoice/api?branch=master
.. |Updates| image:: https://pyup.io/repos/github/multiplechoice/api/shield.svg
  :target: https://pyup.io/repos/github/multiplechoice/api/
  :alt: Updates
