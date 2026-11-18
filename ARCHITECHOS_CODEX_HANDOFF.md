# ArchitechOS — Contexte de référence pour Codex (VS Code)

> Source : handoff projet DA + Hardware daté du 17 octobre 2026. Ce document distingue les décisions validées, l'état technique rapporté et les éléments encore ouverts. Le dépôt courant fait foi pour les détails d'implémentation.

## 1. Rôle de Codex et règles impératives

- Travailler en français, avec une collaboration progressive et concrète.
- Avancer par petits incréments : analyser, proposer, faire valider, puis seulement implémenter.
- **Ne pas coder tant que la conception de la fonctionnalité concernée n'a pas été validée explicitement.**
- **Ne pas modifier le home global**, considéré terminé et validé pour ce chantier.
- Ne pas réinventer la direction artistique, multiplier les mockups ou extrapoler les besoins métier.
- Préserver les fonctionnalités existantes ; éviter les refontes hors périmètre.
- Avant toute modification, examiner les fichiers réels du workspace et annoncer précisément les changements proposés. Ne jamais supposer que l'état du dépôt est identique à ce handoff.
- En cas d'incertitude, demander confirmation au lieu de prendre une décision produit implicite.

## 2. Projet et stack connue au 17/10/2026

- Dépôt privé : `RaccoonDevHub/ArchitechOS`.
- Framework : Django 5.2 LTS ; Python 3.14.4.
- Front-end : Node 24.6.0, npm 11.5.1, Tailwind CLI 4.3.3, daisyUI 5.7.46.
- Applications Django : `core`, `hardware`, `chronos`, `electronics`.
- Branche rapportée dans le document source : `feature/hardware-home` (**à vérifier dans Git**, elle a pu changer).
- Fichiers connus :
  - `templates/hardware/home.html`
  - `templates/hardware/partials/trieur.html`
  - `hardware/views.py`
  - `hardware/urls.py`
  - `static/css/hardware.css`
  - `static/js/htmx.min.js`
- HTMX 2.0.11 installé localement et inclus dans la page Hardware : **pas de CDN**.

### Comportements techniques déjà fonctionnels (état rapporté)

- Le trieur interne Hardware est dynamique via Django + HTMX.
- Le clic sur un volet met à jour une zone ciblée sans recharger la page complète.
- `home.html` doit inclure le partial du trieur **une seule fois**, sans conserver une ancienne copie HTML en doublon.
- Dans `hardware/urls.py`, conserver `app_name = "hardware"` et la route :

```python
path("module/<slug:module>/", views.select_module, name="select_module")
```

- Les chevrons `< >` sont indispensables. L'erreur `module/slug:module/` a déjà provoqué un `NoReverseMatch`.
- `hardware/views.py` a été modifié par l'utilisateur pour renommer les sous-modules. **Ne pas écraser ses noms actuels** : les relire directement dans le dépôt.

## 3. Architecture de navigation VALIDÉE

1. Le home global comporte trois grandes cartes : **Hardware**, **Chronos**, **Electronics**. Il est terminé et hors périmètre.
2. Chaque grand module possède sa propre page et sa propre navigation dynamique interne.
3. Dans Hardware, trois volets sont actifs : **Fiches matériel**, **Builder**, **Following**.
4. Le système de trieur / languettes doit être réutilisable ultérieurement pour Chronos et Electronics.
5. HTMX gère les remplacements ciblés côté serveur ; CSS et JavaScript peuvent gérer les animations locales.
6. Pas de rechargement intégral de page à chaque changement de volet.

**Important :** l'existence des volets Builder et Following est validée ; leur logique métier détaillée n'est pas spécifiée dans le document source. Ne pas l'inventer.

## 4. Direction artistique VALIDÉE

| Élément | Couleur | Usage |
|---|---|---|
| Fond principal | `#C8D8C2` | Sauge |
| Éléments sombres / inactifs | `#234D3C` | Vert sapin |
| Surfaces claires / panneaux | `#F1F3EA` | Ivoire |

Principes :

- Ambiance **macOS / Apple-made** : interface épurée, cohérente, discrète, pratique.
- Lisibilité, homogénéité et efficacité avant décoration.
- Éviter la surcharge, les effets 3D trop graphiques, les supports mécaniques visibles et les grosses illustrations décoratives.
- Les trois cartes du home global sont la **référence stylistique** pour les futures cartes de catégories du volet Fiches matériel.
- Ne pas réinterpréter cette DA sans demande explicite.

## 5. Fiches matériel — Concept fonctionnel VALIDÉ

