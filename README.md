Go to <http://dev.fitbit.com/apps> and register an app.  Put your client id
and secret in `client.json`:

    {
      "client_id": "XXXXXX",
      "client_secret": "12345678901234567890123456789012"
    }

Run `python fitbit-req.py`.  This will prompt you to authorize the app
in your browser, and will then write `token.json`.  Now you can run
the other scripts, as in `python fitbit-sleep.py 2017-08-12`.
