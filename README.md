# cryptographie

hashPKDF :

- hash.py : les fonctions en TODO
- hash_utils : les fonctions qu'on touche pas
- hash_main : le main pour tester les trucs de hashPKFD
  - `N = 1000 #DEPEND DU PC ON VISE Temps moyen d'exécution pour 100.00 essais : 19.78 ms`

RSA :

- rsa_main : c'est le main pour tester les trucs rsa
- rsa_utils : les maths qui était dans rsa.py de base
- rsa : la classe rsa (receive / hash / sign / verify / ...)
- send : la méthode pour send des messages
- template_usage : des exemples d'utilisation de RSA que j'ai pas delete au cas ou je suis trop con dans 2 mois

AES :

- aes_main : c'est le main pour tester les trucs aes
- aes_utils : les maths qui était dans aes.py de base
- aes : la classe aes (receive / hash )
- send : la méthode send

Update python path :

- export PYTHONPATH=lepath/le dossier au dessus des folders aes / rsa / hashPKDF
