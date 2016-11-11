# monitor_stocks

The following is only meant for educational purposes!

```
EMAIL_USER='myemail' EMAIL_PASSWORD='mypassword' python monitor.py
```

The above will monitor the symbols mentioned at
https://gist.githubusercontent.com/vvb/7606bf8e35074953987ddbdaa9f01d59/raw/rules.json

and send an email alert if the price goes above the specified 'high' or
below the specified 'low'

I have tested this only with a gmail email address, which needs to be
configured in 'lesser secure mode' to allow third-party apps to send emails.
