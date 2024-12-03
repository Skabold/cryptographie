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
        word1 = self.words[i]
        word2 = self.prev_words[(i)]
        word3 = self.words[(i + 2)]
        word4 = self.prev_words[(i + 2)]

        # Mélange
        mixed_word_1 = xor(word1, word2)
        mixed_word_2 = xor(word3, word4)
        mixed_word_f = xor(mixed_word_1, mixed_word_2)

        self.words.append(mixed_word_f)

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
    N = 10  # Nombre de tours de compression
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
    padded_message = pad(message)
    prev_block = IV
    new_hash = b""

    for i in range(0, len(padded_message), BS):
        block = padded_message[i:i + BS]
        prev_block = hash_block(block, prev_block)
        new_hash += prev_block

    return truncate_cmp(new_hash)

def test_hash_function():
    """
    Teste la fonction de hachage personnalisée.

    Actions :
        - Vérifie que des messages proches produisent des hashes différents (effet d'avalanche).
        - Mesure le temps moyen d'exécution du hachage sur 100 itérations.
    """
    h1 = custhash("Je suis une truite")
    h2 = custhash("Je suis une truita")
    print("Hash 1:", h1.hex())
    print("Hash 2:", h2.hex())
    assert h1 != h2, "The hashes should be different"

    # Measure execution time
    start_time = time.time()
    for _ in range(100):
        custhash("Je suis une truite")
    end_time = time.time()
    avg_time = (end_time - start_time) / 100
    print(f"Average time per block: {avg_time * 1000:.2f} ms")
