from flask import render_template
from . import controller
from flask import request, redirect, url_for


@controller.route('/admin', methods=['GET'])
def admin_index():
    username = request.cookies.get('username')
    if username is None:
        return redirect(url_for('controller.index_index'))
    return render_template('admin/index.html', username=username)
