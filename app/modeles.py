from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, Text, DateTime, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_security.models import fsqla_v3 as fsqla
from flask_sqlalchemy import SQLAlchemy

projets = [
  {"id": 1, "titre": "Pages d'accueil", "image": "img/site00.png", "description": 
"""Vitrine de votre site, la page d'accueil doit être esthétique, ergonomique et fonctionnelle pour séduire \
vos visiteurs. Nous créons des pages d'accueil sur mesure, adaptées à votre univers graphique et à vos \
besoins."""},
  {"id": 2, "titre": "Fiches produits", "image": "img/site01.png", "description": 
"""Éléments clés de votre site e-commerce, les fiches produits doivent être attractives, informatives et \
ergonomiques pour séduire vos visiteurs et les inciter à acheter. Nous créons des fiches produits sur \
mesure, adaptées à votre univers graphique et à vos besoins."""},
  {"id": 3, "titre": "SEO", "image": "img/site02.png", "description": 
"""Le référencement naturel (SEO) est essentiel pour attirer de nouveaux visiteurs et augmenter votre trafic. \
Nous mettons en place une stratégie de référencement naturel pertinente et adaptée à votre activité.
"""},
  {"id": 4, "titre": "Persona", "image": "img/site03.png", "description": 
"""Les personas sont des profils types de vos clients, créés à partir de données réelles et de recherches \
qualitatives. Ils vous permettent de mieux comprendre vos cibles et de mieux répondre à leurs besoins. \
Nous créons des personas marketing pertinents et adaptés à votre marché."""},
  {"id": 5, "titre": "Catalogues", "image": "img/site04.png", "description": 
"""Éléments clés de votre site e-commerce, les catalogues en ligne doivent être attractifs, informatifs et \
ergonomiques pour séduire vos visiteurs et les inciter à acheter. Nous créons des catalogues en ligne sur \
mesure, adaptés à votre univers graphique et à vos besoins."""},
  {"id": 6, "titre": "Carrousels", "image": "img/site05.png", "description": 
"""Éléments de navigation permettant de faire défiler des contenus, les carrousels sont très utilisés sur les \
sites internet pour mettre en valeur des contenus et faciliter la navigation. Nous élaborons des \
carrousels sur mesure, adaptés à votre univers graphique et à vos besoins."""},
  {"id": 7, "titre": "Applications", "image": "img/site06.png", "description": 
"""Les applications web sont des logiciels accessibles en ligne via un navigateur internet. Elles sont très \
utilisées pour faciliter la gestion et le partage de données, et pour proposer des services en ligne. Nous \
concevons des applications web sur mesure, adaptées à vos besoins et à votre activité."""},
  {"id": 8, "titre": "Pages de contact", "image": "img/site07.png", "description": 
"""Éléments clés de votre site internet, les pages de contact doivent être esthétiques, ergonomiques et \
fonctionnelles pour inciter vos visiteurs à vous contacter et à établir une relation de confiance. Nous \
créons des pages de contact sur mesure, adaptées à votre univers graphique et à vos besoins."""},
]

references = [
  {"id": 1, "entreprise": "Aqua Corp."    , "logo": "img/logos/aqua.png"},
  {"id": 2, "entreprise": "Business Inc." , "logo": "img/logos/business.png"},
  {"id": 3, "entreprise": "Colormix Ltd." , "logo": "img/logos/colormix.png"},
  {"id": 4, "entreprise": "Globe SA"      , "logo": "img/logos/globe.png"},
  {"id": 5, "entreprise": "Integration AG", "logo": "img/logos/integration.png"},
  {"id": 6, "entreprise": "Lock Gmbh"     , "logo": "img/logos/lock.png"},
  {"id": 7, "entreprise": "People Care SE", "logo": "img/logos/peoplecare.png"},
  {"id": 8, "entreprise": "Teamwork Co."  , "logo": "img/logos/teamwork.png"},
  {"id": 9, "entreprise": "Wave SAS"      , "logo": "img/logos/wave.png"},
]

