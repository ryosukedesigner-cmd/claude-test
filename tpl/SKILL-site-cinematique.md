---
name: site-vitrine-cinematique
description: Concevoir et produire des sites vitrines « effet waouh » (scènes en récit, images fortes avec profondeur, animations au défilement, vidéo d'ouverture) pour un métier ou une PME, mobile d'abord, à coût nul, puis les industrialiser en modèles.
---

# Site vitrine cinématique

À charger avant de créer ou refondre une page vitrine, un aperçu commercial ou une page d'accueil qui doit déclencher l'envie d'acheter. Réutilisable pour tout projet (artisans, commerces, SaaS locaux).

## 1. Pourquoi une page ne vend pas
- Le visiteur décide en 3 à 8 secondes, presque toujours sur téléphone. Une page propre mais faite de cartes blanches et d'icônes ressemble à toutes les autres : il la parcourt en 5 à 10 s et repart.
- Ce qui arrête le pouce : une image plein écran qui a de la profondeur (premier plan, plan moyen, lointain, lumière rasante), du mouvement lent, un titre court et fort, puis une histoire qui se dévoile au défilement.
- Pour un métier du bâtiment, ce qui fait appeler : la preuve visuelle (avant/après), le problème reconnu (la fuite, la fissure), un geste de métier précis, la zone, la note réelle, un bouton d'appel toujours visible. Les photos de banque d'images détruisent la confiance ; une image générée doit être parlante, sans visage identifiable, sans texte, et ne jamais être présentée comme « nos réalisations ».

## 2. Structure en scènes (mobile d'abord)
1. **Ouverture** (100svh) : vidéo muette en boucle ou image avec zoom lent, voile dégradé, accroche en 2 lignes (un mot en italique d'empattement pour la touche éditoriale), sous-titre, appel + devis, note Google réelle. Au défilement : l'image grossit et descend, le texte monte et s'efface (profondeur).
2. **Bandeau défilant** des engagements (garantie, devis gratuit, réponse rapide, zone).
3. **Le problème** (section épinglée ~260svh) : image sombre plein écran, 3 phrases qui apparaissent une à une (flou → net), puis la phrase de bascule en italique, barre de progression.
4. **Le geste** : gros plan des mains au travail, révélation par masque qui s'ouvre + parallaxe interne, à côté des 3 engagements.
5. **Avant / après** (section épinglée) : les deux images superposées, l'« après » se dévoile de gauche à droite au défilement, poignée glissable au doigt, légende « illustration ».
6. **Services** : cartes à numéros en contour, carrousel horizontal à aimantation sur mobile, grille sur ordinateur.
7. **Méthode** : frise verticale dont le trait se dessine au défilement.
8. **Zone** : vue de ville au crépuscule en parallaxe, appel « Vérifier ma disponibilité ».
9. **FAQ**, puis **appel final** sur l'image d'ouverture assombrie.

Règles : un seul appel principal répété (téléphone), en-tête en verre sombre, textes français avec espaces insécables avant ? ! : ;, aucune affirmation inventée (pas d'années d'expérience ni de nombre de chantiers non fournis).

## 3. Moteur d'animation (sans bibliothèque)
- Un script de 2 Ko : chaque section `data-cx="out|pin|in"` reçoit une variable CSS `--p` (0 à 1) calculée au défilement dans un `requestAnimationFrame` ; tout l'effet est en CSS (`transform`, `opacity`, `clip-path`, `filter`) à partir de `--p`. Fonctionne partout (y compris anciens iOS), contrairement à `animation-timeline` encore absent de Firefox.
- Valeur par défaut `--p:1` : sans JavaScript, tout est visible.
- Apparitions par IntersectionObserver (classe `.in`), décalages via `--d`.
- `prefers-reduced-motion` : sections épinglées dépliées, aucune animation.
- Ne jamais animer `top/left/width` ; ne pas épingler plus de 2 sections ; tester à 390 × 844 avec écran tactile.
- Implémentation de référence : `tpl/build_cine.py` du dépôt média (CSS + JS + structure), à copier et adapter.

## 4. Banque d'images par métier (0 €)
- **Outil par défaut : Google Flow dans Chrome** (`https://flow.google.com`), modèle d'image Nano Banana, « 0 crédit ». Les modèles payants (Higgsfield, etc.) seulement avec accord explicite de dépense.
- Par métier : ouverture 9:16 + 16:9 (même prompt), problème 9:16, geste 3:4, résultat 3:4, avant 3:4 (édition du « résultat » ajouté au prompt par « + » puis « Ajouter au prompt », consigne « Edit this exact photograph, keeping the identical … camera angle, framing … »). Une vue de ville commune à tous.
- Gabarit de prompt : sujet + lumière (golden hour, blue hour, rayon de soleil) + profondeur (« deep perspective », « shallow depth of field », « soft bokeh ») + « Shot on 35mm/85mm, editorial photography, photorealistic » + « No text, no logos, no brand names, face not visible ».
- Flow accepte environ 4 générations en parallèle ; au-delà « Échec : trop de demandes » → bouton Réessayer.
- 4 variantes par prise : choisir sur planche-contact ; pour l'avant/après, garder l'« avant » dont les contours sont le plus proches de l'« après » (différence de contours mesurée), puis vérifier sur une vignette coupée en deux.
- **Récupération sans téléchargement** : depuis l'onglet Flow, en JavaScript, `fetch(img.src)` puis POST vers un stockage public (ex. bucket Supabase avec une politique d'insertion temporaire, limitée à un dossier et qui expire d'elle-même), puis récupération dans l'espace de travail.
- Optimisation : WebP qualité ~74, 900 px (portrait) ou 1 800 px (paysage) ; viser < 150 Ko, image d'ouverture < 90 Ko (LCP).

## 5. Vidéo d'ouverture
- 5 s, mouvement lent (poussée de caméra, poussière dans la lumière, geste simple), sans coupe, depuis l'image d'ouverture 9:16.
- Gratuit : IA locale (LTX-Video, ComfyUI) si disponible ; sinon pas de vidéo, l'image a un zoom lent infini (Ken Burns).
- Encodage : `scale=540`, 24 i/s, boucle aller-retour (`reverse` + `concat`), sans son, H.264 `-crf 29 -preset veryfast -movflags +faststart`, < 700 Ko.
- Chargée seulement sur mobile, après `load`, jamais si `saveData` ou 2G ; affichée en fondu au premier `playing` ; mise en pause hors écran.

## 6. Hébergement des médias (0 €)
- Dépôt GitHub public + jsDelivr, URL figée sur le commit : `https://cdn.jsdelivr.net/gh/<compte>/<dépôt>@<sha>/m/<métier>/<fichier>`. Ne jamais renommer un fichier publié.
- Les modèles HTML peuvent aussi y être publiés : la base les télécharge elle-même (`net.http_get`) et vérifie le md5 avant insertion, ce qui évite de faire transiter 60 Ko de HTML par une requête.

## 7. Industrialiser
1. Partir du modèle existant et garder TOUS ses crochets (logo, accroche personnalisée, emplacement de la note, galerie de vraies photos cachée, couche de vente, suivi) : le générateur ne remplace que le corps visible.
2. Un fichier de config par métier : textes des 3 phrases du problème, phrase de bascule, titre avant/après, textes alternatifs.
3. Construire, remplacer les variables par un faux client, rendre en 390 × 844 et 1 440 × 900 (Playwright), vérifier : zéro erreur JS, zéro `{{`, texte lisible sur l'image, avant/après aligné.
4. Publier comme nouvelle version du modèle ; dater le changement dans le journal ; mesurer sur la cohorte suivante (vues humaines, temps, profondeur de défilement, clics).

## 8. Contrôle final
- Mobile : l'accroche et l'appel sont visibles au-dessus de la barre de vente basse ; rien n'est caché sous l'en-tête.
- Poids : HTML < 70 Ko, image d'ouverture < 90 Ko, page complète < 1,5 Mo hors vidéo.
- Honnêteté : images d'illustration non présentées comme chantiers réels ; note et avis réels seulement.
