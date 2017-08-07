from django.shortcuts import render
from django.http import HttpResponse
from watson_developer_cloud import ConversationV1
from django.http import JsonResponse

from os import environ

conversation = ConversationV1(
    url=environ.get('BOT_URL'),
    username=environ.get('BOT_USERNAME'),
    password=environ.get('BOT_PASSWORD'),
    version='2017-04-21')

workspace_id = environ.get('BOT_ID')


def hello_world(request):
    if 'old_answer' in request.session:
        del request.session['old_answer']

    return render(request, 'base.html', {'greeting': 'hello world'})


def ping(request):
    return HttpResponse("I am alive.", content_type="text/plain")


def ask(request):
    if request.method == "POST":
        response = "missing parameters"
        old_answer = request.session.get('old_answer')
        try:
            question = request.POST['question']
            if not old_answer:
                answer = conversation.message(workspace_id=workspace_id, message_input={
                    'text': question})
                response = answer['output']['text']
                request.session['old_answer'] = answer
            else:
                answer = conversation.message(workspace_id=workspace_id, message_input={'text': question},
                                              context=old_answer['context'])
                request.session['old_answer'] = answer
                response = answer['output']['text']
        except Exception as e:
            print(e)
            pass
        return JsonResponse(response, safe=False)

    return HttpResponse("I am alive.", content_type="text/plain")
