from werkzeug.security import generate_password_hash

# Configura qui le credenziali che desideri
username_admin = "admin"
password_in_chiaro = "pass123"
nome_admin = "Amministratore"

# Genera l'hash sicuro compatibile con Flask
password_hashata = generate_password_hash(password_in_chiaro)

# Crea e stampa la query SQL finale
query_sql = f"""INSERT INTO admin (username, password, nome) 
VALUES ('{username_admin}', '{password_hashata}', '{nome_admin}');"""

print("--- COPIA LA QUERY SQL SOTTOSTANTE ---")
print(query_sql)
print("---------------------------------------")