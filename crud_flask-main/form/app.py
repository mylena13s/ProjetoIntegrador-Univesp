from flask import Flask, flash, render_template, jsonify, request, redirect, url_for, session
from datetime import datetime
import pyrebase

config = {
    "apiKey": "AIzaSyC7Kne4MWoZx5-v_XhrAcKKw2ndn-98zmE",
    "authDomain": "tabelas-45b2b.firebaseapp.com",
    "databaseURL": "https://tabelas-45b2b-default-rtdb.firebaseio.com",
    "projectId": "tabelas-45b2b",
    "storageBucket": "tabelas-45b2b.appspot.com",
    "messagingSenderId": "621012930482",
    "appId": "1:621012930482:web:7c5b015baa10f9c37bdeab"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__)
app.secret_key = 'admin123'


@app.route('/')
def home():
    if 'user_id' in session:
        user_info = db.child("users").child(session['user_id']).get().val()
        return render_template('painel.html', user_info=user_info)
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['pwd']
        cpf = request.form['cpf']
        tipo_usuario = request.form['tipo_usuario']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            data = {"email": email, "password": password, "cpf": cpf, "tipo_usuario": tipo_usuario}
            db.child("users").child(user['localId']).set(data)
            flash('Login criado com sucesso!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(e)
            flash('Erro na criação de Login!', 'error')
            return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pwd')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user_id'] = user['localId']
            user_info = db.child("users").child(user['localId']).get().val()
            session['user_info'] = user_info  # Store the user info in the session
            session['tipo_usuario'] = user_info['tipo_usuario']
            if session['tipo_usuario'] == 'coordenador':
                return redirect(url_for('painel'))
            else:
                return redirect(url_for('painel'))
        except Exception as e:
            print(e)
            flash('Credenciais de login incorretas. Por favor, tente novamente.')
            return redirect(url_for('login'))  # Redireciona o usuário de volta para a página de login

@app.route('/painel', methods=['GET', 'POST'])
def painel():
    if 'user_id' in session and session['tipo_usuario'] == 'coordenador':
        # Recupera todos os idosos do banco de dados
        idosos_dict = db.child("idoso").get().val()
        idoso = ...
        # Se idosos é None, define como uma lista vazia
        idosos = list(idosos_dict.values()) if idosos_dict else []

        if request.method == 'POST':
            nome = request.form.get('nome')
            cpf_cordenador = request.form.get('cpf_cordenador')
            cargo = request.form.get('cargo')
            telefone = request.form.get('telefone')
            data = {
                "nome": nome,
                "cpf_cordenador": cpf_cordenador,
                "cargo": cargo,
                "telefone": telefone
            }
            db.child("coordenadores").push(data)

        coordenadores = db.child("coordenadores").get().val() or {}
        user_info = db.child("users").child(session['user_id']).get().val() or {}
        return render_template('painel.html', coordenadores=coordenadores, user_info=user_info, idosos=idosos, idoso=idoso)
    else:
        return redirect(url_for('login'))
    
@app.route('/view_coordinator')
def view_coordinator():
    if 'user_id' in session and session['tipo_usuario'] == 'coordenador':
        user_info = db.child("users").child(session['user_id']).get().val() or {}
        return render_template('view_coordinator.html', user_info=user_info)
    else:
        return redirect(url_for('login'))

@app.route('/update_coordinator', methods=['GET', 'POST'])
def update_coordinator():
    if 'user_id' in session and session['tipo_usuario'] == 'coordenador':
        if request.method == 'POST':
            nome = request.form.get('nome')
            cpf_cordenador = request.form.get('cpf_cordenador')
            cargo = request.form.get('cargo')
            telefone = request.form.get('telefone')
            data = {
                "nome": nome,
                "cpf_cordenador": cpf_cordenador,
                "cargo": cargo,
                "telefone": telefone
            }
            db.child("users").child(session['user_id']).update(data)
            flash('O seu cadastro foi atualizado com sucesso!', 'success')
            return redirect(url_for('update_coordinator'))
        else:
            user_info = db.child("users").child(session['user_id']).get().val() or {}
            return render_template('update_coordinator.html', user_info=user_info)
    else:
        return redirect(url_for('login'))

