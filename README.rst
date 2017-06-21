|Build Status| |Coveralls Status| |Requirements Status|

api
===

- Deploy to AWS Lambda with `zappa deploy dev` and ensure that the `remote_env.json` at the `s3` path given in the settings contains the correct db credentials.
- Deploy locally by running the `app.py`. Be sure to provide a Postgres instance to talk to, and pass the credentials via the environment, f.ex: `PG_CREDS=postgresql://user:pass@host:port/database python app.py` and visit `127.0.0.1:5000`


.. |Build Status| image:: https://travis-ci.org/multiplechoice/api.svg?branch=master
  :target: https://travis-ci.org/multiplechoice/api
.. |Coveralls Status| image:: https://coveralls.io/repos/github/multiplechoice/api/badge.svg?branch=master
  :target: https://coveralls.io/github/multiplechoice/api?branch=master
.. |Requirements Status| image:: https://requires.io/github/multiplechoice/api/requirements.svg?branch=master
  :target: https://requires.io/github/multiplechoice/api/requirements/?branch=master
  :alt: Requirements Status
