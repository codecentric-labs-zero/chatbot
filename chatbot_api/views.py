from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import logging
import requests
import os
import messagebird

logger = logging.getLogger('testlogger')


def hello_world(request):
    return HttpResponse('hello world')


@csrf_exempt
def receive_sms(request):
    print('receive_sms')
    logger.warning('in method receive_sms')
    if request.method == 'POST':
        logger.warning(request.POST.get('id'))
        logger.warning(request.POST.get('recipient'))
        logger.warning(request.POST.get('originator'))
        logger.warning(request.POST.get('body'))
        logger.warning(request.POST.get('createdDatetime'))
        user = request.POST.get('originator')
        text = request.POST.get('body')
        # forward q to bot
        r = requests.post('https://cclz-chatbot.herokuapp.com/web/ask',
                          data={'question': text})
        answer = r.text
        send_sms_to_user(user, answer)
        return HttpResponse(status=200)
    else:
        logger.warning('method GET')
        return HttpResponse('GET req. not supported')


def send_sms_to_user(user, answer):
    client = messagebird.Client(os.getenv('MBIRD'))
    try:
        # Fetch the Balance object.
        balance = client.balance()
        logger.info('  amount  : %s' % balance.amount)

        msg = client.message_create('12028525940', user, answer)

        # Print the object information.
        logger.info('\nThe following information was returned as a Message object:\n')
        logger.info('  id                : %s' % msg.id)
        logger.info('  href              : %s' % msg.href)
        logger.info('  direction         : %s' % msg.direction)
        logger.info('  type              : %s' % msg.type)
        logger.info('  originator        : %s' % msg.originator)

    except messagebird.client.ErrorException as e:
        logger.info('\nAn error occured while requesting a Message object:\n')

        for error in e.errors:
            logger.info('  code        : %d' % error.code)
            logger.info('  description : %s' % error.description)
            logger.info('  parameter   : %s\n' % error.parameter)
