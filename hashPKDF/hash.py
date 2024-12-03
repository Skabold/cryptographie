from filecmp import cmp
from hash_utils import *
import time

"""
Fichier contenant les fonctions principales pour le hachage à partir de blocs et la compression.
Les fonctions incluent des opérations de padding, de compression, et des tests unitaires.
(C'était les fonctions de base en TODO)
"""

# State
class Compression:
    """
    Classe représentant l'état de compression pour un bloc et son bloc précédent.

    Attributs :
        - words (list): Liste des mots extraits du bloc actuel.
        - prev_words (list): Liste des mots extraits du bloc précédent.
    """

    def __init__(self, block, prev_block):
        """
        Initialise les mots du bloc actuel et du bloc précédent.

        Paramètres :
            - block (bytes) : Bloc de données actuel.
            - prev_block (bytes) : Bloc de données précédent.

        Exceptions :
            - AssertionError : Si le nombre de mots dans les blocs n'est pas égal à BLOCK_DIV.
        """
        words = block_to_words(block)
        prev_words = block_to_words(prev_block)
        assert len(words) == BLOCK_DIV
        assert len(prev_words) == BLOCK_DIV
        self.words = words
        self.prev_words = prev_words

    def compress_round(self, i):
        """
        Effectue un tour de compression en mélangeant les mots actuels et précédents.

        Paramètres :
            - i (int) : Indice du mot sur lequel effectuer la compression.

        Actions :
            - Mélange les mots actuels et précédents pour produire un nouveau mot.
            - Ajoute le nouveau mot à la liste des mots actuels.
        """
        # Sélection des mots
        word1 = self.words[i % len(self.words)]
        word2 = self.prev_words[i % len(self.prev_words)]
        word3 = self.words[(i - 2) % len(self.words)]
        word4 = self.prev_words[(i - 2) % len(self.prev_words)]

        mixed_word = sub_word(word1)
        mixed_word = xor(mixed_word, rot_left(word2, i % 8))
        mixed_word = bitand(mixed_word, rot_right(word3, (i + 3) % 8))
        mixed_word = xor(mixed_word, word4)
        cross_mixed = xor(rot_left(word2, 5), rot_right(word4, 3))
        mixed_word = xor(mixed_word, cross_mixed)

        self.words.append(mixed_word)

    def get_result(self):
        """
        Récupère le résultat final de la compression.

        Retourne :
            - bytes : Le bloc compressé sous forme de bytes, à partir des derniers mots.
        """
        return words_to_block(self.words[-BLOCK_DIV:])

def hash_block(block, prev):
    """
    Hache un bloc en utilisant le bloc précédent.

    Paramètres :
        - block (bytes) : Bloc de données actuel.
        - prev (bytes) : Bloc de données précédent.

    Retourne :
        - bytes : Le résultat du hachage pour le bloc.

    Exceptions :
        - AssertionError : Si les blocs ne sont pas de longueur BS.
    """
    assert len(block) == BS
    assert len(prev) == BS

    cmp = Compression(block, prev)
    N = 100 
    for i in range(N):
        cmp.compress_round(i)

    return cmp.get_result()

def truncate_cmp(hash):
    """
    Tronque le hash final en le combinant avec une valeur IV initiale.

    Paramètres :
        - hash (bytes) : Hash calculé.

    Retourne :
        - bytes : Le hash tronqué.
    """
    return xor(hash, IV)

def custhash(message):
    """
    Fonction principale de hachage pour un message.

    Paramètres :
        - message (str) : Message à hacher.

    Retourne :
        - bytes : Le hash final du message.

    Actions :
        - Applique un padding au message.
        - Itère sur les blocs pour effectuer le hachage.
        - Tronque le résultat final.
    """
    message = message.encode('utf-8')
    padded_msg = pad(message)
    prev_block = IV
    
    # Process each block in the padded message
    for i in range(0, len(padded_msg), BS):
        block = padded_msg[i:i + BS]
        prev_block = hash_block(block, prev_block)

    return truncate_cmp(prev_block)

def test_hash_function():
    """
    Teste la fonction de hachage personnalisée.

    Actions :
        - Vérifie que des messages proches produisent des hashes différents (effet d'avalanche).
        - Mesure le temps moyen d'exécution du hachage sur 100 itérations.
    """
    h1 = custhash("J'emmerde les truites")
    h2 = custhash("J'emmerde les truites!")
    print("Hash 1:", h1.hex())
    print("Hash 2:", h2.hex())
    assert h1 != h2, "The hashes should be different"

    # Measure execution time
    start_time = time.time()
    for _ in range(100):
       custhash("J'emmerde les truites :D")
    end_time = time.time()
    avg_time = (end_time - start_time) / 100
    print(f"Average time per block: {avg_time * 1000:.2f} ms")
