from __future__ import print_function

import os

# from wsgiref.simple_server import make_server
# from pyramid.config import Configurator
# from pyramid.view import view_config, view_defaults

from screenutils import list_screens, Screen
#
#
# @view_defaults(
#     route_name="payload", renderer="json", request_method="POST"
# )
# class PayloadView(object):
#     """
#     View receiving of Github payload. By default, this view it's fired only if
#     the request is json and method POST.
#     """
#
#     def __init__(self, request):
#         self.request = request
#         # Payload from Github, it's a dict
#         self.payload = self.request.json
#         self.workstation =  os.path.expanduser('~') + os.environ['REPOPATH']
#         self.repo = os.environ['GHREPO']
#
#     @view_config(header="X-Github-Event")
#     def payload_push(self):
#         """
#         This method is a continuation of PayloadView process,
#         triggered if header HTTP-X-Github-Event
#         type is Push Issues
#         """
#         action = self.payload['action']
#         label = self.payload['label']
#         issue = self.payload['issue']
#
#         # just create a new branch when the user assign
#         # 'in progress' label into
#         if action == 'labeled' and label['name'] == 'in progress':
#             s_name = 'github-webhook'
#             s = Screen(s_name)
#             if s.exists:
#                 s.kill()
#
#             s.initialize()
#             s.enable_logs()
#
#             s.send_commands(
#                 'cd %s' % self.workstation
#             )
#
#             title = issue['title']
#
#             if len(issue['title'].split(' ')) > 1:
#                 title = '-'.join(issue['title'].split(' '))
#
#             new_branch = '%s-%s' % (
#                 issue['number'],
#                 title
#             )
#
#             s.send_commands(
#                 'git checkout -b %s' % new_branch
#             )
#
#             data = {
#                 'repository': self.repo,
#                 'username': os.environ['GHUSER'],
#                 'password': os.environ['GHPWD'],
#                 'new_branch': new_branch
#             }
#
#             s.send_commands(
#                 'git push https://{username}:{password}@{repository} {new_branch}'.format(**data)
#             )
#
#         return {}
#
#
# if __name__ == "__main__":
#     config = Configurator()
#
#     config.add_route("payload", "/payload")
#     config.scan()
#
#     app = config.make_wsgi_app()
#     server = make_server("0.0.0.0", 8080, app)
#     server.serve_forever()

from flask import Flask, request

app = Flask(__name__)

# Change ngrok listening port accordingly
# ./ngrok http 5000


@app.route("/payload", methods=['POST'])
def payload():
    payload = request.json
    workstation =  os.path.expanduser('~') + os.environ['REPOPATH']
    repo = os.environ['GHREPO']


    action = payload['action']
    label = payload['label']
    issue = payload['issue']

    # just create a new branch when the user assign
    # 'in progress' label into
    if action == 'labeled' and label['name'] == 'in progress':
        s_name = 'github-webhook'
        s = Screen(s_name)
        if s.exists:
            s.kill()

        s.initialize()

        s.send_commands(
            'cd %s' % workstation
        )

        title = issue['title']

        if len(issue['title'].split(' ')) > 1:
            title = '-'.join(issue['title'].split(' '))

        new_branch = '%s-%s' % (
            issue['number'],
            title
        )

        s.send_commands(
            'git checkout -b %s' % new_branch
        )

        data = {
            'repository': repo,
            'username': os.environ['GHUSER'],
            'password': os.environ['GHPWD'],
            'new_branch': new_branch
        }

        s.send_commands(
            'git push https://{username}:{password}@{repository} {new_branch}'.format(**data)
        )
    return 'ok'
