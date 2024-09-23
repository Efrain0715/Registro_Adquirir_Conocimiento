import sqlite3

# Conectar a la base de datos SQLite (si no existe, se crea)
conn = sqlite3.connect('knowledge_urgencia.db')
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS knowledge_urgencias (
                    question TEXT PRIMARY KEY,
                    answer TEXT
                )''')
conn.commit()


# Función para obtener respuesta desde la base de datos
def get_response_from_db(question):
    cursor.execute("SELECT answer FROM knowledge_urgencias WHERE question=?", (question,))
    result = cursor.fetchone()
    return result[0] if result else None


# Función para aprender una nueva respuesta
def learn_new_knowledge_db(question, answer):
    cursor.execute("INSERT OR REPLACE INTO knowledge_urgencias (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()

# Función para obtener todo el conocimiento almacenado
def list_all_knowledge():
    cursor.execute("SELECT * FROM knowledge_urgencia")
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"Pregunta: {row[0]}, Respuesta: {row[1]}")
    else:
        print("Aun no se cuenta con conocimiento")

# Interacción con el usuario
def chat():
    while True:
        user_input = input("Usuario: ")

        # Si el usuario quiere ver todo el conocimiento hasta el momento
        if user_input.lower() == "mostrar todo":
            list_all_knowledge()
            continue

        response = get_response_from_db(user_input)

        if response:
            print(f"ChatBot: {response}")
        else:
            print("No se de lo que me hablas. ¿Quieres enseñarme una nueva respuesta?")
            should_learn = input("¿Quieres enseñarme? (sí/no): ").lower()
            if should_learn == "sí" or should_learn == "si":
                new_question = input("Por favor, ingresa la pregunta que debería reconocer o palabra: ")
                new_answer = input("Por favor, dime la respuesta correcta: ")
                learn_new_knowledge_db(new_question, new_answer)
                print(f" GRACIAS. Ya tengo mas conocimiento: {new_question} -> {new_answer}")


# Cargar conocimiento inicial en la base de datos
def load_initial_knowledge():
    # Base de conocimiento inicial
    initial_knowledge = {
        "Hola": "¡Hola! ¿Cómo estás?",
        "Como estas?": "Estoy bien, gracias por preguntar.",
        "¿Cual es la urgencia medica?":""
    }

    for question, answer in initial_knowledge.items():
        learn_new_knowledge_db(question, answer)


# Cargar conocimiento inicial en la base de datos solo si no existe
def check_and_load_initial_knowledge():
    cursor.execute("SELECT count(*) FROM knowledge_urgencias")
    result = cursor.fetchone()[0]
    if result == 0:
        load_initial_knowledge()


# Verifica si es necesario cargar el conocimiento inicial
check_and_load_initial_knowledge()

# Iniciar la interacción con el usuario
chat()
