from __future__ import print_function

import os

# from wsgiref.simple_server import make_server
# from pyramid.config import Configurator
# from pyramid.view import view_config, view_defaults

from screenutils import list_screens, Screen

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
            'git pull && git checkout hml'
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