@app.route('/delete_coordinator')
def delete_coordinator():
    if 'user_id' in session and session['tipo_usuario'] == 'coordenador':
        db.child("users").child(session['user_id']).remove()
        return redirect(url_for('logout'))
    else:
        return redirect(url_for('login'))
    
@app.route('/idoso_registrar', methods=['GET', 'POST'])
def idoso_registrar():
    if 'user_id' in session and session['tipo_usuario'] == 'coordenador':
        if request.method == 'POST':
            # Fetch all the fields from the form
            nome_idoso = request.form.get('nome_idoso')
            data_nascimento = request.form.get('data_nascimento')
            cpf_idoso = request.form.get('cpf_idoso')
            rg_idoso = request.form.get('rg_idoso')
            cartao_sus = request.form.get('cartao_sus')
            endereco = request.form.get('endereco')
            complemento = request.form.get('complemento')
            telefone = request.form.get('telefone')
            nome_responsavel = request.form.get('nome_responsavel')
            rg_responsavel = request.form.get('rg_responsavel')
            cpf_responsavel = request.form.get('cpf_responsavel')
            telefone_responsavel = request.form.get('telefone_responsavel')

            # Add all the fields to the data dictionary
            data = {
                "nome_idoso": nome_idoso,
                "data_nascimento": data_nascimento,
                "cpf_idoso": cpf_idoso,
                "rg_idoso": rg_idoso,
                "cartao_sus": cartao_sus,
                "endereco": endereco,
                "complemento": complemento,
                "telefone": telefone,
                "nome_responsavel": nome_responsavel,
                "rg_responsavel": rg_responsavel,
                "cpf_responsavel": cpf_responsavel,
                "telefone_responsavel": telefone_responsavel
            }

            # Fetch the current counter value
            counter = db.child("counter").get().val()
            if counter is None:
                counter = 1
            else:
                counter += 1
            # Store the new counter value
            db.child("counter").set(counter)
            # Use the counter as the id_idoso
            data["id_idoso"] = counter
            db.child("idoso").child(counter).set(data)
            flash('Idoso registrado com sucesso!', 'success')
        return render_template('idoso_registrar.html')
    else:
        flash('Você não tem permissão para acessar esta página.', 'error')
        return redirect(url_for('login'))
    

@app.route('/view_idoso/<id>')
def view_idoso(id):
    if 'user_id' in session and session['tipo_usuario'] == 'coordenador':
        idoso = db.child("idoso").child(id).get().val()
        if not idoso:
            return "Idoso não encontrado", 404
        return render_template('view_idoso.html', idosos=[idoso])
    else:
        return redirect(url_for('login'))
 
@app.route('/update_idoso/<id>', methods=['GET', 'POST'])
def update_idoso(id):
    if 'user_id' in session and session['tipo_usuario'] == 'coordenador':
        if request.method == 'POST':
            # Fetch all the fields from the form
            nome_idoso = request.form.get('nome_idoso')
            data_nascimento = request.form.get('data_nascimento')
            cpf_idoso = request.form.get('cpf_idoso')
            rg_idoso = request.form.get('rg_idoso')
            cartao_sus = request.form.get('cartao_sus')
            endereco = request.form.get('endereco')
            complemento = request.form.get('complemento')
            telefone = request.form.get('telefone')
            nome_responsavel = request.form.get('nome_responsavel')
            rg_responsavel = request.form.get('rg_responsavel')
            cpf_responsavel = request.form.get('cpf_responsavel')
            telefone_responsavel = request.form.get('telefone_responsavel')

            # Add all the fields to the data dictionary
            data = {
                "nome_idoso": nome_idoso,
                "data_nascimento": data_nascimento,
                "cpf_idoso": cpf_idoso,
                "rg_idoso": rg_idoso,
                "cartao_sus": cartao_sus,
                "endereco": endereco,
                "complemento": complemento,
                "telefone": telefone,
                "nome_responsavel": nome_responsavel,
                "rg_responsavel": rg_responsavel,
                "cpf_responsavel": cpf_responsavel,
                "telefone_responsavel": telefone_responsavel
            }
            db.child("idoso").child(id).update(data)
            print(f"Updated idoso {id} with data: {data}")
            flash('Cadastro do idoso foi atualizado com sucesso!', 'success')
            return redirect(url_for('update_idoso', id=id))
        else:
            # Fetch the idoso data
            idoso_info = db.child("idoso").child(id).get().val() or {}
            print(idoso_info)
            return render_template('update_idoso.html', idoso_info=idoso_info)
    else:
        flash('Você não tem permissão para acessar esta página.', 'error')
        return redirect(url_for('login'))
    