Le volet **Fiches matériel** n'est **pas** une liste unique et désordonnée de composants. Il suit un parcours en deux étapes :

### Étape A — Choix d'une catégorie

- Afficher des cartes de catégories homogènes, inspirées des trois grandes cartes du home global.
- Adapter leur taille à l'espace disponible dans le module Hardware.
- Une carte représente une catégorie de composants.

### Étape B — Consultation des fiches d'une catégorie

- À gauche : un répertoire de type **Rolodex**, filtré sur la catégorie sélectionnée.
- À droite : un grand panneau affichant la fiche technique du composant sélectionné.
- La navigation doit rester lisible et pratique.

### Catégories envisagées — NON VALIDÉES définitivement

- Processeurs
- Cartes graphiques
- Cartes mères
- Mémoire vive
- Stockage
- Alimentations
- Refroidissement
- Boîtiers

**Ne pas figer cette liste ni créer les modèles, routes ou interfaces correspondants avant validation.**

## 6. Rolodex — Direction retenue et correction restante

Le principe recherché est un répertoire de fiches empilées, avec **défilement vertical en cascade et perspective subtile**.

Caractéristiques souhaitées :

- Fiches larges, lisibles, occupant la largeur de leur compartiment.
- Superposition et décalage subtils entre fiches, avec profondeur produite **uniquement par la cascade**.
- La fiche active ressort en **vert sapin** ; les autres restent claires.
- Nom court sur chaque fiche, éventuellement complété par une référence constructeur exacte.
- Commandes de défilement discrètes si utiles à l'ergonomie.
- **Aucun relief latéral, aucune structure de maintien visible, aucun gros mécanisme 3D.**

La dernière maquette était proche du résultat recherché, mais sa correction demandée n'était pas encore validée : **supprimer les côtés / supports 3D, conserver seulement l'effet de cascade et renforcer très légèrement la perspective**.

Le format final des libellés (nom, référence, ou les deux) reste à décider.

## 7. Panneau technique de droite — Direction retenue

- Conserver la structure générale appréciée dans la maquette.
- Interface sobre, dense mais claire, orientée usage technique.
- Privilégier : **références exactes, caractéristiques structurées, compatibilité, données techniques**, et éventuellement images produit utiles.
- Réduire fortement les textes éditoriaux ou marketing : outil destiné à un utilisateur technique, pas à une vitrine grand public.

Onglets **envisagés, non figés** :

- Aperçu
- Spécifications
- Prix & Disponibilité
- Liens utiles

Ne pas décider seul des champs, du schéma de données ou des sources d'information.

## 8. Statut exact et prochaine étape

### Déjà validé

- Home global et son esthétique : **ne pas toucher**.
- Architecture des grands modules et navigation interne Hardware.
- Volets Hardware : Fiches matériel, Builder, Following.
- Principe de mise à jour ciblée Django + HTMX.
- Palette et style macOS sobre.
- Parcours Fiches matériel : catégories, puis Rolodex à gauche + fiche technique à droite.
- Principe visuel du Rolodex : cascade, perspective subtile, pas de supports 3D visibles.
- Priorité aux données techniques dans le panneau de droite.

### À valider avant implémentation

- Maquette finale du Rolodex corrigé.
- Liste définitive des catégories.
- Format exact des titres et références dans les languettes.
- Structure détaillée des fiches techniques et éventuels onglets.
- Besoins métier détaillés non documentés pour Builder et Following.

### Prochaine action attendue de Codex

1. **Inspecter en lecture seule** la branche Git active, l'état des modifications locales et les fichiers concernés.
2. Comparer le dépôt au contexte ci-dessus, en signalant les écarts sans écraser le travail existant.
3. Résumer l'architecture actuelle de Hardware et les composants réutilisables.
4. Proposer uniquement la prochaine petite étape de conception : finalisation du Rolodex, sans toucher au home global ni lancer de développement prématuré.
5. **Attendre la validation explicite de l'utilisateur avant de modifier le code.**

## 9. Consigne de démarrage à Codex

> Tu travailles sur ArchitechOS dans VS Code. Considère ce document comme le contexte de référence des décisions produit et DA connues, pas comme une preuve de l'état actuel des fichiers. Commence par une inspection en lecture seule du dépôt, vérifie la branche et les modifications locales, puis présente un état des lieux concis, les éventuels écarts et la prochaine proposition de conception. Ne modifie aucun fichier sans mon accord explicite. Ne touche pas au home global validé. N'invente ni besoins métier, ni catégories définitives, ni détails d'interface non confirmés.
