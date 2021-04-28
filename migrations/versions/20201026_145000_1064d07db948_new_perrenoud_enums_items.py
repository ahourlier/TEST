"""new perrenoud enums items

Revision ID: 1064d07db948
Revises: 07a44648f4a3
Create Date: 2020-10-26 14:50:00.515332

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import MetaData, Table

revision = "1064d07db948"
down_revision = "07a44648f4a3"
branch_labels = None
depends_on = None


def upgrade():

    meta = MetaData(bind=op.get_bind(), schema="core")
    meta.reflect(only=("perrenoud_enum",))
    perrenoud_enums = Table("perrenoud_enum", meta)

    # 11 / 39 / 41 / 42 / 43 / 44 / 46 /47
    new_perrenoud_enums = {
        11: [{"value": 0, "label": "Non"}, {"value": 1, "label": "Oui"}],
        39: [
            {"value": 101, "label": "Chaudière fioul classique avant 1970"},
            {"value": 102, "label": "Chaudière fioul classique entre 1971 et 1975"},
            {"value": 103, "label": "Chaudière fioul classique entre 1976 et 1980"},
            {"value": 104, "label": "Chaudière fioul classique entre 1981 et 1990"},
            {"value": 106, "label": "Chaudière fioul standard depuis 1994"},
            {"value": 107, "label": "Chaudière fioul basse température depuis 1991"},
            {"value": 108, "label": "Chaudière fioul condensation depuis 1996"},
            {"value": 188, "label": "Cogénération fioul  depuis 1996"},
            {"value": 201, "label": "Chaudière Gaz classique avant 1980"},
            {"value": 202, "label": "Chaudière Gaz classique entre 1981 et 1985"},
            {"value": 203, "label": "Chaudière Gaz classique entre 1986 et 1990"},
            {"value": 205, "label": "Chaudière Gaz standard entre 1994 et 2000"},
            {"value": 206, "label": "Chaudière Gaz standard depuis 2001"},
            {
                "value": 207,
                "label": "Chaudière Gaz basse température entre 1991 et 20l0",
            },
            {"value": 208, "label": "Chaudière Gaz basse température depuis 2001"},
            {"value": 211, "label": "Chaudière Gaz condensation depuis 2001"},
            {
                "value": 231,
                "label": "Radiateur Gaz  avant 2006 avec ou sans ventilateur",
            },
            {
                "value": 233,
                "label": "Radiateur Gaz après 2006 avec ou sans ventilateur",
            },
            {"value": 301, "label": "Chaudière Bois atmosphérique avant 1978"},
            {"value": 302, "label": "Chaudière Bois atmosphérique entre 1978 et 1994"},
            {"value": 303, "label": "Chaudière Bois atmosphérique après 1994 classe 1"},
            {"value": 304, "label": "Chaudière Bois atmosphérique après 1994 classe 2"},
            {"value": 305, "label": "Chaudière Bois atmosphérique après 1994 classe 3"},
            {"value": 311, "label": "Chaudière Bois atmosphérique après 1994 classe 4"},
            {"value": 312, "label": "Chaudière Bois atmosphérique après 1994 classe 5"},
            {"value": 401, "label": "Chaudière Charbon atmosphérique avant 1978"},
            {
                "value": 402,
                "label": "Chaudière Charbon atmosphérique entre 1978 et 1994",
            },
            {"value": 403, "label": "Chaudière Charbon atmosphérique après 1994"},
            {"value": 502, "label": "PAC air/air"},
            {"value": 503, "label": "PAC air/eau"},
            {"value": 504, "label": "PAC eau/eau"},
            {"value": 505, "label": "PAC géothermique"},
            {"value": 601, "label": "Chaudière électrique"},
        ],
        41: [
            {"value": 0, "label": "Emetteurs divisés"},
            {
                "value": 1,
                "label": "Emetteurs reliés à un chauffage central individuel",
            },
            {"value": 2, "label": "Emetteurs reliés à un chauffage central collectif",},
        ],
        42: [
            {"value": 0, "label": "Electrique effet joule"},
            {"value": 1, "label": "Fioul"},
            {"value": 2, "label": "Gaz"},
            {"value": 3, "label": "Bois"},
            {"value": 4, "label": "Charbon"},
            {"value": 5, "label": "Electrique thermodynamique(PAC)"},
        ],
        43: [
            {"value": 101, "label": "Convecteur électrique NF Catégorie C"},
            {"value": 102, "label": "Panneau rayonnant électrique NF catégorie C"},
            {"value": 103, "label": "Radiateur électrique NF catégorie C"},
            {"value": 106, "label": "Radiateur électrique accumulation"},
            {"value": 109, "label": "Soufflage air chaud effet joule"},
            {"value": 112, "label": "Convecteur électrique Ancien"},
            {"value": 113, "label": "Panneau rayonnant Ancien"},
            {"value": 114, "label": "Radiateur électrique Ancien"},
            {
                "value": 201,
                "label": "Générateur électrique - Radiateur HT sans robinet therm.",
            },
            {
                "value": 202,
                "label": "Générateur électrique - Radiateur HT avec robinet therm.",
            },
            {"value": 203, "label": "Générateur électrique - Plancher chauffant"},
            {"value": 204, "label": "Générateur électrique - Soufflage air chaud"},
            {
                "value": 301,
                "label": "Chauffage fioul - Radiateur HT sans robinet therm.",
            },
            {
                "value": 302,
                "label": "Chauffage fioul - Radiateur HT avec robinet therm.",
            },
            {"value": 303, "label": "Chauffage fioul - Plancher chauffant"},
            {"value": 304, "label": "Chauffage fioul - Soufflage air chaud"},
            {
                "value": 307,
                "label": "Chauffage fioul - Radiateur BT sans robinet therm.",
            },
            {
                "value": 308,
                "label": "Chauffage fioul - Radiateur BT avec robinet therm.",
            },
            {"value": 311, "label": "Poêle fioul"},
            {
                "value": 401,
                "label": "Chauffage gaz - Radiateur HT sans robinet therm.",
            },
            {
                "value": 402,
                "label": "Chauffage gaz - Radiateur HT avec robinet therm.",
            },
            {"value": 403, "label": "Chauffage gaz - Plancher chauffant"},
            {"value": 404, "label": "Chauffage gaz - Soufflage air chaud"},
            {
                "value": 407,
                "label": "Chauffage gaz - Radiateur BT sans robinet therm.",
            },
            {
                "value": 408,
                "label": "Chauffage gaz - Radiateur BT avec robinet therm.",
            },
            {"value": 411, "label": "Poêle GPL"},
            {"value": 417, "label": "Radiateur gaz à ventouse"},
            {"value": 418, "label": "Radiateur gaz sur conduit de fumées"},
            {
                "value": 501,
                "label": "Chauffage bois - Radiateur HT sans robinet therm.",
            },
            {
                "value": 502,
                "label": "Chauffage bois - Radiateur HT avec robinet therm.",
            },
            {"value": 503, "label": "Chauffage bois - Plancher chauffant"},
            {"value": 504, "label": "Chauffage bois - Soufflage air chaud"},
            {
                "value": 507,
                "label": "Chauffage bois - Radiateur BT sans robinet therm.",
            },
            {
                "value": 508,
                "label": "Chauffage bois - Radiateur BT avec robinet therm.",
            },
            {
                "value": 511,
                "label": "Poêle ou insert bois avant 2OOO ou sans label flamme verte",
            },
            {
                "value": 512,
                "label": "Poêle ou insert bois après 2OOO ou avec label flamme verte",
            },
            {
                "value": 601,
                "label": "Chauffage charbon - Radiateur HT sans robinet therm.",
            },
            {
                "value": 602,
                "label": "Chauffage charbon - Radiateur HT avec robinet therm.",
            },
            {"value": 603, "label": "Chauffage charbon - Plancher chauffant"},
            {"value": 604, "label": "Chauffage charbon - Soufflage air chaud"},
            {
                "value": 607,
                "label": "Chauffage charbon - Radiateur BT sans robinet therm.",
            },
            {
                "value": 608,
                "label": "Chauffage charbon - Radiateur BT avec robinet therm.",
            },
            {"value": 611, "label": "Poêle charbon"},
            {"value": 701, "label": "Split ou Multi - Split"},
            {"value": 702, "label": "PAC air / air"},
            {"value": 703, "label": "PAC - Radiateur HT sans robinet therm."},
            {"value": 704, "label": "PAC - Radiateur HT avec robinet therm."},
            {"value": 705, "label": "PAC - Plancher chauffant"},
            {"value": 706, "label": "PAC - Soufflage air chaud"},
            {"value": 709, "label": "PAC - Radiateur BT sans robinet therm."},
            {"value": 710, "label": "PAC - Radiateur BT avec robinet therm."},
        ],
        44: [
            {"value": 0, "label": "Aucun"},
            {"value": 2, "label": "Central avec minimum de température"},
            {"value": 3, "label": "Par pièce avec minimum de température"},
        ],
        46: [
            {"value": 0, "label": "Avant 2000 ou sans label flamme verte"},
            {"value": 1, "label": "Après 2000 ou avec label flamme verte"},
        ],
        47: [
            {"value": 0, "label": "Avant 1981"},
            {"value": 1, "label": "de 1981 à 2000"},
            {"value": 2, "label": "Après 2000"},
        ],
    }

    current_date = datetime.utcnow()
    rows = []
    for index, items in new_perrenoud_enums.items():
        for item in items:
            rows.append(
                {
                    "index": index,
                    "value": item.get("value"),
                    "label": item.get("label"),
                    "created_at": current_date,
                    "updated_at": current_date,
                }
            )

    op.bulk_insert(
        perrenoud_enums, rows,
    )


def downgrade():
    pass
