import subprocess

# Define los nombres de tus scripts y los parámetros comunes
scripts = [
    'rpl_operation_sl.py',
    'rpl_operation_sl_second_approach.py',
    'rpl_projected_routes.py',
    'rpl_multicast.py'
]

common_params = {'tx_range': 30, 'num_nodes': 10, 'num_street_lights': 2 }
num_runs = 100  # Número de veces que quieres ejecutar cada script

# Crea un diccionario para almacenar los resultados de cada script
results = {script: [] for script in scripts}

# Define una función para ejecutar un script con parámetros comunes y capturar su salida
def run_script_with_params(script, params):
    try:
        # Construye la lista de argumentos para el script
        cmd = ['python', script] + [f"--{key}={value}" for key, value in params.items()]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script} con parámetros {params}: {e}")
        print(e.output)  # Muestra el error detallado
        return None

# Ejecuta cada script el número especificado de veces
for script in scripts:
    print(f"Ejecutando {script} {num_runs} veces con parámetros {common_params}...")
    for _ in range(num_runs):
        output = run_script_with_params(script, common_params)
        if output is not None:
            results[script].append(output)

# Guarda los resultados en un archivo para su análisis posterior
with open('results.txt', 'w') as f:
    for script, outputs in results.items():
        f.write(f"Resultados para {script}:\n")
        for output in outputs:
            f.write(output + '\n')
        f.write('\n')

print("Ejecuciones completas. Resultados guardados en 'results.txt'.")

# Aquí puedes agregar el análisis de resultados si es necesario
# Por ejemplo, calcular estadísticas, hacer gráficos, etc.
