from __future__ import print_function

import os
import random

from screenutils import list_screens, Screen

from flask import Flask, request

app = Flask(__name__)

# Change ngrok listening port accordingly
# ./ngrok http 5000


@app.route('/')
def up():
    return 'UP!'


@app.route("/payload", methods=['POST'])
def payload():
    payload = request.json
    # print('*'*10)
    workstation =  os.path.expanduser('~') + os.environ['REPOPATH']
    repo = os.environ['GHREPO']

    action = payload.get('action', '')
    label = payload.get('label', '')
    issue = payload.get('issue', '')

    # just create a new branch when the user assign
    # 'in progress' label into
    if (
        action and
        label and
        issue and
        action == 'labeled' and
        label['name'] == 'in progress'
    ):
        # useful to implement the label at commits,
        # e.g: label/issue should be the name of the branch.
        labels = [l['name'] for l in issue['labels'] if l['name']]
        labels.remove('in progress')

        branch_label = '' if not labels else random.choice(labels)

        branch_format = '{label}/issue-{number}' if branch_label else '{number}'

        branch_info = {
            'label': branch_label,
            'number': issue['number']
        }

        new_branch = branch_format.format(**branch_info)

        # screen name
        s_name = 'github-webhook'

        s = Screen(s_name)
        if not s.exists:
            s.initialize()

        s.send_commands(
            'cd %s' % workstation
        )

        data = {
            'repository': repo,
            'username': os.environ['GHUSER'],
            'password': os.environ['GHPWD'],
            'default_b': 'hml',
            'new_branch': new_branch
        }

        s.send_commands(
            'git pull https://{username}:{password}@{repository} {default_b}'.format(**data)
        )

        s.send_commands(
            'git checkout %s' % data['default_b']
        )

        s.send_commands(
            'git branch -d %s' % new_branch
        )

        s.send_commands(
            'git checkout -b %s' % new_branch
        )

        s.send_commands(
            'git push https://{username}:{password}@{repository} {new_branch}'.format(**data)
        )

    return 'ok'

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=8080)

