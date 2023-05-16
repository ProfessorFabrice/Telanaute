# Telanaute
L'utilisation d'un moteur de recherche afin de cibler les documents est
une méthode efficace mais qui présente néanmoins un certain nombre de
faiblesses. Nous ne maîtrisons tout d'abord pas l'ensemble des documents
indexés et de plus le langage de requête proposé est assez frustre.
C'est pour cette raison que nous avons développé notre propre moteur de
recherche, appelé Telanaute, dont nous présentons l'architecture et les
fonctionnalités. Le processus général est le suivant, à partir d'un
ensemble d'URL de départ (« graine ») il faut (i) récupérer les pages de
ces URL, (ii) chercher dans ces pages les liens, (iii) ajouter les liens
pointant vers des pages à récupérer, vers une liste d'URL à traiter.
Cette tâche, a priori simple, soulève des problèmes complexes (comment
extraire les adresses d'une page, lesquelles garder, comment stocker
efficacement la masse des documents récupérés, \...)

## Architecture

La plateforme est basée sur une conception modulaire qui offre aux
développeurs une grande souplesse et permet ainsi d'envisager un
développement en plusieurs phases distinctes échelonnées dans le temps.
Par ailleurs, la production de code et la correction d'erreurs sont
beaucoup plus aisées. Au lieu de rapatrier une partie du web puis de
sélectionner les pages intéressantes, l'idée est d'effectuer un parcours
en fonction de contraintes et de conserver uniquement les pages
intéressantes. Une collection est l'ensemble des pages ainsi
sélectionnées. Cette solution présente plusieurs avantages en
particulier, celui de limiter l'utilisation du réseau, l'espace disque
et le nombre de traitements effectués. Dans le but de constituer une
collection, il est nécessaire de disposer d'un ensemble d'URL. Cet
ensemble, que nous appelons graine, sera le point de départ de la
recherche de documents. Le concept de chaîne de traitements s'applique
aux différents traitements que nous devons effectuer sur une page
puisque ceux-ci doivent être généralement effectués dans un ordre
prédéfini. Les greffons sont une technique particulièrement bien adaptée
et permettent d'offrir la souplesse et la personnalisation nécessaire à
notre plate-forme. L'utilisateur a la possibilité de définir des
traitements spécifiques de manière simple à l'aide d'une interface de
programmation documentée. Par ailleurs ces greffons s'intègrent très
facilement dans la chaîne de traitement que l'utilisateur applique à une
collection. Les différentes expérimentations que nous avons pu faire à
l'aide d'un moteur commercial2 nous ont montré les limites de
l'utilisation du langage de balise XML pour stocker les résultats des
traitements. Ces limites sont toutes liées aux coûts d'utilisation du
processeur et d'espace disque et non en termes de pouvoir d'expression
d'XML. En effet, nous souhaitons stocker un maximum de documents sur un
minimum d'espace et comme nous ne disposons pas de machines suffisantes
pour effectuer les traitements, nous avons été contraints d'écarter XML.
Pour autant, l'utilisation de greffons permet d'envisager très
facilement son utilisation. Après une analyse approfondie, la
plate-forme a été découpée en quatre modules indépendants dont nous
détaillons ci-dessous les deux principaux.

## Arpenteur

L'arpenteur est chargé de parcourir le web en fonction de contraintes
définies par l'utilisateur (syntaxe de l'URL, contenu et type de la
page) et de stocker localement les pages retenues. Le processus itératif
de l'arpenteur est le suivant (voir figure 1) : 1.chargement depuis le
web d'une URL à récupérer, 2.application de contraintes définies à
l'aide de greffons dans une chaîne de traitements sur la page
correspondant à l'URL, 3.application de ces contraintes et classement de
la page dans l'un des états suivants : (a)la page est acceptée : elle
est alors sauvegardée sur disque et les liens contenus dans cette page
doivent être par la suite récupérés ; (b)la page est rejetée : ses liens
ne seront pas récupérés. En effet, si cette page n'est pas intéressante,
a priori les liens qu'elle contient ne le sont pas ; (c)la page n'est ni
acceptée ni rejetée : cet état survient lorsqu'une page contient peu de
texte, mais beaucoup de liens. La page n'est pas sauvegardée, mais ses
liens seront par la suite récupérés. Il est ainsi possible de
contraindre le parcours de l'arpenteur sur, par exemple, les pages
francophones des sites universitaires. Un premier filtre ne conserve que
les URL contenant l'une des formes traditionnelles des sites
universitaires (www.univ- par exemple), un second analyse le contenu des
pages et élimine ? au sens de l'étape (b) ? celles qui ne sont pas en
français.

## Traiteur

Le traiteur effectue une chaîne de traitements sur des fichiers
provenant, en particulier, de l'arpenteur, mais la source de données
peut provenir d'un autre média. Le principe de fonctionnement du
traiteur est très similaire à celui de l'arpenteur. Le document est pris
localement sur le disque et non plus récupéré sur le Web, les
contraintes exprimées par les filtres sont remplacées par des
traitements. Le processus itératif est le suivant (i) prise d'une page à
traiter en local (ii) application de la chaîne de traitements au travers
de greffons et pour chaque traitement le résultat est stocké sur le
disque (voir figure 2). Voici à titre d'exemple la chaîne de traitement
permettant, à partir de journaux en ligne, d'extraire les néologies
potentielles : html2texte : transformation d'un fichier au format HTML
en texte brut dico : utilisation d'un dictionnaire permettant de repérer
les mots potentiellement néologiques orthographe : élimination des
fautes les plus flagrantes à l'aide d'un correcteur orthographique
heuristiques : élimination d'erreurs non orthographique (par exemple 5
consonnes à la suite) rangeBase : rangement dans une base de données
Avantages : grande précision Inconvénients : mise en oeuvre délicate