avis = [
  {"id": 1, "id_projet": 1, "creation": datetime(2021, 3, 15, 14, 25, 6), "likes": 2, "auteur": "Jeanne L.", "contenu": 
"""Alice a su créer une page d'accueil à la fois esthétique et fonctionnelle pour notre site internet. Grâce \
à ses compétences en Python et en développement web, elle a répondu à toutes nos attentes et nous sommes \
ravis du résultat."""},
  {"id": 2, "id_projet": 1, "creation": datetime(2022, 1, 8, 9, 12, 33), "likes": 1, "auteur": "Marc D.", "contenu": 
"""Je recommande vivement Mme BOB qui a parfaitement su s'adapter à nos besoins et à notre univers graphique. \
La page qu'elle a développée est fluide, ergonomique et très bien optimisée.
"""},
  {"id": 3, "id_projet": 1, "creation": datetime(2021, 11, 27, 17, 45, 51), "likes": 3, "auteur": "Leïla B.", "contenu": 
"""Travailler avec Alice BOB a été un réel plaisir. Elle est à l'écoute, réactive et très professionnelle. La \
page d'accueil qu'elle a créée pour notre site est moderne, dynamique et correspond parfaitement à notre \
cahier des charges."""},

  {"id": 4, "id_projet": 2, "creation": datetime(2022, 2, 19, 12, 34, 8), "likes": 0, "auteur": "Kim L.", "contenu": 
"""Les fiches produits réalisées par Alice sont tout simplement exceptionnelles. Elle a su mettre en valeur \
nos produits grâce à un design soigné et des fonctionnalités innovantes. Nos clients sont conquis et nos \
ventes ont augmenté."""},
  {"id": 5, "id_projet": 2, "creation": datetime(2021, 6, 4, 22, 15, 23), "likes": 4, "auteur": "Inès M.", "contenu": 
"""Mme BOB a fait un travail remarquable sur nos fiches produits. Elle a parfaitement intégré nos contenus et \
nos visuels, tout en optimisant le référencement naturel. Nous sommes très satisfaits de sa prestation et \
la recommandons sans hésitation."""},
  {"id": 6, "id_projet": 2, "creation": datetime(2022, 3, 24, 15, 28, 46), "likes": 2, "auteur": "William D.", "contenu": 
"""Grâce à Alice, nos fiches produits sont désormais claires, attrayantes et très bien organisées. Elle a su \
comprendre nos besoins et nos contraintes, et a développé une solution sur mesure en Python. Nous sommes \
ravis de cette collaboration."""},

  {"id": 7, "id_projet": 3, "creation": datetime(2021, 8, 22, 8, 45, 12), "likes": 1, "auteur": "Emma R.", "contenu": 
"""Experte en référencement naturel, Alice a su optimiser notre site internet et nos contenus pour améliorer \
notre visibilité sur les moteurs de recherche. Résultat : notre trafic a augmenté et nos clients nous \
trouvent plus facilement."""},
  {"id": 8, "id_projet": 3, "creation": datetime(2022, 1, 15, 11, 56, 29), "likes": 3, "auteur": "Firmin P.", "contenu": 
"""Je suis très satisfait de la prestation de Mme BOB en matière de SEO. Elle a su nous proposer des \
solutions concrètes et efficaces pour améliorer notre référencement. Elle est également très pédagogue et \
nous a donné de précieux conseils pour la suite."""},
  {"id": 9, "id_projet": 3, "creation": datetime(2021, 4, 18, 16, 33, 47), "likes": 0, "auteur": "Fatima Z.", "contenu": 
"""Mme BOB a su mettre en place une stratégie de référencement naturel pertinente et adaptée à notre \
activité. Elle a travaillé sur nos mots-clés, nos balises et nos liens, et nous avons vu une nette \
amélioration de notre positionnement sur Google. Merci Alice !"""},

  {"id": 10, "id_projet": 4, "creation": datetime(2022, 2, 26, 9, 48, 13), "likes": 2, "auteur": "Marie-Ange G.", "contenu": 
"""Alice nous a accompagnés dans la création de nos personas marketing, et nous sommes ravis du résultat. \
Elle a su comprendre nos cibles et nos enjeux, et a développé des profils types très précis et \
exploitables. Nous recommandons vivement ses services."""},
  {"id": 11, "id_projet": 4, "creation": datetime(2021, 12, 6, 21, 12, 58), "likes": 1, "auteur": "Mehdi L.", "contenu": 
"""Alice BOB a su nous apporter son expertise et sa méthodologie pour créer des personas pertinents et \
adaptés à notre marché. Elle a su nous challenger et nous faire réfléchir à nos cibles de manière \
approfondie. Une collaboration très enrichissante."""},
  {"id": 12, "id_projet": 4, "creation": datetime(2022, 3, 13, 14, 26, 35), "likes": 4, "auteur": "Lucia F.", "contenu": 
"""Grâce à Mme BOB, nous avons pu créer des personas qui nous permettent de mieux comprendre nos clients et \
de mieux répondre à leurs besoins. Elle a su nous guider et nous conseiller tout au long du processus, et \
a fait preuve d'une grande écoute et d'une grande adaptabilité."""},

  {"id": 13, "id_projet": 5, "creation": datetime(2021, 5, 11, 13, 39, 14), "likes": 0, "auteur": "Trésor R.", "contenu": 
"""Alice a su créer un catalogue en ligne à la fois esthétique et fonctionnel pour notre entreprise. Elle a \
su intégrer nos produits et nos visuels de manière optimale, et a développé des fonctionnalités \
innovantes pour faciliter la navigation et la recherche. Nous sommes très satisfaits de cette collaboration."""},
  {"id": 14, "id_projet": 5, "creation": datetime(2022, 1, 23, 10, 52, 41), "likes": 2, "auteur": "Karine M.", "contenu": 
"""Mme BOB a fait un travail remarquable sur notre catalogue en ligne. Elle a su s'adapter à nos besoins et \
à notre univers graphique, et a développé une solution sur mesure en Python. Nos clients sont conquis et \
nos ventes ont augmenté. Nous recommandons vivement ses services."""},
  {"id": 15, "id_projet": 5, "creation": datetime(2021, 9, 29, 18, 18, 27), "likes": 1, "auteur": "Frédéric B.", "contenu": 
"""Le catalogue en ligne réalisé par Alice est tout simplement exceptionnel. Elle a su mettre en valeur \
nos produits grâce à un design soigné et des fonctionnalités innovantes. Nos clients sont ravis et nous \
aussi. Merci Alice pour cette collaboration très réussie."""},

  {"id": 16, "id_projet": 6, "creation": datetime(2022, 2, 8, 12, 24, 54), "likes": 3, "auteur": "Livia R.", "contenu": 
"""Alice a su créer des carrousels à la fois esthétiques et fonctionnels pour notre site internet. Grâce à \
ses compétences en développement web, elle a répondu à toutes nos attentes et nous sommes ravis du \
résultat. Nos clients apprécient également la fluidité et l'ergonomie des carrousels."""},
  {"id": 17, "id_projet": 6, "creation": datetime(2021, 7, 17, 20, 45, 32), "likes": 0, "auteur": "Romain G.", "contenu": 
"""Je recommande vivement Mme BOB pour la création de carrousels. Elle a parfaitement su s'adapter à nos \
besoins et à notre univers graphique. Les carrousels qu'elle a développés sont fluides, ergonomiques et \
très bien optimisés. Nos clients sont conquis et nos ventes ont augmenté."""},
  {"id": 18, "id_projet": 6, "creation": datetime(2022, 3, 5, 15, 50, 9), "likes": 2, "auteur": "Samia B.", "contenu": 
"""Travailler avec Alice BOB a été un réel plaisir. Elle est à l'écoute, réactive et très professionnelle. \
Les carrousels qu'elle a créés pour notre site sont modernes, dynamiques et correspondent parfaitement à \
notre cahier des charges. Nous sommes ravis de cette collaboration et la recommandons sans hésitation."""},

  {"id": 19, "id_projet": 7, "creation": datetime(2021, 10, 24, 7, 33, 26), "likes": 1, "auteur": "Joseph S.", "contenu": 
"""Mme BOB a su développer une application web à la fois esthétique et fonctionnelle pour notre entreprise. \
Elle a su intégrer nos contenus et nos visuels de manière optimale, et a développé des fonctionnalités \
innovantes pour faciliter la navigation et la recherche. Nous sommes très satisfaits de cette collaboration."""},
  {"id": 20, "id_projet": 7, "creation": datetime(2022, 1, 30, 11, 4, 53), "likes": 4, "auteur": "Maria R.", "contenu": 
"""Alice a fait un travail remarquable sur notre application web. Elle a su s'adapter à nos besoins et à \
notre univers graphique, et a développé une solution sur mesure en Python. Nos clients sont conquis et \
nos ventes ont augmenté. Nous recommandons vivement ses services."""},
  {"id": 21, "id_projet": 7, "creation": datetime(2021, 2, 9, 14, 12, 40), "likes": 0, "auteur": "Yannick C.", "contenu": 
"""L'application web réalisée par Alic est tout simplement exceptionnelle. Elle a su mettre en valeur nos \
produits grâce à un design soigné et des fonctionnalités innovantes. Nos clients sont ravis et nous aussi. \
Merci Alice pour cette collaboration très réussie."""},

  {"id": 22, "id_projet": 8, "creation": datetime(2022, 2, 16, 9, 28, 17), "likes": 2, "auteur": "Virginie D.", "contenu": 
"""Alice a su créer une page de contact à la fois esthétique et fonctionnelle pour notre site internet. Grâce \
à ses compétences en Python et en développement web, elle a répondu à toutes nos attentes et nous sommes \
ravis du résultat. Nos clients apprécient également la fluidité et l'ergonomie de la page."""},
  {"id": 23, "id_projet": 8, "creation": datetime(2021, 3, 26, 17, 45, 59), "likes": 1, "auteur": "José M.", "contenu": 
"""Je recommande vivement Mme BOB pour la création de pages de contact. Elle a parfaitement su s'adapter à \
nos besoins et à notre univers graphique. La page de contact qu'elle a développée est fluide, ergonomique \
et très bien optimisée. Nos clients sont conquis et nous aussi."""},
  {"id": 24, "id_projet": 8, "creation": datetime(2022, 3, 20, 14, 33, 38), "likes": 3, "auteur": "Nadia AIT-S.", "contenu": 
"""Travailler avec Alice BOB a été un réel plaisir. Elle est à l'écoute, réactive et très professionnelle. \
La page de contact qu'elle a créée pour notre site est moderne, dynamique et correspond parfaitement à \
notre cahier des charges. Nous sommes ravis de cette collaboration et la recommandons sans hésitation."""},
]

