from flask import Flask, request, render_template_string, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

# HTML template for the form and QR code verification
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Product Code Verification</title>
</head>
<body>
    <h1>Verify Product Code</h1>
    <form method="post">
        <label for="code">Product Code:</label>
        <input type="text" id="code" name="code" required>
        <button type="submit">Verify</button>
    </form>
    {% if message %}
        <p>{{ message }}</p>
    {% endif %}
</body>
</html>
"""

def check_code_in_db(code):
    conn = sqlite3.connect('product_codes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM product_codes WHERE code = ?', (code,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def add_code_to_db(code):
    conn = sqlite3.connect('product_codes.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO product_codes (code) VALUES (?)', (code,))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def verify_code():
    message = ""
    if request.method == 'POST':
        code = request.form['code']
        if check_code_in_db(code):
            message = "This code has already been used."
        else:
            add_code_to_db(code)
            message = "The code has been successfully verified and added to the database."
    
    return render_template_string(html_template, message=message)

@app.route('/verify', methods=['GET'])
def verify_code_from_url():
    code = request.args.get('code')
    if code:
        if check_code_in_db(code):
            message = "This code has already been used."
        else:
            add_code_to_db(code)
            message = "The code has been successfully verified and added to the database."
        return render_template_string(html_template, message=message)
    else:
        return redirect(url_for('verify_code'))

if __name__ == '__main__':
    app.run(debug=True)