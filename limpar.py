import sqlite3

# Conecte-se ao banco de dados SQLite
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# Execute a instrução SQL para excluir todas as linhas da tabela
#c.execute('DELETE FROM fabricaNeeds_entradasestoque')
c.execute(input("Qual comando SQL? "))

# Confirme as alterações
conn.commit()

# Feche a conexão com o banco de dados
conn.close()