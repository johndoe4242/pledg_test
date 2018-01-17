
# API de paiement à plusieurs

L'objectif est de développer en Python une API de paiement à plusieurs très basique (inspirée de [https://api-docs.pledg.co/](https://api-docs.pledg.co/), mais beaucoup plus simple ;-)) :

## Techno à utiliser :

Le micro-framework Flask, avec SQLAlchemy comme ORM (avec alembic pour gérer les migrations).


## Description fonctionnelle de l'API :

- un acheteur remplit son panier et choisit de payer par Pledg sur la page de paiement d'un e-commerçant (hors scope du projet)
- en cliquant sur le bouton &quot;Partager le paiement avec Pledg&quot;, le marchand fait un appel API avec les informations de l'achat (purchase, cf ci-dessous) :
  - Le mail de l'organisateur
  - Le montant du panier à partager
  - Le contenu du panier
- Le paiement est créé (état INITIALIZED) et l'API renvoie l'url de la page de paiement Pledg avec un identifiant dynamique
- l'acheteur renseigne les emails de ses amis (les &quot;pledgers&quot;), puis renseigne ses coordonnées de carte pour payer le montant total du panier.
- ensuite, les pledgers ont 48h pour rembourser avec un appel API de remboursement (share, cf ci-dessous)
- lorsque tout le monde a payé, le statut du paiement (purchase, cf ci-dessous) passe à SUCCESSFULL
- Si au bout de 48h, un ou plusieurs pledger n'a pas payé sa part, le paiement passe en FAILED et ne peut plus être modifié


## Détail des endpoints de l'API :

- La ressource purchase décrit un paiement à plusieurs. Elle est exposée à l'extérieur. Le paiement à plusieurs a comme paramètres d'entrée :
  - Le mail de l'organisateur
  - Le montant du panier à partager

## Attributs d'un purchase retournés par GET /purchase/{id} :

-
  - L'URL de la page de paiement dynamique
  - Les emails des pledgers
  - L'état du purchase (INITIALIZED, SUCCESSFULL,ou FAILED)
- La ressource share décrit un paiement par l'un des membres du groupe, leader ou pledger. Elle n'est pas exposée à l'extérieur.

## Attributs d'un share :

-
  - L'email du membre du groupe
  - Le montant à payer
  - L'état de la share selon que le paiement réussit ou non (INITIALIZED, SUCCESSFULL,ou FAILED).