@app.route('/delete_idoso/<id>', methods=['GET'])
def delete_idoso(id):
    if 'user_id' in session and session['tipo_usuario'] == 'coordenador':
        db.child("idoso").child(id).remove()
    return redirect(url_for('painel'))


@app.route('/register_daily_info/<int:id>', methods=['GET', 'POST'])
def register_daily_info(id):
    if request.method == 'POST':
        user_info = session.get('user_info')
        if not user_info:
            return jsonify({'message': 'User not logged in'}), 401

        data = request.form.to_dict()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        # Fetch all daily info for the specific elderly person
        all_daily_info = db.child("checklist_diario_idoso").get().val()

                # Check if there is already a record with the same date and id
        if all_daily_info is not None:
            for record_id, info in all_daily_info.items():
                if isinstance(info, dict) and info.get('data_checklist') == data['data_checklist'] and str(info.get('id_idoso')) == str(id):
                    flash('Já existe um registro do idoso com a data de hoje', 'error')
                    return redirect(url_for('register_daily_info', id=id))

        try:
            db.child("checklist_diario_idoso").push(data)
            flash('Informações diárias do idoso foi registrado com sucesso!', 'success')
            return redirect(url_for('register_daily_info', id=id))
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    else:
        idoso = db.child("idoso").child(id).get().val()
        if not idoso:
            return jsonify({'message': 'Idoso não encontrado'}), 404
        user_info = session.get('user_info')
        return render_template('register_daily_info.html', idoso=idoso, user_info=user_info, id=id)
    

@app.route('/view_diario_idoso/<int:id>', methods=['GET', 'POST'])
def view_diario_idoso(id):
    user_info = session.get('user_info')
    if not user_info:
        return jsonify({'message': 'User not logged in'}), 401

    # Fetch all daily info for the specific elderly person
    all_daily_info = db.child("checklist_diario_idoso").get().val()

    if all_daily_info is None:
        flash('Não há registro de diário do idoso(a) gravado', 'error')
        return redirect(url_for('painel'))

    # Filter the daily info for the specific elderly person
    daily_info = [info for record_id, info in all_daily_info.items() if isinstance(info, dict) and str(info.get('id_idoso')) == str(id)]
    
    idoso = db.child("idoso").child(id).get().val()
    if not idoso:
        return jsonify({'message': 'Idoso não encontrado'}), 404

    if not daily_info:
       flash('Não há registro do idoso gravado', 'error')
       return redirect(url_for('painel'))

    return render_template('view_diario_idoso.html', daily_info=daily_info, user_info=user_info, id=id, idoso=idoso)

from flask import flash

@app.route('/delete_diario_idoso/<id>/<data_checklist>', methods=['GET'])
def delete_diario_idoso(id, data_checklist):
    if 'user_id' in session and session['tipo_usuario'] == 'coordenador':
        registros = db.child("checklist_diario_idoso").get()
        if registros.each() is not None:
            for registro in registros.each():
                if 'id_idoso' in registro.val() and 'data_checklist' in registro.val():
                    if registro.val()['id_idoso'] == str(id) and registro.val()['data_checklist'] == data_checklist:
                        try:
                            db.child("checklist_diario_idoso").child(registro.key()).remove()
                            flash('Registro apagado com sucesso', 'success')
                        except Exception as e:
                            flash('Erro ao apagar o registro: ' + str(e), 'error')
    return redirect(url_for('view_diario_idoso', id=id))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('tipo_usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
