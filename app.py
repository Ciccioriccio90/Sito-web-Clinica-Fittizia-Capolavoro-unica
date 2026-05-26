from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'
app.config['SECRET_KEY'] = 'chiave_molto_segreta'

def db_connection():
    connection = pymysql.connect(
        host="127.0.0.1",
        user="user",
        database="dbtest",

        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/pazienti")
def pazienti():
   
    if 'username' not in session or session.get('ruolo') not in ['admin', 'dottore']:
        flash("Accesso riservato al personale autorizzato.")
        return redirect(url_for('home'))

    conn = db_connection()
    with conn.cursor() as cur:
        if session.get('ruolo') == 'admin':
            cur.execute("SELECT * FROM pazienti")
        else:
            sql = """
                SELECT DISTINCT p.* FROM pazienti p
                JOIN appuntamenti a ON p.cf = a.codice_fiscale
                WHERE a.codice_dottore = %s
            """
            cur.execute(sql, (session.get('id'),))
            
        dati = cur.fetchall()
    conn.close()
    
    return render_template("pazienti.html", pazienti=dati)

@app.route("/dottori")
def dottori():
    conn = db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM dottori")
        dati = cur.fetchall()
    conn.close()
    return render_template("dottori.html", dottori=dati)

@app.route("/appuntamenti/<codice>/<tipo>")
@app.route("/appuntamenti")
def appuntamenti(codice=None, tipo=None):
    if 'username' not in session:
        flash("Effettua il login per vedere gli appuntamenti.")
        return redirect(url_for('login'))

    ruolo_loggato = session.get('ruolo')
    id_loggato = session.get('id')
    
    conn = db_connection()
    visite = []
    
    with conn.cursor() as cur:
        
        if codice and tipo:
            if ruolo_loggato == "paziente":
                sql = "SELECT codice_dottore, codice_fiscale, data, ora FROM appuntamenti WHERE codice_fiscale = %s AND codice_dottore = %s"
                cur.execute(sql, (id_loggato, codice))
                visite = cur.fetchall()
            
            elif ruolo_loggato == "dottore":
                if tipo == "paziente":
                    sql = "SELECT codice_dottore, codice_fiscale, data, ora FROM appuntamenti WHERE codice_dottore = %s AND codice_fiscale = %s"
                    cur.execute(sql, (id_loggato, codice))
                    visite = cur.fetchall()
                    
            elif ruolo_loggato == "admin":
                if tipo == "dottore":
                    sql = "SELECT codice_dottore, codice_fiscale, data, ora FROM appuntamenti WHERE codice_dottore = %s"
                    cur.execute(sql, (codice))
                elif tipo == "paziente":
                    sql = "SELECT codice_dottore, codice_fiscale, data, ora FROM appuntamenti WHERE codice_fiscale = %s"
                    cur.execute(sql, (codice))
                visite = cur.fetchall()
        else:
            if ruolo_loggato == "admin":
                sql = "SELECT codice_dottore, codice_fiscale, data, ora FROM appuntamenti"
                cur.execute(sql)
                visite = cur.fetchall()
                
            elif ruolo_loggato == "dottore":
                sql = "SELECT codice_dottore, codice_fiscale, data, ora FROM appuntamenti WHERE codice_dottore = %s"
                cur.execute(sql, (id_loggato))
                visite = cur.fetchall()
                
            elif ruolo_loggato == "paziente":
                sql = "SELECT codice_dottore, codice_fiscale, data, ora FROM appuntamenti WHERE codice_fiscale = %s"
                cur.execute(sql, (id_loggato))
                visite = cur.fetchall()
                
    conn.close()
    return render_template("appuntamenti.html", visite=visite)

@app.route('/registrazione', methods=['GET', 'POST'])
def registrazione():
    if request.method == 'POST':
        d = request.form
        ruolo = d.get('ruolo')
        username = d.get('username') 
        password_hashata = generate_password_hash(d.get('password'))
        
        conn = db_connection()
        cursor = conn.cursor()

        if ruolo == 'dottore':
            cursor.execute("SELECT username FROM dottori WHERE username = %s", (username))
        elif ruolo =='paziente':
            cursor.execute("SELECT username FROM pazienti WHERE username = %s", (username))
        
        if cursor.fetchone():
            flash("Errore: Lo username è già esistente per questo ruolo!")
            cursor.close()
            conn.close()
            return redirect(url_for('registrazione'))

        if ruolo == 'dottore':
            file = request.files.get('foto')
            fname = secure_filename(file.filename) if file else "default.jpg"
            if file: file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            
            sql = "INSERT INTO dottori (codice, nome, specializzazione, img, username, password) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (d.get('codice'), d.get('nome'), d.get('specializzazione'), fname, username, password_hashata)
        else:
            sql = "INSERT INTO pazienti (cf, nome, cognome, nascita, username, password) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (d.get('cf'), d.get('nome'), d.get('cognome'), d.get('nascita'), username, password_hashata)

        try:
            cursor.execute(sql, val)
            conn.commit()
            flash("Registrazione completata!")
        except Exception as e:
            print(f"Errore: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('login'))
    
    return render_template('registrazione.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        ruolo = request.form.get('ruolo') 
        
        conn = db_connection()
        cursor = conn.cursor()

        if ruolo == 'dottore':
            cursor.execute("SELECT * FROM dottori WHERE username = %s", (username))
        elif ruolo == 'paziente':
            cursor.execute("SELECT * FROM pazienti WHERE username = %s", (username))
        else:
            cursor.execute("SELECT * FROM admin WHERE username = %s", (username))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()

    
        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            session['ruolo'] = ruolo
            session['nome'] = user['nome']
            

            if ruolo == 'dottore':
                session['id'] = user['codice']
            elif ruolo == 'paziente':
                session['id'] = user['cf']
            elif ruolo == 'admin':
                session['id'] = user['id'] 
            
            flash(f"Benvenuto {user['nome']}!")
            return redirect(url_for('home'))
        else:
            flash("Username, password o ruolo errati!")
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logout effettuato.")
    return redirect(url_for('home'))




@app.route("/creappuntamenti", methods=['GET', 'POST'])
def creappuntamenti():
    if 'username' not in session or session.get('ruolo') != 'dottore':
        flash("Accesso negato! Solo i medici possono inserire nuovi appuntamenti.")
        return redirect(url_for('home'))
    if request.method == 'POST':
        codice_fiscale = request.form.get('codice_fiscale')
        data_visita = request.form.get('data')
        ora_visita = request.form.get('ora')
        id_medico = session.get('id') 

        conn = db_connection()
        cursor = conn.cursor()

        try:
            sql = "INSERT INTO appuntamenti (codice_dottore, codice_fiscale, data, ora) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (id_medico, codice_fiscale, data_visita, ora_visita))
            conn.commit()
            
            flash("Appuntamento fissato con successo!")
            return redirect(url_for('appuntamenti')) 
        except Exception as e:
            print(f"Errore durante l'inserimento: {e}")
            conn.rollback()
            flash("Si è verificato un errore durante il salvataggio dell'appuntamento.")
            return redirect(url_for('creappuntamenti'))
            
        finally:
            cursor.close()
            conn.close()

    conn = db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT cf, nome, cognome FROM pazienti ORDER BY cognome, nome")
        elenco_pazienti = cursor.fetchall()
    except Exception as e:
        print(f"Errore caricamento pazienti: {e}")
        elenco_pazienti = []
    finally:
        cursor.close()
        conn.close()

    return render_template('creaappuntamenti.html', pazienti=elenco_pazienti)


if __name__ == "__main__":
    app.run(debug=True)

