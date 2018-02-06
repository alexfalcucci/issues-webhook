from __future__ import print_function

import os

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
        s_name = 'github-webhook'
        s = Screen(s_name)
        if s.exists:

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
    app.run(threaded=True,host='0.0.0.0', port=8080)
