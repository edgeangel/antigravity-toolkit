# Patterns d'analyse avancés — Bibliothèque EdgeAngel

Patterns identifiés au fil des audits de performance. Chaque pattern décrit un symptôme, la méthode de détection, et l'insight clé.

---

## A. Traffic Dilution (Funnel Synthétique)

- **Symptôme** : les sessions augmentent mais le CA reste plat
- **Méthode** : comparer `AddToCart / Session` (qualité du trafic) vs `Purchase / AddToCart` (efficacité site)
- **Insight** : si `Purchase / AddToCart` est stable mais `AddToCart / Session` chute → le site convertit bien, le trafic entrant est simplement plus froid (audience moins qualifiée)

## B. Fragmentation Algorithmique

- **Symptôme** : éclater une campagne PMax consolidée en plusieurs petites campagnes (DSA, Shopping, Pockets) entraîne un crash du ROAS
- **Insight** : les algorithmes ML ont besoin d'un volume de signaux de conversion par campagne. La fragmentation dilue le signal, menant à des enchères sur des requêtes peu qualifiées

## C. Weather-Context Activation

- **Symptôme** : fort volume de navigation mais zéro vente pendant un mois « chaud »
- **Méthode** : croiser température (drive l'intérêt) avec pluviométrie (bloque l'activation)
- **Insight** : +3°C en février ne compte pas s'il pleut tous les jours. Les utilisateurs browsent mais reportent l'achat

## D. Reseller Pricing Gap

- **Symptôme** : volume de recherche élevé mais ventes e-com en baisse
- **Méthode** : comparer les prix du site avec les revendeurs (Darty, Boulanger, etc.) via Merchant Center `price_competitiveness_product_view`
- **Insight** : si la marque est systématiquement 100€+ plus chère, le site devient un showroom qui renvoie vers les revendeurs

## E. Indirect Brand Halo

- **Symptôme** : augmentation massive du budget brand en basse saison sans croissance e-com directe
- **Insight** : l'investissement « arrose » probablement les revendeurs. La notoriété ne se matérialise pas toujours sur le site .com mais contribue à l'écosystème global

## F. AOV / Mix Degradation

- **Symptôme** : le volume d'achats augmente (+40%) mais le CA ne suit pas (+10%)
- **Méthode** : comparer le prix unitaire moyen par produit/catégorie entre N et N-1
- **Insight** : les canaux d'acquisition (Meta/PMax) attirent des « acheteurs d'accessoires » (panier faible) plutôt que des « acheteurs de machines » (panier élevé), diluant l'AOV global

## G. Landing Page Rupture (Homepage Shift)

- **Symptôme** : explosion du taux de rebond sur la page d'entrée principale
- **Méthode** : comparer le bounce rate de la homepage N vs N-1
- **Insight** : un x2 ou x4 indique soit une régression UX/UI, soit un afflux de trafic non qualifié (bots ou post-click non pertinent) qui casse le funnel à la racine

## H. Meta Attribution Paradox

- **Symptôme** : Meta déclare 10+ conversions, GA4 en voit 1
- **Insight** : les campagnes Meta Advantage+ drivent un fort impact **post-view**. Si GA4 est quasi-nul mais la régie est saine, la campagne fonctionne probablement mais son impact est invisible en last-click. Croiser avec le lift de recherche brand

## I. Device Divergence (Mobile vs Desktop)

- **Symptôme** : le CA total est stable, mais Mobile explose (+170%) pendant que Desktop crash (-20%)
- **Insight** : le trafic « Growth » (Meta/Social) drive des transactions mobiles (items moins chers) tandis que l'audience Desktop core (intent élevé, machines) est soit en baisse, soit face à une friction spécifique (bug checkout, pricing gap sur le haut de gamme)

## J. Dynamic Recovery Validation

- **Symptôme** : débat entre « saisonnalité » vs « baisse de qualité opérationnelle » comme cause d'un creux
- **Méthode** : monitorer la première semaine du mois suivant (ex : 1-7 mars après un mauvais février)
- **Insight** : si la performance (CVR, ROAS, AOV) rebondit instantanément de +100% ou +200% avec des budgets et une structure similaires → ça invalide mathématiquement la « défaillance opérationnelle ». La demande était simplement supprimée et le setup était prêt à la capter dès que le marché s'est retourné

## K. Product Mix Scaling Paradox

- **Symptôme** : CA plat (+10%) alors que les achats augmentent significativement (+40%)
- **Méthode** : comparer le prix unitaire N vs N-1 par produit top. Calculer depuis l'event `purchase` : `itemRevenue / itemsPurchased`
- **Insight** : en phase de scaling horizontal, l'audience est plus large et plus sensible au prix. Le mix se déplace vers l'entrée de gamme. Plus de volume, mais AOV en baisse → CA plat

## L. Reseller Scaling Paradox (Lift Indirect)

- **Symptôme** : explosion du trafic et des recherches brand, mais CA e-com plat/en baisse. Meta/Google déclarent des conversions « View » saines
- **Insight** : l'investissement « arrose » les revendeurs. Le .com fait showroom, et le scaling se matérialise en revenue B2B revendeur plutôt qu'en D2C

## M. GA4 Modeling Inflection Bias

- **Symptôme** : comparaison N vs N-1 montre un +10% « suspect » sur tous les métriques malgré une mauvaise performance back-office
- **Méthode** : vérifier si le Behavioral Modeling (GA4 Consent Mode V2) était actif en N mais pas en N-1
- **Insight** : les données 2026 incluent souvent des utilisateurs *modélisés* (consentement refusé), tandis que 2025 est souvent « pur ». Cela crée un gap artificiel de +10-20%. Toute « croissance » sous 15% doit être traitée comme un déclin réel

## N. Promo Creative Dead-Weight

- **Symptôme** : une campagne « Promos » ou « Advantage+ » montre un ROAS qui se détériore malgré une audience à forte intention
- **Méthode** : analyser au niveau **Ad** (pas Ad Set). Comparer les créas saisonnières (Soldes, Valentine) vs les créas produit evergreen
- **Insight** : les créas événementielles attirent des clics mais ne convertissent pas si l'offre n'est pas assez agressive. Elles « volent » du budget aux créas produit qui fonctionnaient. Les pauser peut restaurer le ROAS instantanément

## O. Discount Intent / Offer Gap (Incentive Expiration)

- **Symptôme** : fort volume d'impressions/clics sur « code promo [Marque] » mais zéro conversion
- **Méthode** : comparer le volume de recherche discount N vs N-1 et vérifier les dates de fin des opérations commerciales
- **Insight** : si le volume augmente mais les conversions disparaissent, il y a un gap entre la demande d'incentive et l'offre :
  1. **Expiration de l'incentive** : le budget est encore actif mais la promo du mois précédent est terminée. L'utilisateur cherche un deal, trouve une pub, mais le code/la LP n'est plus valide
  2. **Hijacking conversion** : l'utilisateur ne trouve pas l'incentive attendu et redirige vers un revendeur qui a encore une promo
  3. **Échec LP** : la landing page ne mentionne pas les « soldes » ou le « code » référencé dans la requête

## P. Longitudinal Brand / Generic Shift

- **Symptôme** : le budget augmente significativement N vs N-1 (ex : x3) mais le ROAS global baisse
- **Méthode** : comparer la distribution spend/conversions entre termes « Brand » et « Generic » sur une période longue (6-9 mois)
- **Insight** : identifier si le compte scale en surenchérissant sur sa propre marque (cannibalisation) ou si la croissance est saine (expansion non-branded). En PMax, utiliser `campaign_search_term_insight` pour classifier brand vs generic
