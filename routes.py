from flask import Blueprint, render_template, request, redirect, url_for
from db import db  # Import the db from db.py
from models import Contact  # Import your model here

main = Blueprint('main', __name__)

# Formatacao do numero de telefone
def format_phone(phone):
    if len(phone) == 11:  # (99)9.9999-9999
        return f"({phone[:2]}) {phone[2]}{phone[3:7]}-{phone[7:]}"
    elif len(phone) == 10:  # (99)9999-9999
        return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
    elif len(phone) == 8:  # 9.9999-9999 ou 9999-9999
        return f"{phone[:4]}-{phone[4:]}"
    elif len(phone) == 7:  # 9.9999-9999
        return f"{phone[0]}.{phone[1:5]}-{phone[5:]}"
    return phone  # Retorna o número original se não corresponder a nenhum formato

@main.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('list.html', contacts=contacts, format_phone=format_phone)

@main.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_contact = Contact(
            name=request.form['name'],
            phone=request.form['phone'],
            email=request.form['email']
        )
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('add.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    contact = Contact.query.get_or_404(id)
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.phone = request.form['phone']
        contact.email = request.form['email']
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('edit.html', contact=contact)

@main.route('/delete/<int:id>')
def delete(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('main.index'))