refs_projets = [
  {"id_projet": 1, "id_reference": 3},
  {"id_projet": 1, "id_reference": 1},
  {"id_projet": 1, "id_reference": 5},

  {"id_projet": 2, "id_reference": 9},
  {"id_projet": 2, "id_reference": 2},
  {"id_projet": 2, "id_reference": 1},
  {"id_projet": 2, "id_reference": 7},

  {"id_projet": 3, "id_reference": 4},
  {"id_projet": 3, "id_reference": 8},
  {"id_projet": 3, "id_reference": 1},

  {"id_projet": 4, "id_reference": 6},
  {"id_projet": 4, "id_reference": 2},
  {"id_projet": 4, "id_reference": 5},
  {"id_projet": 4, "id_reference": 3},
  {"id_projet": 4, "id_reference": 7},

  {"id_projet": 5, "id_reference": 8},
  {"id_projet": 5, "id_reference": 6},
  {"id_projet": 5, "id_reference": 4},

  {"id_projet": 6, "id_reference": 2},
  {"id_projet": 6, "id_reference": 9},

  {"id_projet": 7, "id_reference": 7},
  {"id_projet": 7, "id_reference": 8},
  {"id_projet": 7, "id_reference": 5},
  {"id_projet": 7, "id_reference": 4},

  {"id_projet": 8, "id_reference": 6},
  {"id_projet": 8, "id_reference": 9},
  {"id_projet": 8, "id_reference": 3},
]

