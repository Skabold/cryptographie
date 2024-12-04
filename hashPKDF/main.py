import os
import time
from hash import custhash, pkdf

def test_hash_function():
    """
    Teste la fonction de hachage personnalisée.

    - Vérifie que des messages similaires produisent des hashes différents (effet d'avalanche).
    - Mesure le temps moyen d'exécution pour 100 itérations.
    """
    print()
    print("Premiers 2 identiques, 3e différent")
    print(custhash("test"))
    print(custhash("test"))
    print(custhash("tesy"))
    print()


def test_pkdf():
    """
    Teste la fonction PBKDF avec différents paramètres pour atteindre 500 ms par bloc.
    """
    password = "mon_super_mot_de_passe"
    salt = os.urandom(16)  
    key_length = 16  # 128 bits
    iterations = 320 # je connais déjà le résultat (~350ms / 390ms) pour moi
    
    # Mesurer le temps de calcul
    start_time = time.time()
    derived_key = pkdf(password, salt, iterations, key_length)
    end_time = time.time()
    
    # Afficher les résultats
    elapsed_time = (end_time - start_time) * 1000 
    print(f"Temps de calcul : {elapsed_time:.2f} ms")
    
    # Ajuster le nombre d'itérations
    while elapsed_time < 500:
        print(f"Nouvel essai avec {iterations} itérations : {elapsed_time:.2f} ms")
        iterations += 10
        start_time = time.time()
        derived_key = pkdf(password, salt, iterations, key_length)
        print(f"Clé dérivée : {derived_key.hex()}")
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000 
        

# Exécuter le test
test_hash_function()
print()
print()
test_pkdf()