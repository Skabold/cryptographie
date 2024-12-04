# broken

# import os
# import time
# from hash import custhash, pkdf

# def test_hash_function():
#     """
#     Teste la fonction de hachage personnalisée.

#     - Vérifie que des messages similaires produisent des hashes différents (effet d'avalanche).
#     - Mesure le temps moyen d'exécution pour 100 itérations.
#     """
#     print()
#     print("Premiers 2 identiques, 3e différent")
#     print(custhash("test"))
#     print(custhash("test"))
#     print(custhash("tesy"))
#     print()


# def test_pkdf():
#     """
#     Teste la fonction PBKDF avec différents paramètres pour atteindre 500 ms par bloc.
#     """
#     password = "mon_super_mot_de_passemon_super_mot_de_passe"
#     salt = os.urandom(16)  
#     iterations = 5 # je connais déjà le résultat (90/100) pour moi
    
#     # Mesurer le temps de calcul
#     start_time = time.time()
#     derived_key = pkdf(password, salt, iterations)
#     end_time = time.time()
#     elapsed_time = (end_time - start_time) * 1000 
    
#     # Ajuster le nombre d'itérations
#     while elapsed_time < 500:
#         iterations += 5
#         start_time = time.time()
#         derived_key = pkdf(password, salt, iterations)
#         end_time = time.time()
#         elapsed_time = (end_time - start_time) * 1000 
        
#     print(f"Nouvel essai avec {iterations} itérations : {elapsed_time:.2f} ms")
#     print(f"Clé dérivée : {derived_key.hex()}")

    
        
        

# def test_pkdf_average_time():
#     """
#     Teste la fonction PBKDF sur un message "test" avec 1 itération, 10 fois.
#     Calcule la moyenne du temps d'exécution pour ces 10 essais.
#     """
#     password = "test" 
#     salt = os.urandom(16) 
#     iterations = 1 
#     total_time = 0 
#     n = 100
#     for i in range(n):
#         start_time = time.time()
#         derived_key = pkdf(password, salt, iterations)
#         end_time = time.time()

#         elapsed_time = (end_time - start_time) * 1000  
#         total_time += elapsed_time
    
#     # Calculer la moyenne
#     average_time = total_time / n
#     print(f"\nTemps moyen d'exécution pour {n:.2f} essais : {average_time:.2f} ms")

# # Exécuter le test
# test_hash_function()
# print()
# print()
# test_pkdf()
# print()
# print()
# test_pkdf_average_time()