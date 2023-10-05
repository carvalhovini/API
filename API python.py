from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medconnect.db'
db = SQLAlchemy(app)

class Medico(db.Model):
    MedicoID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(255), nullable=False)
    CRM = db.Column(db.String(20), unique=True, nullable=False)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    Senha = db.Column(db.String(255), nullable=False)
    Especialidade = db.Column(db.String(255))
    Telefone = db.Column(db.String(20))
    Endereco = db.Column(db.String(255))
    CPF = db.Column(db.String(14), unique=True)
    RG = db.Column(db.String(20), unique=True)

    def serialize(self):
        return {
            'MedicoID': self.MedicoID,
            'Nome': self.Nome,
            'CRM': self.CRM,
            'Email': self.Email,
            'Senha': self.Senha,
            'Especialidade': self.Especialidade,
            'Telefone': self.Telefone,
            'Endereco': self.Endereco,
            'CPF': self.CPF,
            'RG': self.RG
        }

class Hospital(db.Model):
    HospitalID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(255), nullable=False)
    Endereco = db.Column(db.String(255))
    Telefone = db.Column(db.String(20))
    Email = db.Column(db.String(255), unique=True, nullable=False)
    Senha = db.Column(db.String(255), nullable=False)
    CNPJ = db.Column(db.String(18), unique=True)

    def serialize(self):
        return {
            'HospitalID': self.HospitalID,
            'Nome': self.Nome,
            'Endereco': self.Endereco,
            'Telefone': self.Telefone,
            'Email': self.Email,
            'Senha': self.Senha,
            'CNPJ': self.CNPJ
        }

class Paciente(db.Model):
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    Senha = db.Column(db.String(255), nullable=False)
    Sexo = db.Column(db.Enum('Masculino', 'Feminino', 'Outro'))
    Telefone = db.Column(db.String(20))
    Endereco = db.Column(db.String(255))
    CPF = db.Column(db.String(14), unique=True)
    RG = db.Column(db.String(20), unique=True)

    def serialize(self):
        return {
            'UserID': self.UserID,
            'Nome': self.Nome,
            'Email': self.Email,
            'Senha': self.Senha,
            'Sexo': self.Sexo,
            'Telefone': self.Telefone,
            'Endereco': self.Endereco,
            'CPF': self.CPF,
            'RG': self.RG
        }

@app.route('/medicos', methods=['GET', 'POST'])
def medicos():
    if request.method == 'GET':
        medicos = Medico.query.all()
        return jsonify([medico.serialize() for medico in medicos])
    elif request.method == 'POST':
        data = request.json
        novo_medico = Medico(**data)
        db.session.add(novo_medico)
        db.session.commit()
        return jsonify({"message": "Médico cadastrado com sucesso!"})

@app.route('/medicos/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def medico(id):
    medico = Medico.query.get(id)
    if not medico:
        return jsonify({"message": "Médico não encontrado"}), 404
    if request.method == 'GET':
        return jsonify(medico.serialize())
    elif request.method == 'PUT':
        data = request.json
        for key, value in data.items():
            setattr(medico, key, value)
        db.session.commit()
        return jsonify({"message": "Médico atualizado com sucesso!"})
    elif request.method == 'DELETE':
        db.session.delete(medico)
        db.session.commit()
        return jsonify({"message": "Médico excluído com sucesso!"})

@app.route('/hospitais', methods=['GET', 'POST'])
def hospitais():
    if request.method == 'GET':
        hospitais = Hospital.query.all()
        return jsonify([hospital.serialize() for hospital in hospitais])
    elif request.method == 'POST':
        data = request.json
        novo_hospital = Hospital(**data)
        db.session.add(novo_hospital)
        db.session.commit()
        return jsonify({"message": "Hospital cadastrado com sucesso!"})

@app.route('/hospitais/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def hospital(id):
    hospital = Hospital.query.get(id)
    if not hospital:
        return jsonify({"message": "Hospital não encontrado"}), 404
    if request.method == 'GET':
        return jsonify(hospital.serialize())
    elif request.method == 'PUT':
        data = request.json
        for key, value in data.items():
            setattr(hospital, key, value)
        db.session.commit()
        return jsonify({"message": "Hospital atualizado com sucesso!"})
    elif request.method == 'DELETE':
        db.session.delete(hospital)
        db.session.commit()
        return jsonify({"message": "Hospital excluído com sucesso!"})


@app.route('/pacientes', methods=['GET', 'POST'])
def pacientes():
    if request.method == 'GET':
        pacientes = Paciente.query.all()
        return jsonify([paciente.serialize() for paciente in pacientes])
    elif request.method == 'POST':
        data = request.json
        novo_paciente = Paciente(**data)
        db.session.add(novo_paciente)
        db.session

        return jsonify({"message": "Paciente cadastrado com sucesso!"})

@app.route('/pacientes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def paciente(id):
    paciente = db.session.query(Paciente).get(id)
    if not paciente:
        return jsonify({"message": "Paciente não encontrado"}), 404
    if request.method == 'GET':
        return jsonify(paciente.serialize())
    elif request.method == 'PUT':
        data = request.json
        for key, value in data.items():
            setattr(paciente, key, value)
        db.session.commit()
        return jsonify({"message": "Paciente atualizado com sucesso!"})
    elif request.method == 'DELETE':
        db.session.delete(paciente)
        db.session.commit()
        return jsonify({"message": "Paciente excluído com sucesso!"})
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
