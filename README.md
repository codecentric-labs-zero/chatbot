# chatbot
a simple chatbot web app

---

#### SMS via messagebird.com
* Create an account on the platform
* Create an API key [here](https://dashboard.messagebird.com/app/en/developers/access)

   There are `test` and `live` API key. If you use `test`, all actions will be performed but no SMS will be sent and no charges applied.
   
* API key should be set in Heroku as Config variable.
* Buy a phone number. US phone number is $0,50/month (min 3 months) and one sms is $0,005. Receiving an SMS is free. Best option for testing.
* To be able to send SMS to USA or Canada you need to send request to Messagebird.

* On number settings set an action to be performed when SMS is received.
   If no action is triggered, contact messagebird support to remove safety filters.
* For sending an SMS from backend there is [python-rest-api](https://github.com/messagebird/python-rest-api).
