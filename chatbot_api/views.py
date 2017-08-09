from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import requests
import os
import messagebird


def hello_world(request):
    return HttpResponse('hello world')


@csrf_exempt
def receive_sms(request):
    if request.method == 'POST':
        print(request.POST.get('id'))
        print(request.POST.get('recipient'))
        print(request.POST.get('originator'))
        print(request.POST.get('body'))
        print(request.POST.get('createdDatetime'))
        user = request.POST.get('originator')
        text = request.POST.get('body')
        # forward q to bot
        r = requests.post('https://cclz-chatbot.herokuapp.com/web/ask',
                          data={'question': text})
        answer = r.text
        send_sms_to_user(user, answer)
        return HttpResponse(status=200)
    else:
        print('method GET')
        return HttpResponse('GET req. not supported')


def send_sms_to_user(user, answer):
    client = messagebird.Client(os.getenv('MBIRD'))
    try:
        # Fetch the Balance object.
        balance = client.balance()
        print('  amount  : %s' % balance.amount)

        msg = client.message_create('12028525940', user, answer)

        # Print the object information.
        print('\nThe following information was returned as a Message object:\n')
        print('  id                : %s' % msg.id)
        print('  href              : %s' % msg.href)
        print('  direction         : %s' % msg.direction)
        print('  type              : %s' % msg.type)
        print('  originator        : %s' % msg.originator)

    except messagebird.client.ErrorException as e:
        print('\nAn error occured while requesting a Message object:\n')

        for error in e.errors:
            print('  code        : %d' % error.code)
            print('  description : %s' % error.description)
            print('  parameter   : %s\n' % error.parameter)