db = SQLAlchemy()


references_projets = Table(
    'references_projets', db.Model.metadata,
    Column('id_reference', ForeignKey('references.id'), primary_key=True),
    Column('id_projet'   , ForeignKey('projets.id'   ), primary_key=True)
)


class Contact(db.Model):
  __tablename__ = 'contacts'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  creation: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
  mail: Mapped[str]
  sujet: Mapped[str] = mapped_column(String(20))
  message: Mapped[str] = mapped_column(Text())

  def dto(self):
    return {
        attr: getattr(self, attr)
        for attr in ['id', 'creation', 'mail', 'sujet', 'message']
    }


class Reference(db.Model):
  __tablename__ = 'references'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  entreprise: Mapped[str] = mapped_column(String(50))
  logo: Mapped[str]

  projets: Mapped[List['Projet']] = relationship(secondary=references_projets, back_populates='refs')


class Projet(db.Model):
  __tablename__ = 'projets'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  titre: Mapped[str] = mapped_column(String(50))
  description: Mapped[Optional[str]] = mapped_column(Text())
  image: Mapped[Optional[str]] 

  avis: Mapped[List['Avis']] = relationship(back_populates='projet', cascade="all, delete-orphan")
  refs: Mapped[List['Reference']] = relationship(secondary=references_projets, back_populates='projets')


class Avis(db.Model):
  __tablename__ = 'avis'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  creation: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
  contenu: Mapped[str]
  ok: Mapped[bool] = mapped_column(default=False)
  likes: Mapped[int] = mapped_column(default=0)
  auteur: Mapped[Optional[str]] = mapped_column(String(50))

  id_projet: Mapped[int] = mapped_column(ForeignKey('projets.id'))
  projet: Mapped['Projet'] = relationship(back_populates='avis')
  
  def dto(self):
    return {
        attr: getattr(self, attr)
        for attr in ['id', 'creation', 'contenu', 'ok', 'likes', 'auteur', 'id_projet']
    }


fsqla.FsModels.set_db_info(db, user_table_name='utilisateurs', role_table_name='roles', webauthn_table_name='webauthn')


class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = 'roles'


class Utilisateur(db.Model, fsqla.FsUserMixin):
    __tablename__ = 'utilisateurs'

    logo: Mapped[Optional[str]]


class WebAuthn(db.Model, fsqla.FsWebAuthnMixin):
    __tablename__ = 'webauthn'

