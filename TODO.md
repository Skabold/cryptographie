# Todo List

1. Remplacer le JSON par des bytes pour toutes les données.
2. Créer un programme principal (main) qui :
   - Génère deux paires de clés RSA (RSA1 et RSA2).
   - Génère une clé PKDF.
   - Envoie la clé PKDF de RSA1 à RSA2 sous forme de message.
   - Utilise ensuite la clé PKDF pour générer des clés AES pour chaque paire RSA.
   - Permet aux deux parties de communiquer en utilisant AES pour chiffrer et déchiffrer les messages.
