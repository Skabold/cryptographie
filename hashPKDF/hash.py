"""
Ce fichier contient les fonctions principales pour la gestion du hachage personnalisé basé sur des blocs, ainsi que leur compression.  
Les fonctionnalités incluent :  
- Padding des messages.
- Compression des blocs de données.
- Une fonction de hachage principale intégrant ces mécanismes.
- Des tests basiques pour valider le bon fonctionnement du système.

Classes et fonctions principales :
- `Compression` : Gère la compression d'un bloc de données en fonction du bloc précédent.
- `hash_block` : Applique la compression pour obtenir le hachage d'un bloc.
- `truncate_cmp` : Tronque le résultat final du hachage.
- `custhash` : Fonction principale qui prend un message en entrée et retourne son hash.
- `test_hash_function` : Tests unitaires et mesure de performance.

Paramètres globaux :
- `BLOCK_DIV` : Nombre de mots dans un bloc divisé.
- `BS` : Taille en bytes d'un bloc.
- `IV` : Valeur initiale (Initial Vector) pour le hachage.
"""

from hashPKDF.hash_utils import *


class Compression:
    """
    Gère la compression des blocs de données en fonction de leur état précédent.
    Utilise un mélange agressif de transformations linéaires et non linéaires
    pour maximiser l'effet d'avalanche.
    """

    def __init__(self, block, prev_block):
        """
        Initialise les mots du bloc actuel et du bloc précédent.

        :param block: (bytes) Bloc de données actuel.
        :param prev_block: (bytes) Bloc de données précédent.
        :raises AssertionError: Si le nombre de mots dans les blocs n'est pas égal à BLOCK_DIV.
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

        :param i: (int) Indice du mot sur lequel effectuer la compression.
        """
        word1 = self.words[-1]
        word2 = self.prev_words[(i - 1) % BLOCK_DIV]
        word3 = self.words[-2]
        word4 = self.prev_words[(i - 4) % BLOCK_DIV]

        # Transformations non linéaires avancées
        mixed_word = sub_word(word1)
        mixed_word = xor(mixed_word, rot_left(word2, (i * 17) % 64))
        mixed_word = bitand(mixed_word, rot_right(word3, (i * 23) % 32))
        mixed_word = xor(mixed_word, word4)

        cross_mixed = xor(rot_left(word2, i * 5), rot_right(word4, i * 7))
        mixed_word = xor(mixed_word, cross_mixed)
        mixed_word = sub_word(mixed_word)

        mixed_word = xor(mixed_word, rot_right(word1, (i * 11) % 32))
        mixed_word = bitand(mixed_word, rot_left(word3, (i * 19) % 64))
        mixed_word = xor(mixed_word, rot_left(word4, i % 16))

        self.words.append(mixed_word)

    def get_result(self):
        """
        Récupère le résultat final de la compression.

        :return: (bytes) Le bloc compressé sous forme de bytes.
        """
        result = words_to_block(self.words[-BLOCK_DIV:])
        return result


def hash_block(block, prev):
    """
    Hache un bloc en utilisant le bloc précédent.

    :param block: (bytes) Bloc de données actuel.
    :param prev: (bytes) Bloc de données précédent.
    :return: (bytes) Résultat du hachage pour le bloc.
    :raises AssertionError: Si les blocs ne respectent pas la longueur BS.
    """
    assert len(block) == BS
    assert len(prev) == BS

    cmp = Compression(block, prev)
    N = 1000 #DEPEND DU PC ON VISE Temps moyen d'exécution pour 100.00 essais : 19.78 ms
    for i in range(N):
        cmp.compress_round(i)

    result = cmp.get_result()
    return result


def truncate_cmp(hash):
    """
    Tronque le hash de 512 bits à 256 bits en combinant les deux moitiés via XOR.

    :param hash: (bytes) Hash calculé (512 bits).
    :return: (bytes) Hash tronqué (256 bits).
    """
    half_size = len(hash) // 2
    first_half = hash[:half_size]
    second_half = hash[half_size:]
    return xor(first_half, second_half)


def custhash(message):
    """
    Fonction principale de hachage pour un message.

    :param message: (str) Message à hacher.
    :return: (bytes) Hash final du message.
    """
    message = message.encode('utf-8')
    padded_msg = pad(message)
    prev_block = IV

    for i in range(0, len(padded_msg), BS):
        block = padded_msg[i:i + BS]

        # Mélange dynamique (magique, je capte pas)
        dynamic_mix = xor(prev_block, i.to_bytes(BS, 'big', signed=False))
        dynamic_mix = xor(dynamic_mix, block)
        prev_block = dynamic_mix

        prev_block = hash_block(block, prev_block)

    final_hash = truncate_cmp(prev_block)
    return final_hash


def pkdf(password, salt, iterations):
    """
    Génère une clé dérivée à partir d'un mot de passe et d'un salt.

    :param password: (str) Mot de passe utilisé pour générer la clé.
    :param salt: (bytes) Salt unique pour cette opération.
    :param iterations: (int) Nombre d'itérations pour ralentir le calcul.
    :param key_length: (int) Longueur souhaitée de la clé dérivée en octets (par défaut : 16).
    :return: (bytes) Clé dérivée.
    """
    assert isinstance(password, str), "Le mot de passe doit être une chaîne de caractères."
    assert isinstance(salt, bytes), "Le salt doit être un objet bytes."
    
    # Étape 1 : Convertir le mot de passe en bytes
    password_bytes = password.encode('utf-8')
    derived_key = b''
    
    # Étape 3 : Effectuer les itérations
    block = password_bytes + salt
    for i in range(iterations):
        block = custhash(block.decode('latin-1'))  
    
    # Étape 4 : 16 octetc = 128 bits
    derived_key = block[:16]
    
    return derived_key




