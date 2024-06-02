from flask import Blueprint, redirect, url_for, request, render_template_string, jsonify

from .extensions import db
from .models import PKey
import uuid

main = Blueprint('main', __name__)

# HTML template for the form and QR code verification
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Product Code Verification</title>
    <style>
        table {
            width: 50%;
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 18px;
            text-align: left;
        }
        th, td {
            padding: 12px;
            border: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Verify Product Code</h1>
    <form method="post" action="/verify">
        <label for="code">Product Code:</label>
        <input type="text" id="code" name="code" required>
        <button type="submit">Verify</button>
    </form>
    <hr>
    <h2>Product Keys</h2>
    {{ list|safe }}
    {% if message %}
        <p>{{ message }}</p>
    {% endif %}
</body>
</html>
"""

def check_code_in_db(code):
    pkeys = PKey.query.all()
    codes = [pk.uuid for pk in pkeys]
    return code in codes

@main.route('/')
def index():
    pkeys = PKey.query.all()
    strains = [pk.strain for pk in pkeys]
    codes = [pk.uuid for pk in pkeys]
    # total = [f"<li>{ item }</li>" for item in zip(strains, codes)]

    table_rows = "".join([f"<tr><td>{strain}</td><td>{code}</td></tr>" for strain, code in zip(strains, codes)])
    table_html = f"""
    <table>
        <thead>
            <tr>
                <th>Strain</th>
                <th>Product Code</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    """
    return render_template_string(html_template, list=table_html) 

@main.route('/add/<strain>')
def add_user(strain):
    db.session.add(PKey(strain=strain, uuid=str(uuid.uuid4())))
    db.session.commit()
    return redirect(url_for("main.index"))

@main.route('/verify', methods=['POST'])
def verify_code():
    message = ""
    code = request.form['code']
    if check_code_in_db(code):
        message = "This code is legitimate."
    else:
        message = "This code is not legitimate."
    
    return render_template_string(html_template, message=message)

@main.route('/verify_code', methods=['GET'])
def verify_code_from_url():
    code = request.args.get('code')
    if code:
        if check_code_in_db(code):
            message = "This code is legitimate."
        else:
            message = "This code is not legitimate."
        return render_template_string(html_template, message=message)
    else:
        return redirect(url_for("main.index"))
    