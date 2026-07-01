#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Potent Garden - Cannabis Genetic Clade Wheel
=============================================

Source-of-truth generator for a 4-ring hierarchical ("clade wheel" / sunburst)
taxonomy of 250 representative cannabis cultivars, chosen to span the plant's
genetic and chemotype variability.

Rings
-----
  Ring 1 : Clade        (major genetic lineage, ~9 groups)
  Ring 2 : Sub-family   (branch within a clade)
  Ring 3 : Group        (tight cluster / cut family)
  Ring 4 : Strain       (leaf; carries parents, description, terpenes,
                         chemotype and cannabinoid ranges)

Each leaf strain records:
  name           - cultivar name
  parents        - documented / best-consensus lineage
  description    - one-line character note
  terpenes       - top 3-8 terpenes ordered by typical dominance
  chemotype      - Type I / II / III / IV / THCV / CBN framework
  cannabinoids   - approximate THC / CBD / other ranges

Run:
  python build_data.py
It writes potent_garden_clade_wheel.json and prints a progress report every
12 strains plus validation (leaf count == 250, all anchor strains present).

Data are grounded in well-established cannabis-genetics knowledge and public
aggregate lab/terpene data (Leafly, Phylos, Sensi/Green House/DNA breeder
records, and chemotype literature - de Meijer, Hillig 2004). Clone-only cuts
(OG Kush, Bubba, Tahoe, Louis XIII, GG4, etc.) have disputed pedigrees; their
parentage is best-consensus, and terpene orders are typical-case, not fixed.
See strains_table.md for the full References section.
"""

import json
import os

# --------------------------------------------------------------------------
# Chemotype vocabulary (de Meijer / Hillig framework + minor-cannabinoid tags)
# --------------------------------------------------------------------------
TYPE_I   = "Type I (THC-dominant)"
TYPE_II  = "Type II (mixed THC:CBD)"
TYPE_III = "Type III (CBD-dominant)"
TYPE_IV  = "Type IV (CBG-dominant)"
THCV     = "THCV-rich (propyl / Type I+V)"
CBN      = "Type I + notable CBN (oxidative/sedative)"


def S(name, parents, desc, terps, chemo, cann):
    """Build one leaf strain record."""
    return {
        "name": name,
        "type": "strain",
        "parents": parents,
        "description": desc,
        "terpenes": terps,
        "chemotype": chemo,
        "cannabinoids": cann,
        "value": 1,
    }


# --------------------------------------------------------------------------
# THE TREE
#   [ (clade, [ (subfamily, [ (group, [ S(), ... ]) ]) ]) ]
# --------------------------------------------------------------------------
TREE = [

# ==========================================================================
# CLADE A - EQUATORIAL SATIVA LANDRACES
# ==========================================================================
("Equatorial Sativa Landraces", [
    ("African Landraces", [
        ("Southern African", [
            S("Durban Poison", "South African landrace (sativa)",
              "Foundational THCV donor; sweet-anise pine sativa.",
              ["terpinolene", "myrcene", "pinene", "ocimene", "limonene"],
              THCV, "THC 15-25%, THCV up to ~1%, CBD <0.5%"),
            S("Swazi Gold", "Swaziland landrace (sativa)",
              "Eswatini highland sativa, energetic and incense-spiced.",
              ["terpinolene", "pinene", "ocimene", "myrcene"],
              TYPE_I, "THC 15-20%, CBD <0.5%"),
            S("Malawi Gold", "Malawi landrace (sativa)",
              "Long-flowering equatorial 'chamba'; soaring cerebral high.",
              ["terpinolene", "ocimene", "pinene", "limonene"],
              TYPE_I, "THC 18-24%, CBD <0.5%"),
            S("Rooibaard", "South African landrace (sativa)",
              "Red-bearded Transkei landrace, citrus-herbal.",
              ["terpinolene", "pinene", "myrcene"],
              TYPE_I, "THC 12-18%, CBD <0.5%"),
        ]),
        ("Central & West African", [
            S("Congolese", "Democratic Republic of Congo landrace",
              "Equatorial jungle sativa, spicy-sweet and racy.",
              ["terpinolene", "ocimene", "caryophyllene", "pinene"],
              TYPE_I, "THC 16-22%, CBD <0.5%"),
            S("Red Congolese", "Congolese x Mexican/Afghani selection",
              "Refined Congo sativa, clear energetic effect.",
              ["terpinolene", "pinene", "limonene", "myrcene"],
              THCV, "THC 18-22%, some THCV, CBD <0.5%"),
            S("Nigerian", "Nigerian landrace (sativa)",
              "West African equatorial sativa, fuel-herbal.",
              ["terpinolene", "myrcene", "pinene"],
              TYPE_I, "THC 14-20%, CBD <0.5%"),
            S("Kilimanjaro", "East African landrace (Kenya/Tanzania)",
              "'Elephant flattener'; intense energetic highland sativa.",
              ["terpinolene", "pinene", "ocimene"],
              TYPE_I, "THC 16-22%, CBD <0.5%"),
        ]),
    ]),
    ("Southeast & South Asian Sativa", [
        ("Thai & Indochina", [
            S("Thai", "Southeast Asian landrace (Thailand)",
              "Classic equatorial sativa; founding Haze contributor.",
              ["terpinolene", "ocimene", "pinene", "limonene"],
              THCV, "THC 15-22%, occasional THCV, CBD <0.5%"),
            S("Chocolate Thai", "Thai landrace selection",
              "Coffee-cocoa aromatic Thai, cerebral and rare.",
              ["myrcene", "terpinolene", "caryophyllene", "pinene"],
              TYPE_I, "THC 14-18%, CBD <0.5%"),
            S("Cambodian", "Cambodian landrace (sativa)",
              "Indochina lowland sativa, sweet and buzzy.",
              ["terpinolene", "ocimene", "limonene"],
              TYPE_I, "THC 15-20%, CBD <0.5%"),
            S("Vietnamese Black", "Vietnam highland landrace",
              "Dark-leaved Indochina sativa, potent and racy.",
              ["terpinolene", "myrcene", "pinene", "ocimene"],
              TYPE_I, "THC 16-22%, CBD <0.5%"),
        ]),
        ("South Asian Highland", [
            S("Manipuri", "Northeast India landrace (sativa)",
              "Himalayan foothill sativa, resinous and clear.",
              ["terpinolene", "pinene", "myrcene"],
              TYPE_I, "THC 14-19%, CBD <1%"),
            S("Nepalese Highland", "Nepal highland landrace",
              "Charas-selected hill sativa; incense and spice.",
              ["myrcene", "pinene", "caryophyllene", "terpinolene"],
              TYPE_I, "THC 14-20%, CBD <1%"),
        ]),
    ]),
    ("Latin American Sativa", [
        ("Mexican", [
            S("Oaxacan", "Mexican highland landrace (Oaxaca)",
              "Highland sativa; ancestral input to Original Haze.",
              ["terpinolene", "ocimene", "pinene", "limonene", "myrcene"],
              TYPE_I, "THC 15-23%, CBD <0.5%"),
            S("Acapulco Gold", "Mexican landrace (Guerrero coast)",
              "Legendary golden sativa, toffee-citrus and uplifting.",
              ["myrcene", "pinene", "caryophyllene", "terpinolene"],
              TYPE_I, "THC 18-24%, CBD <0.5%"),
            S("Michoacan", "Mexican landrace (Michoacan)",
              "Pacific-coast sativa, sweet-earthy and energetic.",
              ["terpinolene", "myrcene", "pinene"],
              TYPE_I, "THC 15-20%, CBD <0.5%"),
            S("Sinaloa", "Mexican landrace (Sinaloa)",
              "Sierra Madre sativa, spicy and buoyant.",
              ["terpinolene", "ocimene", "caryophyllene"],
              TYPE_I, "THC 14-19%, CBD <0.5%"),
        ]),
        ("Colombian & Andean", [
            S("Colombian Gold", "Colombian landrace (Santa Marta)",
              "Golden Santa Marta sativa; a core Haze ancestor.",
              ["terpinolene", "pinene", "limonene", "myrcene"],
              TYPE_I, "THC 15-22%, CBD <0.5%"),
            S("Punto Rojo", "Colombian mountain landrace",
              "Red-hued Andean sativa, dense and cerebral.",
              ["terpinolene", "myrcene", "pinene", "caryophyllene"],
              TYPE_I, "THC 16-21%, CBD <0.5%"),
            S("Panama Red", "Panamanian landrace (sativa)",
              "1960s icon; rich red equatorial sativa.",
              ["terpinolene", "ocimene", "limonene"],
              TYPE_I, "THC 14-20%, CBD <0.5%"),
        ]),
        ("Caribbean & Pacific Island", [
            S("Lambs Bread", "Jamaican landrace (sativa)",
              "Bob Marley's bright, cheesy-herbal island sativa.",
              ["terpinolene", "myrcene", "pinene", "caryophyllene"],
              TYPE_I, "THC 16-21%, CBD <0.5%"),
            S("Kings Bread", "Jamaican landrace (sativa)",
              "Jamaican hill sativa, sweet and euphoric.",
              ["terpinolene", "ocimene", "pinene"],
              TYPE_I, "THC 15-20%, CBD <0.5%"),
            S("Maui Wowie", "Hawaiian landrace (sativa)",
              "Volcanic-soil sativa; tropical pineapple lift.",
              ["myrcene", "pinene", "ocimene", "caryophyllene"],
              TYPE_I, "THC 15-20%, CBD <0.5%"),
            S("Hawaiian", "Hawaiian landrace (sativa)",
              "Island sativa, fruity-floral and creative.",
              ["ocimene", "myrcene", "pinene", "limonene"],
              TYPE_I, "THC 14-19%, CBD <0.5%"),
            S("Kona Gold", "Hawaiian landrace (Big Island)",
              "Big Island sativa, citrus-tropical and clear.",
              ["terpinolene", "myrcene", "limonene"],
              TYPE_I, "THC 15-20%, CBD <0.5%"),
        ]),
    ]),
]),

# ==========================================================================
# CLADE B - SOUTH / CENTRAL ASIAN INDICA LANDRACES
# ==========================================================================
("Asian Indica Landraces", [
    ("Afghan Broadleaf", [
        ("Afghani Core", [
            S("Afghani", "Hindu Kush landrace (broadleaf indica)",
              "Resin-rich hashish landrace; ancestor of modern indicas.",
              ["myrcene", "caryophyllene", "humulene", "pinene"],
              TYPE_I, "THC 15-20%, CBD <1% (some Type II phenos)"),
            S("Mazar-i-Sharif", "Afghan landrace (Balkh province)",
              "Legendary hash-plant Afghani; heavy and sweet-earthy.",
              ["myrcene", "caryophyllene", "limonene"],
              TYPE_I, "THC 15-21%, CBD <1%"),
            S("Balkh Afghani", "Afghan landrace (Balkh)",
              "Northern Afghan broadleaf, incense-resinous.",
              ["myrcene", "humulene", "caryophyllene"],
              TYPE_I, "THC 14-19%, CBD <1%"),
            S("Afghan Kush", "Hindu Kush landrace selection",
              "Pure Afghan indica, sedative sandalwood-hash.",
              ["myrcene", "caryophyllene", "limonene", "humulene"],
              TYPE_I, "THC 16-21%, CBD <1%"),
        ]),
        ("Hindu Kush & Pakistani", [
            S("Hindu Kush", "Afghanistan/Pakistan landrace (indica)",
              "Foundational mountain indica; earthy sandalwood.",
              ["myrcene", "caryophyllene", "limonene", "humulene"],
              TYPE_I, "THC 15-20%, CBD <1%"),
            S("Pakistani Chitral Kush", "Pakistan landrace (Chitral valley)",
              "Frosty valley indica, sweet hash and berry.",
              ["myrcene", "pinene", "caryophyllene"],
              TYPE_I, "THC 18-22%, CBD <1%"),
            S("Pakistani Valley", "Pakistan landrace (indica)",
              "Broadleaf valley kush, resinous and calm.",
              ["myrcene", "caryophyllene", "humulene"],
              TYPE_I, "THC 15-20%, CBD <1%"),
        ]),
    ]),
    ("Charas & Hashplant Types", [
        ("Hash Plant Lineage", [
            S("Hash Plant", "Afghani-heavy hashplant selection",
              "Sensi hash-resin indica; peppery sandalwood.",
              ["myrcene", "caryophyllene", "humulene", "limonene"],
              TYPE_I, "THC 16-20%, CBD <1%"),
            S("Deep Chunk", "Afghani landrace (Tom Hill line)",
              "Old-school pure Afghani; a modern-indica cornerstone.",
              ["myrcene", "caryophyllene", "pinene"],
              TYPE_I, "THC 14-19%, CBD <1%"),
        ]),
        ("Indian & Nepali Indica", [
            S("Nepalese Indica", "Nepal charas landrace",
              "Hand-rubbed charas indica; spicy and resinous.",
              ["myrcene", "pinene", "caryophyllene", "humulene"],
              TYPE_I, "THC 14-19%, CBD <1%"),
            S("Kashmir", "Kashmir Himalayan landrace",
              "Cold-hardy hash indica, floral-earthy.",
              ["myrcene", "linalool", "caryophyllene"],
              TYPE_I, "THC 13-18%, CBD <1%"),
            S("Parvati", "India (Parvati valley) landrace",
              "Malana-region charas plant, incense-sweet.",
              ["myrcene", "caryophyllene", "pinene"],
              TYPE_I, "THC 14-18%, CBD <1%"),
        ]),
    ]),
]),

# ==========================================================================
# CLADE C - HAZE LINEAGE
# ==========================================================================
("Haze Lineage", [
    ("Original Haze Core", [
        ("Foundational Haze", [
            S("Haze", "Colombian x Mexican x South Indian x Thai",
              "The Santa Cruz original; textbook terpinolene sativa.",
              ["terpinolene", "pinene", "caryophyllene", "myrcene", "ocimene"],
              TYPE_I, "THC 18-22%, CBD <0.5%"),
            S("Purple Haze", "Haze landrace selection",
              "Hendrix-famed purpling Haze; berry-spice sativa.",
              ["terpinolene", "pinene", "myrcene", "caryophyllene"],
              TYPE_I, "THC 16-20%, CBD <0.5%"),
            S("Silver Haze", "Haze x Northern Lights",
              "Frosted Haze bridge; sweet-citrus energy.",
              ["terpinolene", "myrcene", "caryophyllene", "pinene"],
              TYPE_I, "THC 18-22%, CBD <0.5%"),
            S("Neville's Haze", "(Haze A x Northern Lights #5) x Haze C",
              "~3/4 Haze; incense-floral flagship sativa.",
              ["terpinolene", "pinene", "caryophyllene"],
              TYPE_I, "THC 20-24%, CBD ~0.15%, trace CBN"),
        ]),
    ]),
    ("Amnesia Group", [
        ("Amnesia", [
            S("Amnesia Haze", "Amnesia x Haze (landrace-backed)",
              "Dutch coffeeshop staple; lemony soaring high.",
              ["myrcene", "terpinolene", "limonene", "caryophyllene"],
              TYPE_I, "THC 20-22%, CBD <0.5%"),
            S("Amnesia", "Skunk x Cinderella 99 x landrace",
              "Original Amnesia; sweet-citrus haze.",
              ["myrcene", "limonene", "terpinolene", "pinene"],
              TYPE_I, "THC 19-22%, CBD <0.5%"),
            S("Amnesia Lemon", "Amnesia Haze x Lemon Skunk",
              "Cannabis Cup lemon-forward haze.",
              ["limonene", "myrcene", "terpinolene", "caryophyllene"],
              TYPE_I, "THC 20-22%, CBD <0.5%"),
            S("NYC Amnesia", "Amnesia phenotype selection",
              "High-yield citrus haze, buzzy and clear.",
              ["myrcene", "limonene", "terpinolene"],
              TYPE_I, "THC 20-24%, CBD <0.5%"),
        ]),
    ]),
    ("Silver & Lemon Haze", [
        ("Silver / Lemon", [
            S("Super Silver Haze", "Haze x Skunk #1 x Northern Lights",
              "Green House three-time Cup champion sativa.",
              ["myrcene", "caryophyllene", "limonene", "terpinolene"],
              TYPE_I, "THC 18-23%, CBD <0.5%"),
            S("Super Lemon Haze", "Lemon Skunk x Super Silver Haze",
              "Zesty lemon-candy haze; lively and bright.",
              ["caryophyllene", "limonene", "terpinolene", "myrcene"],
              TYPE_I, "THC 19-22%, CBD <0.5%"),
            S("Lemon Haze", "Lemon Skunk x Silver Haze",
              "Fresh-peeled lemon sativa, energetic.",
              ["limonene", "terpinolene", "caryophyllene"],
              TYPE_I, "THC 17-21%, CBD <0.5%"),
            S("Silver Pearl", "Early Pearl x Skunk x Northern Lights",
              "Early Haze-Skunk hybrid; sweet and fast.",
              ["myrcene", "terpinolene", "pinene"],
              TYPE_I, "THC 15-19%, CBD <0.5%"),
            S("G13 Haze", "G13 x Haze",
              "Government-legend indica crossed into Haze.",
              ["terpinolene", "myrcene", "caryophyllene", "pinene"],
              TYPE_I, "THC 20-24%, CBD <0.5%"),
        ]),
    ]),
    ("Jack Lineage", [
        ("Jack Family", [
            S("Jack Herer", "Haze x Northern Lights #5 x Shiva Skunk",
              "Sensi's terpinolene icon; pine-spice clarity.",
              ["terpinolene", "caryophyllene", "pinene", "ocimene"],
              TYPE_I, "THC 18-23%, CBD <0.5%"),
            S("Jack Flash", "Jack Herer x (Super Skunk x Haze)",
              "Fast, bright Jack cut; citrus-pepper.",
              ["terpinolene", "myrcene", "caryophyllene"],
              TYPE_I, "THC 18-22%, CBD <0.5%"),
            S("Jack the Ripper", "Jack's Cleaner x Space Queen",
              "Subcool TGA lemon-spice; often THCV-leaning.",
              ["terpinolene", "caryophyllene", "ocimene"],
              THCV, "THC 18-22%, some THCV, CBD <0.5%"),
            S("Jacky White", "Jack Herer x White Widow",
              "Balanced Jack-White hybrid, resinous and clear.",
              ["terpinolene", "myrcene", "caryophyllene"],
              TYPE_I, "THC 18-21%, CBD <0.5%"),
            S("Pineapple Jack", "Jack Herer x Pineapple",
              "Tropical Jack cut; sweet pine-pineapple.",
              ["terpinolene", "ocimene", "myrcene"],
              TYPE_I, "THC 17-21%, CBD <0.5%"),
        ]),
    ]),
    ("Modern Haze Hybrids", [
        ("Sativa Hybrids", [
            S("Kali Mist", "Haze-heavy sativa hybrid",
              "Swirling 'queen of sativas'; sweet-spicy.",
              ["terpinolene", "myrcene", "caryophyllene", "pinene"],
              TYPE_I, "THC 16-20%, CBD <0.5%"),
            S("Blue Dream", "Blueberry x Super Silver Haze",
              "California workhorse; berry-sweet balanced high.",
              ["myrcene", "pinene", "caryophyllene", "limonene"],
              TYPE_I, "THC 17-24%, CBD <0.5%"),
            S("Green Crack", "Skunk #1 sativa phenotype",
              "Sharp mango-citrus energy; daytime classic.",
              ["myrcene", "caryophyllene", "limonene", "pinene"],
              TYPE_I, "THC 16-21%, CBD <0.5%"),
            S("Trainwreck", "Mexican x Thai x Afghani",
              "Lemon-pine freight-train sativa hybrid.",
              ["terpinolene", "myrcene", "pinene", "ocimene"],
              TYPE_I, "THC 18-22%, CBD <0.5%"),
            S("Chocolope", "Chocolate Thai x Cannalope Haze",
              "DNA coffee-melon sativa; dreamy uplift.",
              ["terpinolene", "myrcene", "caryophyllene"],
              TYPE_I, "THC 18-22%, CBD <0.5%"),
            S("Ghost Train Haze", "Ghost OG x Neville's Wreck",
              "Ferociously potent citrus-floral haze.",
              ["terpinolene", "caryophyllene", "limonene", "pinene"],
              TYPE_I, "THC 22-27%, CBD <0.5%"),
            S("Strawberry Cough", "Strawberry Fields x Haze",
              "Sweet-strawberry sativa; expansive and clear.",
              ["myrcene", "pinene", "caryophyllene", "terpinolene"],
              TYPE_I, "THC 16-20%, CBD <0.5%"),
            S("Moby Dick", "White Widow x Haze",
              "Towering, resin-heavy citrus-incense sativa.",
              ["terpinolene", "myrcene", "pinene", "limonene"],
              TYPE_I, "THC 21-27%, CBD <0.5%"),
        ]),
    ]),
    ("Haze Exotics", [
        ("Haze Crosses", [
            S("Haze Berry", "Blueberry x Original Haze",
              "Berry-sweet Haze with jetstream energy.",
              ["myrcene", "terpinolene", "caryophyllene", "pinene"],
              TYPE_I, "THC 18-22%, CBD <0.5%"),
            S("Nebula", "Haze x US skunk hybrid",
              "Starry honey-sweet Haze; heady and warm.",
              ["myrcene", "terpinolene", "limonene"],
              TYPE_I, "THC 16-20%, CBD <0.5%"),
            S("Dr. Grinspoon", "Heirloom sativa (Haze-type)",
              "Beaded heirloom sativa; rare, purely cerebral.",
              ["terpinolene", "pinene", "myrcene"],
              TYPE_I, "THC 16-20%, CBD <0.5%"),
            S("Arjan's Haze", "Haze x (Skunk / Northern Lights)",
              "Green House named Haze; sweet-spicy and tall.",
              ["terpinolene", "myrcene", "caryophyllene"],
              TYPE_I, "THC 19-23%, CBD <0.5%"),
        ]),
    ]),
]),

# ==========================================================================
# CLADE D - SKUNK LINEAGE
# ==========================================================================
("Skunk Lineage", [
    ("Skunk Core", [
        ("Skunk #1 Family", [
            S("Skunk #1", "Afghani x Acapulco Gold x Colombian Gold",
              "The stabilized hybrid that anchors modern breeding.",
              ["myrcene", "caryophyllene", "limonene", "humulene"],
              TYPE_I, "THC 15-19%, CBD <0.5%"),
            S("Roadkill Skunk", "Original pungent Skunk phenotype",
              "Notoriously loud sulphur-skunk classic.",
              ["myrcene", "caryophyllene", "humulene"],
              TYPE_I, "THC 14-18%, CBD <0.5%"),
            S("Super Skunk", "Skunk #1 x Afghani",
              "Beefed-up Skunk; sweeter, heavier resin.",
              ["myrcene", "caryophyllene", "limonene"],
              TYPE_I, "THC 15-20%, CBD <0.5%"),
            S("Island Sweet Skunk", "Skunk #1 (Sweet Skunk) selection",
              "Tropical grapefruit-skunk sativa lean.",
              ["myrcene", "terpinolene", "caryophyllene"],
              TYPE_I, "THC 16-20%, CBD <0.5%"),
            S("Sweet Skunk", "Skunk #1 phenotype",
              "Candy-sweet Skunk expression; smooth.",
              ["myrcene", "limonene", "caryophyllene"],
              TYPE_I, "THC 14-18%, CBD <0.5%"),
        ]),
    ]),
    ("Early Bloomers", [
        ("Early Outdoor", [
            S("Early Pearl", "Pollyanna (Colombian x Mexican) x Early Girl",
              "Sensi's early-outdoor sativa; sweet-piney and hardy.",
              ["myrcene", "caryophyllene", "pinene"],
              TYPE_I, "THC 12-16%, CBD <0.5%"),
            S("Early Skunk", "Skunk #1 x Early Pearl",
              "Mold-resistant, fast outdoor Skunk hybrid.",
              ["myrcene", "caryophyllene", "pinene", "limonene"],
              TYPE_I, "THC 13-17%, CBD <0.5%"),
            S("Early Girl", "Afghani-heavy early indica hybrid",
              "Reliable quick outdoor indica; earthy-sweet.",
              ["myrcene", "caryophyllene", "pinene"],
              TYPE_I, "THC 12-17%, CBD <0.5%"),
            S("Early Misty", "Early indica-skunk hybrid",
              "Compact, fast, sweet indica for short seasons.",
              ["myrcene", "pinene", "caryophyllene"],
              TYPE_I, "THC 13-17%, CBD <0.5%"),
        ]),
    ]),
    ("Cheese Family", [
        ("Cheese", [
            S("Cheese", "Skunk #1 phenotype (UK Exodus cut)",
              "Pungent sour-dairy UK Skunk cut; the Cheese origin.",
              ["myrcene", "caryophyllene", "pinene", "humulene"],
              TYPE_I, "THC 15-20%, CBD <0.5%"),
            S("Blue Cheese", "UK Cheese x Blueberry",
              "Savory cheese meets sweet blueberry; relaxing.",
              ["myrcene", "caryophyllene", "limonene", "linalool"],
              TYPE_I, "THC 15-20%, CBD <0.5%"),
            S("Exodus Cheese", "Original Exodus Skunk cut",
              "The clone-only UK Cheese progenitor.",
              ["myrcene", "caryophyllene", "humulene"],
              TYPE_I, "THC 15-18%, CBD <0.5%"),
            S("Big Buddha Cheese", "Exodus Cheese x Afghani",
              "Seed-stable Cheese; funky and full-bodied.",
              ["myrcene", "caryophyllene", "pinene"],
              TYPE_I, "THC 15-19%, CBD <0.5%"),
        ]),
    ]),
    ("White Family", [
        ("Widow / White", [
            S("White Widow", "Brazilian sativa x South Indian indica",
              "Frost-caked balanced hybrid; a 1990s legend.",
              ["myrcene", "caryophyllene", "pinene", "humulene"],
              TYPE_I, "THC 15-25%, CBD <1%"),
            S("White Rhino", "White Widow x North American indica",
              "Heavier White cut; dense and sedating.",
              ["myrcene", "caryophyllene", "limonene"],
              TYPE_I, "THC 18-22%, CBD <1%"),
            S("White Russian", "White Widow x AK-47",
              "Ultra-frosty potent hybrid; earthy-sweet.",
              ["myrcene", "caryophyllene", "pinene"],
              TYPE_I, "THC 18-22%, CBD <1%"),
            S("Great White Shark", "White Widow x Super Skunk-Brazilian",
              "Resin-drenched 'Peacemaker'; earthy and calm.",
              ["myrcene", "caryophyllene", "humulene", "pinene"],
              TYPE_I, "THC 18-21%, CBD <1%"),
            S("Blue Widow", "White Widow x Blueberry",
              "Berry-frost hybrid; balanced and mellow.",
              ["myrcene", "caryophyllene", "linalool"],
              TYPE_I, "THC 16-20%, CBD <1%"),
            S("The White", "Clone-only (unknown, White-type)",
              "Nearly odorless, trichome-blanketed OG relative.",
              ["caryophyllene", "myrcene", "limonene"],
              TYPE_I, "THC 22-28%, CBD <1%"),
        ]),
    ]),
    ("Northern Indica-Skunk", [
        ("Northern Lights", [
            S("Northern Lights", "Afghani x Thai",
              "Resin-heavy indica cornerstone; sweet and calming.",
              ["myrcene", "pinene", "caryophyllene"],
              TYPE_I, "THC 16-21%, CBD <0.5%"),
            S("Northern Lights #5", "Northern Lights selection",
              "The elite NL cut behind Haze/Skunk hybrids.",
              ["myrcene", "caryophyllene", "pinene"],
              TYPE_I, "THC 16-21%, CBD <0.5%"),
            S("Shiva Skunk", "Northern Lights #5 x Skunk #1",
              "Heavy resinous indica-skunk; sweet-pungent.",
              ["myrcene", "caryophyllene", "limonene"],
              TYPE_I, "THC 18-21%, CBD <0.5%"),
            S("Sensi Skunk", "Skunk #1 x Afghani-indica",
              "Easy, forgiving Skunk hybrid; sweet-earthy.",
              ["myrcene", "caryophyllene", "pinene"],
              TYPE_I, "THC 14-18%, CBD <0.5%"),
            S("Hash Plant Skunk", "Hash Plant x Skunk #1",
              "Fast, resin-drenched indica-skunk.",
              ["myrcene", "humulene", "caryophyllene"],
              TYPE_I, "THC 15-19%, CBD <0.5%"),
        ]),
    ]),
    ("Fruity Skunk Hybrids", [
        ("Sweet Skunk Hybrids", [
            S("Cinderella 99", "Jack Herer x Shiva Skunk (Princess)",
              "Brothers Grimm pineapple-citrus sativa dream.",
              ["terpinolene", "myrcene", "limonene", "caryophyllene"],
              TYPE_I, "THC 18-22%, CBD <0.5%"),
            S("Orange Bud", "Skunk #1 selection",
              "Sweet orange-citrus Skunk classic.",
              ["myrcene", "limonene", "caryophyllene"],
              TYPE_I, "THC 15-19%, CBD <0.5%"),
            S("Lemon Skunk", "Skunk #1 lemon phenotypes",
              "Bright lemon-zest Skunk; lively and sweet.",
              ["limonene", "myrcene", "caryophyllene"],
              TYPE_I, "THC 16-22%, CBD <0.5%"),
            S("AK-47", "Colombian x Mexican x Thai x Afghani",
              "One-hit sativa-leaning hybrid; floral-earthy.",
              ["myrcene", "caryophyllene", "limonene", "pinene"],
              TYPE_I, "THC 18-22%, CBD <0.5%"),
            S("Pineapple Express", "Trainwreck x Hawaiian",
              "Tropical pineapple-cedar hybrid; buoyant.",
              ["myrcene", "caryophyllene", "pinene", "limonene"],
              TYPE_I, "THC 17-24%, CBD <0.5%"),
        ]),
    ]),
]),

# ==========================================================================
# CLADE E - KUSH / OG LINEAGE
# ==========================================================================
("Kush / OG Lineage", [
    ("OG Kush Core", [
        ("OG Kush & Cuts", [
            S("OG Kush", "Chemdawg x (Lemon Thai x Hindu Kush)",
              "West Coast foundation cut; gassy-lemon-pine.",
              ["caryophyllene", "limonene", "myrcene", "linalool"],
              TYPE_I, "THC 19-26%, CBD <1%"),
            S("SFV OG", "OG Kush cut x Afghani",
              "San Fernando Valley OG; piney-fuel and bright.",
              ["myrcene", "limonene", "caryophyllene", "pinene"],
              TYPE_I, "THC 17-25%, CBD <0.5%"),
            S("Tahoe OG", "OG Kush phenotype (Tahoe cut)",
              "Heavy, fast-finishing sedative nighttime OG.",
              ["limonene", "caryophyllene", "myrcene", "pinene"],
              TYPE_I, "THC 20-25%, CBD <1%"),
            S("Larry OG", "OG Kush phenotype (SFV-related)",
              "Lemon-pine OG cut; happy and relaxing.",
              ["myrcene", "limonene", "caryophyllene"],
              TYPE_I, "THC 20-25%, CBD <1%"),
            S("Ghost OG", "OG Kush phenotype",
              "Ethereal balanced OG; citrus-pine and potent.",
              ["myrcene", "limonene", "caryophyllene", "humulene"],
              TYPE_I, "THC 20-25%, CBD <1%"),
            S("Fire OG", "OG Kush x SFV OG",
              "Red-haired, potent OG; lemon-fuel and heavy.",
              ["limonene", "caryophyllene", "myrcene", "linalool"],
              TYPE_I, "THC 20-25%, CBD <1%"),
            S("Triangle Kush", "Florida OG Kush cut",
              "Florida OG progenitor; earthy-lemon and dank.",
              ["caryophyllene", "limonene", "myrcene", "humulene"],
              TYPE_I, "THC 20-24%, CBD <1%"),
        ]),
    ]),
    ("LA & Louis Cuts", [
        ("LA / Louis OG", [
            S("Louis XIII", "OG Kush x LA Confidential (LA OG cut)",
              "King Louis XIII; regal pine-earth sedative OG.",
              ["myrcene", "limonene", "caryophyllene", "pinene"],
              TYPE_I, "THC 21-29%, CBD <1%"),
            S("LA OG", "OG Kush x Afghani (LA cut)",
              "Los Angeles OG; kushy-fuel and stony.",
              ["myrcene", "limonene", "caryophyllene"],
              TYPE_I, "THC 18-24%, CBD <1%"),
            S("Alien OG", "Tahoe OG x Alien Kush",
              "Lemon-pine OG with dreamy, dizzy potency.",
              ["myrcene", "limonene", "caryophyllene"],
              TYPE_I, "THC 20-28%, CBD <1%"),
            S("Skywalker OG", "Skywalker (Blueberry x Mazar) x OG Kush",
              "Spicy-fuel OG with a berry undertone; heavy.",
              ["caryophyllene", "limonene", "myrcene", "linalool"],
              TYPE_I, "THC 20-26%, CBD <1%"),
        ]),
    ]),
    ("Bubba & Pre-98", [
        ("Bubba Family", [
            S("Bubba Kush", "OG Kush x Afghani-indica (clone-only)",
              "Coffee-chocolate heavy indica; tranquilizing.",
              ["caryophyllene", "myrcene", "limonene", "humulene"],
              TYPE_I, "THC 15-22%, CBD <1%"),
            S("Pre-98 Bubba Kush", "Original 1998 Bubba cut",
              "The benchmark Bubba; hashy-cocoa and sedative.",
              ["caryophyllene", "myrcene", "limonene"],
              TYPE_I, "THC 16-22%, CBD <1%"),
            S("Katsu Bubba Kush", "Bubba Kush phenotype (Katsu cut)",
              "Refined Bubba cut; earthy-sweet couch-lock.",
              ["caryophyllene", "myrcene", "linalool"],
              TYPE_I, "THC 16-21%, CBD <1%"),
            S("Master Yoda", "Master Kush x OG Kush",
              "Dense, resinous OG-Kush indica; earthy-piney.",
              ["myrcene", "caryophyllene", "limonene"],
              TYPE_I, "THC 18-23%, CBD <1%"),
        ]),
    ]),
    ("Kush Classics", [
        ("Afghani-Kush", [
            S("Master Kush", "Hindu Kush x Skunk #1",
              "Sensi incense-earth indica; smooth and calm.",
              ["myrcene", "caryophyllene", "limonene", "bisabolol"],
              TYPE_I, "THC 16-24%, CBD <0.5%"),
            S("Purple Kush", "Hindu Kush x Purple Afghani",
              "Pure indica; grape-earth and deeply sedative.",
              ["myrcene", "pinene", "caryophyllene", "linalool"],
              TYPE_I, "THC 17-22%, CBD <1%"),
            S("Kosher Kush", "OG Kush elite phenotype",
              "Blessed OG cut; rich earthy-fruit and heavy.",
              ["myrcene", "limonene", "caryophyllene", "linalool"],
              TYPE_I, "THC 20-25%, CBD <1%"),
            S("Critical Kush", "Critical Mass x OG Kush",
              "High-yield sedative kush; earthy-spice.",
              ["myrcene", "caryophyllene", "limonene"],
              TYPE_I, "THC 20-25%, CBD <1%"),
            S("Nepali OG", "Nepali indica x OG Kush",
              "Hash-plant OG hybrid; spicy sandalwood.",
              ["myrcene", "caryophyllene", "humulene"],
              TYPE_I, "THC 18-23%, CBD <1%"),
        ]),
    ]),
    ("Modern OG Hybrids", [
        ("OG Crosses", [
            S("Headband", "OG Kush x Sour Diesel",
              "Pressure-around-the-head hybrid; lemon-diesel.",
              ["caryophyllene", "limonene", "myrcene", "humulene"],
              TYPE_I, "THC 20-27%, CBD <1%"),
            S("White Fire OG", "Fire OG x The White",
              "WiFi; frosty gas-citrus, bright and heady.",
              ["caryophyllene", "limonene", "myrcene"],
              TYPE_I, "THC 22-28%, CBD <1%"),
            S("Platinum OG", "OG Kush x Master Kush x unknown",
              "Silvery, heavy OG; earthy-fuel sedation.",
              ["myrcene", "caryophyllene", "limonene"],
              TYPE_I, "THC 20-24%, CBD <1%"),
            S("God's Gift", "Granddaddy Purple x OG Kush",
              "Grape-berry OG indica; dreamy and heavy.",
              ["myrcene", "caryophyllene", "linalool", "pinene"],
              TYPE_I, "THC 18-22%, CBD <1%"),
            S("True OG", "OG Kush phenotype",
              "Award-winning kush cut; lemon-pine-earth.",
              ["myrcene", "limonene", "caryophyllene"],
              TYPE_I, "THC 20-25%, CBD <1%"),
            S("Face Off OG", "OG Kush cut (Archive)",
              "Foundational modern OG parent; gassy-earthy.",
              ["caryophyllene", "myrcene", "limonene"],
              TYPE_I, "THC 20-26%, CBD <1%"),
        ]),
    ]),
    ("Kush x Fruit", [
        ("Fruity Kush", [
            S("Banana Kush", "Ghost OG x Skunk Haze",
              "Creamy banana-tropical OG hybrid; mellow.",
              ["limonene", "myrcene", "caryophyllene"],
              TYPE_I, "THC 18-25%, CBD <1%"),
            S("Mango Kush", "Kush x Mango-Skunk selection",
              "Sweet mango indica; relaxed and giggly.",
              ["myrcene", "caryophyllene", "limonene"],
              TYPE_I, "THC 15-20%, CBD <1%"),
            S("Blueberry Kush", "Blueberry x OG Kush",
              "Berry-fuel indica; sweet and sedating.",
              ["myrcene", "caryophyllene", "linalool", "pinene"],
              TYPE_I, "THC 18-24%, CBD <1%"),
            S("Cherry OG", "Cherry Thai x Lost Coast OG",
              "Sweet-tart cherry OG; balanced and bright.",
              ["myrcene", "limonene", "caryophyllene"],
              TYPE_I, "THC 20-24%, CBD <1%"),
        ]),
    ]),
]),

# ==========================================================================
# CLADE F - DIESEL / CHEM LINEAGE
# ==========================================================================
("Diesel / Chem Lineage", [
    ("Chemdawg Core", [
        ("Chem Cuts", [
            S("Chemdawg", "Unknown Thai/Nepali sativa cross (clone-only)",
              "The mysterious fuel cut behind OG and Diesel.",
              ["caryophyllene", "limonene", "myrcene", "humulene"],
              TYPE_I, "THC 18-25%, CBD <1%"),
            S("Chem 91", "Chemdawg phenotype (1991 cut)",
              "Sharp, sour-fuel Chem selection; pungent.",
              ["caryophyllene", "myrcene", "limonene"],
              TYPE_I, "THC 18-24%, CBD <1%"),
            S("Chem D", "Chemdawg phenotype (D cut)",
              "Acrid diesel Chem; a GMO/Cookies-era parent.",
              ["caryophyllene", "limonene", "humulene"],
              TYPE_I, "THC 19-25%, CBD <1%"),
            S("Chem 4", "Chemdawg phenotype (4 cut)",
              "Robust fuel-pine Chem cut; Stardawg parent.",
              ["caryophyllene", "myrcene", "limonene"],
              TYPE_I, "THC 19-25%, CBD <1%"),
            S("Chem Sister", "Chemdawg phenotype (sister cut)",
              "Bright, sativa-leaning Chem selection.",
              ["caryophyllene", "limonene", "pinene"],
              TYPE_I, "THC 18-24%, CBD <1%"),
            S("Tres Dawg", "Chemdawg x (Afghani #1)",
              "Stabilized Chem line; heavy fuel and earth.",
              ["caryophyllene", "myrcene", "humulene"],
              TYPE_I, "THC 18-24%, CBD <1%"),
        ]),
    ]),
    ("Sour Diesel Group", [
        ("Sour Family", [
            S("Sour Diesel", "Chemdawg 91 x Super Skunk",
              "East Coast diesel legend; pungent citrus-fuel.",
              ["caryophyllene", "limonene", "myrcene", "pinene"],
              TYPE_I, "THC 18-26%, CBD <1%"),
            S("NYC Diesel", "Sour Diesel x Afghani-Hawaiian",
              "Ruby-grapefruit diesel; lively and aromatic.",
              ["myrcene", "limonene", "caryophyllene", "pinene"],
              TYPE_I, "THC 18-23%, CBD <1%"),
            S("Super Sour Diesel", "Sour Diesel x (Sour x NYC)",
              "Turbocharged sour-fuel sativa; racy.",
              ["caryophyllene", "limonene", "terpinolene"],
              TYPE_I, "THC 20-25%, CBD <1%"),
            S("Sour OG", "Sour Diesel x OG Kush",
              "Fuel-meets-kush hybrid; balanced and dank.",
              ["caryophyllene", "limonene", "myrcene"],
              TYPE_I, "THC 20-25%, CBD <1%"),
            S("East Coast Sour Diesel", "Sour Diesel elite cut",
              "The definitive ECSD; sharp lemon-fuel.",
              ["caryophyllene", "limonene", "myrcene"],
              TYPE_I, "THC 19-24%, CBD <1%"),
            S("Strawberry Diesel", "Strawberry Cough x Sour Diesel",
              "Sweet-berry diesel; bright and buzzy.",
              ["caryophyllene", "myrcene", "limonene"],
              TYPE_I, "THC 18-22%, CBD <1%"),
        ]),
    ]),
    ("Glue Family", [
        ("Gorilla Glue", [
            S("Gorilla Glue #4", "Chem's Sister x Sour Dubb x Chocolate Diesel",
              "GG4 / Original Glue; ultra-sticky chocolate-diesel powerhouse.",
              ["caryophyllene", "myrcene", "limonene", "humulene"],
              TYPE_I, "THC 24-30%, CBD <1%"),
            S("Gorilla Glue #1", "Sister Glue phenotype",
              "The GG sister cut; sour-earth and heavy.",
              ["caryophyllene", "myrcene", "limonene"],
              TYPE_I, "THC 22-28%, CBD <1%"),
            S("New Glue (GG5)", "Sister Glue x Gorilla Glue #4",
              "Refined Glue; fuel-cocoa and adhesive resin.",
              ["caryophyllene", "limonene", "humulene"],
              TYPE_I, "THC 24-30%, CBD <1%"),
        ]),
    ]),
    ("Diesel Hybrids", [
        ("Modern Diesel", [
            S("Stardawg", "Chemdawg #4 x Tres Dawg",
              "Glittering fuel-pine Chem hybrid; sharp.",
              ["caryophyllene", "myrcene", "limonene", "pinene"],
              TYPE_I, "THC 20-25%, CBD <1%"),
            S("i-95", "Chem D x (Legend OG x Triangle Kush)",
              "Dense, gassy Chem-OG hybrid; heavy-hitting.",
              ["caryophyllene", "limonene", "myrcene"],
              TYPE_I, "THC 25-30%, CBD <1%"),
            S("Chemdog Millionaire", "Chemdawg x Sour Diesel-line",
              "Loud fuel-citrus Chem cross; potent.",
              ["caryophyllene", "limonene", "humulene"],
              TYPE_I, "THC 20-25%, CBD <1%"),
            S("Turbo Diesel", "Sour Diesel x indica hybrid",
              "Fuel-forward hybrid; fast and pungent.",
              ["caryophyllene", "myrcene", "limonene"],
              TYPE_I, "THC 18-23%, CBD <1%"),
        ]),
    ]),
]),

# ==========================================================================
# CLADE G - COOKIES / DESSERT LINEAGE
# ==========================================================================
("Cookies / Dessert Lineage", [
    ("GSC Core", [
        ("Girl Scout Cookies", [
            S("GSC", "OG Kush x Durban Poison (F1 Durb)",
              "Girl Scout Cookies; sweet-earth dessert cornerstone.",
              ["caryophyllene", "limonene", "humulene", "linalool"],
              TYPE_I, "THC 19-28%, CBD <1%"),
            S("Thin Mint GSC", "GSC phenotype (Thin Mint cut)",
              "Minty, frosty Cookies cut; balanced and heady.",
              ["caryophyllene", "limonene", "humulene"],
              TYPE_I, "THC 19-25%, CBD <1%"),
            S("Platinum GSC", "GSC phenotype (Platinum cut)",
              "Silvery, sweet-berry Cookies; potent and calm.",
              ["caryophyllene", "limonene", "linalool"],
              TYPE_I, "THC 18-24%, CBD <1%"),
            S("Forum Cut Cookies", "GSC elite phenotype (Forum)",
              "The exotic Cookies parent behind Gelato/Cake.",
              ["caryophyllene", "limonene", "humulene", "linalool"],
              TYPE_I, "THC 20-26%, CBD <1%"),
            S("Animal Cookies", "GSC x Fire OG",
              "Heavy, sweet-sour Cookies indica; sedating.",
              ["caryophyllene", "limonene", "linalool", "myrcene"],
              TYPE_I, "THC 20-27%, CBD <1%"),
        ]),
    ]),
    ("Cherry & Sherbet", [
        ("Cherry / Sherbet", [
            S("Cherry Pie", "Granddaddy Purple x Durban Poison",
              "Sweet-tart cherry dessert; a Sherbet/Cake parent.",
              ["myrcene", "caryophyllene", "limonene", "pinene"],
              TYPE_I, "THC 16-24%, CBD <1%"),
            S("Sunset Sherbet", "GSC x Pink Panties",
              "Creamy citrus-berry Cookies; the Gelato mother.",
              ["caryophyllene", "limonene", "linalool", "myrcene"],
              TYPE_I, "THC 18-24%, CBD <1%"),
            S("Pink Cookies", "Cherry Pie x GSC (Wedding Cake alt)",
              "Sweet-doughy Cookies hybrid; relaxing.",
              ["caryophyllene", "limonene", "linalool"],
              TYPE_I, "THC 20-25%, CBD <1%"),
            S("Cherry Cookies", "Cherry Pie x GSC",
              "Fruit-forward Cookies; sweet and mellow.",
              ["caryophyllene", "myrcene", "limonene"],
              TYPE_I, "THC 18-23%, CBD <1%"),
        ]),
    ]),
    ("Gelato Family", [
        ("Gelato", [
            S("Gelato", "Sunset Sherbet x Thin Mint GSC",
              "Gelato #33; dessert-sweet, creamy-citrus balance.",
              ["caryophyllene", "limonene", "linalool", "myrcene"],
              TYPE_I, "THC 20-26%, CBD <1%"),
            S("Gelato #41", "Sunset Sherbet x Thin Mint GSC (#41)",
              "Bacio-parent Gelato cut; sweet-lavender fuel.",
              ["caryophyllene", "limonene", "humulene", "linalool"],
              TYPE_I, "THC 20-26%, CBD <1%"),
            S("Bacio Gelato", "Sunset Sherbet x Thin Mint GSC (Bacio)",
              "Rich, gassy dessert Gelato; Grandiflora line.",
              ["caryophyllene", "limonene", "linalool"],
              TYPE_I, "THC 22-28%, CBD <1%"),
            S("Mochi Gelato", "Sunset Sherbet x Thin Mint GSC (Mochi)",
              "Sweet-mint creamy Gelato; balanced and heady.",
              ["caryophyllene", "limonene", "myrcene"],
              TYPE_I, "THC 20-25%, CBD <1%"),
        ]),
    ]),
    ("Exotic Cookies", [
        ("Biscotti / Runtz", [
            S("Biscotti", "Gelato #25 x South Florida OG",
              "Cookies-fuel dessert; sweet, spicy, sedative.",
              ["caryophyllene", "limonene", "linalool", "humulene"],
              TYPE_I, "THC 21-25%, CBD <1%"),
            S("RS-11", "OZK x Sunset Sherbet (Rntz Sundae #11)",
              "Rainbow Sherbet 11; creamy-fruit exotic Cookies.",
              ["limonene", "caryophyllene", "linalool", "myrcene"],
              TYPE_I, "THC 22-30%, CBD <1%"),
            S("Runtz", "Zkittlez x Gelato",
              "Candy-sweet dessert hybrid; smooth and euphoric.",
              ["caryophyllene", "limonene", "linalool"],
              TYPE_I, "THC 19-29%, CBD <1%"),
            S("White Runtz", "Zkittlez x Gelato (white pheno)",
              "Frosty, creamy-candy Runtz cut; balanced.",
              ["limonene", "caryophyllene", "linalool"],
              TYPE_I, "THC 23-29%, CBD <1%"),
            S("Pink Runtz", "Runtz phenotype (pink)",
              "Sweet-tart candy Runtz; happy and calm.",
              ["limonene", "caryophyllene", "myrcene"],
              TYPE_I, "THC 22-28%, CBD <1%"),
            S("Jealousy", "Gelato #41 x Sherbet BX1",
              "Creamy-funk exotic; smooth, potent, modern.",
              ["caryophyllene", "limonene", "linalool"],
              TYPE_I, "THC 23-27%, CBD <1%"),
            S("Gelonade", "Lemon Tree x Gelato #41",
              "Zesty lemon dessert Gelato; bright and rich.",
              ["limonene", "caryophyllene", "myrcene"],
              TYPE_I, "THC 22-27%, CBD <1%"),
        ]),
    ]),
    ("Cake Family", [
        ("Wedding Cake", [
            S("Wedding Cake", "Triangle Kush x Animal Mints",
              "Tangy-sweet vanilla dessert indica; rich.",
              ["caryophyllene", "limonene", "myrcene", "linalool"],
              TYPE_I, "THC 22-27%, CBD <1%"),
            S("Ice Cream Cake", "Wedding Cake x Gelato #33",
              "Creamy vanilla-nut indica; heavy and sweet.",
              ["caryophyllene", "limonene", "linalool"],
              TYPE_I, "THC 20-25%, CBD <1%"),
            S("Birthday Cake", "GSC x Cherry Pie",
              "Sweet vanilla Cookies; relaxing and mellow.",
              ["caryophyllene", "limonene", "linalool"],
              TYPE_I, "THC 20-24%, CBD <1%"),
            S("Wedding Crasher", "Wedding Cake x Purple Punch",
              "Grape-vanilla dessert hybrid; uplifting.",
              ["caryophyllene", "limonene", "myrcene"],
              TYPE_I, "THC 18-24%, CBD <1%"),
            S("Kush Mints", "Bubba Kush x Animal Mints",
              "Minty-cookie kush; potent, balanced, cool.",
              ["caryophyllene", "limonene", "linalool", "humulene"],
              TYPE_I, "THC 22-27%, CBD <1%"),
        ]),
    ]),
    ("Garlic / Chem Cookies", [
        ("GMO Family", [
            S("GMO", "Chemdawg x GSC (Garlic Cookies)",
              "GMO / Garlic Cookies; savory garlic-fuel funk.",
              ["caryophyllene", "limonene", "humulene", "myrcene"],
              TYPE_I, "THC 22-30%, CBD <1%"),
            S("Garlic Breath", "GMO phenotype selection",
              "Pungent garlic-earth Cookies-Chem; heavy.",
              ["caryophyllene", "limonene", "humulene"],
              TYPE_I, "THC 20-27%, CBD <1%"),
            S("Motorbreath", "Chemdawg x SFV OG Kush",
              "Diesel-garlic OG-Chem; acrid and potent.",
              ["caryophyllene", "limonene", "myrcene"],
              TYPE_I, "THC 22-28%, CBD <1%"),
            S("MAC", "Alien Cookies x (Colombian x Starfighter)",
              "Miracle Alien Cookies; creamy-citrus and floral.",
              ["limonene", "caryophyllene", "pinene", "linalool"],
              TYPE_I, "THC 20-26%, CBD <1%"),
        ]),
    ]),
    ("Cookies x OG & Modern", [
        ("Dosi / Mints", [
            S("Do-Si-Dos", "OGKB (GSC) x Face Off OG",
              "Sweet-earthy Cookies indica; frosty and heavy.",
              ["limonene", "caryophyllene", "linalool", "myrcene"],
              TYPE_I, "THC 21-30%, CBD <1%"),
            S("OGKB", "GSC phenotype (OG Kush Breath)",
              "Foundational Cookies indica cut; earthy-sweet.",
              ["caryophyllene", "limonene", "linalool"],
              TYPE_I, "THC 20-26%, CBD <1%"),
            S("Animal Mints", "GSC x (Fire OG x Blue Power)",
              "Minty, gassy Cookies; the Wedding Cake parent.",
              ["caryophyllene", "limonene", "linalool"],
              TYPE_I, "THC 22-28%, CBD <1%"),
            S("Gushers", "Gelato #41 x Triangle Kush (Fruit Gushers)",
              "Sweet-sour tropical Cookies; balanced.",
              ["caryophyllene", "limonene", "myrcene"],
              TYPE_I, "THC 20-25%, CBD <1%"),
            S("Sunday Driver", "Fruity Pebbles OG x Grape Pie",
              "Grape-cream dessert hybrid; smooth and calm.",
              ["caryophyllene", "limonene", "linalool", "myrcene"],
              TYPE_I, "THC 18-24%, CBD <1%"),
            S("Georgia Pie", "Gelatti x Kush Mints",
              "Peach-cobbler sweet Cookies; rich and relaxed.",
              ["caryophyllene", "limonene", "linalool"],
              TYPE_I, "THC 22-28%, CBD <1%"),
            S("Cereal Milk", "Y Life (GSC x Cherry Pie) x Snowman",
              "Sweet, creamy-milk Cookies; smooth balance.",
              ["caryophyllene", "limonene", "myrcene"],
              TYPE_I, "THC 18-23%, CBD <1%"),
            S("Lemon Cherry Gelato", "Sunset Sherbet x GSC x Gelato",
              "Citrus-cherry dessert; a modern menu darling.",
              ["limonene", "caryophyllene", "linalool"],
              TYPE_I, "THC 22-28%, CBD <1%"),
        ]),
    ]),
]),

# ==========================================================================
# CLADE H - PURPLE / GRAPE & BERRY INDICA
# ==========================================================================
("Purple / Grape & Berry Indica", [
    ("Purple (GDP) Family", [
        ("Granddaddy Purple", [
            S("Granddaddy Purple", "Purple Urkle x Big Bud",
              "Ken Estes GDP; grape-berry heavy sedative indica.",
              ["myrcene", "caryophyllene", "pinene", "linalool"],
              TYPE_I, "THC 17-23%, CBD <1%"),
            S("Purple Urkle", "Mendocino Purps phenotype",
              "Grape-skunk California indica; sleepy and rich.",
              ["myrcene", "caryophyllene", "linalool", "pinene"],
              TYPE_I, "THC 18-22%, CBD <1%"),
            S("Grape Ape", "Mendo Purps x Skunk x Afghani",
              "Grape-candy indica; relaxing and full-bodied.",
              ["myrcene", "caryophyllene", "pinene"],
              TYPE_I, "THC 15-23%, CBD <1%"),
            S("Purple Punch", "Larry OG x Granddaddy Purple",
              "Grape-Kool-Aid dessert indica; sweet and sedating.",
              ["caryophyllene", "limonene", "pinene", "myrcene"],
              TYPE_I, "THC 18-25%, CBD <1%"),
            S("Mendo Purps", "Mendocino landrace-purple selection",
              "Northern California purple heirloom; grape-earth.",
              ["myrcene", "pinene", "caryophyllene"],
              TYPE_I, "THC 16-21%, CBD <1%"),
        ]),
    ]),
    ("Dark Indica", [
        ("Black / Domina", [
            S("Black Domina", "Northern Lights x Ortega x Hash Plant x Afghani",
              "Sensi four-way indica; blackberry-pepper narcotic.",
              ["myrcene", "caryophyllene", "limonene"],
              TYPE_I, "THC 18-24%, CBD <1%"),
            S("Blackberry", "Black Domina x Raspberry Cough",
              "Sweet-tart berry indica hybrid; relaxing.",
              ["myrcene", "caryophyllene", "pinene"],
              TYPE_I, "THC 16-20%, CBD <1%"),
            S("Blackwater", "Mendo Purps x SFV OG Kush",
              "Purple grape-fuel indica; deeply calming.",
              ["myrcene", "caryophyllene", "linalool"],
              TYPE_I, "THC 18-22%, CBD <1%"),
            S("Black Cherry Soda", "Unknown purple indica-hybrid",
              "Tart cherry-berry purple; balanced and mellow.",
              ["myrcene", "caryophyllene", "pinene"],
              TYPE_I, "THC 16-20%, CBD <1%"),
        ]),
    ]),
    ("Berry / Blueberry", [
        ("DJ Short Berry", [
            S("Blueberry", "Thai x Afghani x Purple Thai (DJ Short)",
              "Legendary sweet-blueberry indica; euphoric-calm.",
              ["myrcene", "pinene", "caryophyllene", "limonene"],
              TYPE_I, "THC 16-24%, CBD <1%"),
            S("Blueberry Muffin", "Blueberry x Purple Panty Dropper",
              "Baked-blueberry sweet indica; happy and relaxed.",
              ["myrcene", "caryophyllene", "pinene"],
              TYPE_I, "THC 16-21%, CBD <1%"),
            S("Blue Cookies", "Blueberry x GSC",
              "Berry-cookie hybrid; sweet and euphoric.",
              ["caryophyllene", "myrcene", "limonene", "linalool"],
              TYPE_I, "THC 20-25%, CBD <1%"),
            S("Blue Zkittlez", "Blue Diamond x Zkittlez",
              "Berry-candy hybrid; fruity and soothing.",
              ["caryophyllene", "linalool", "humulene", "myrcene"],
              TYPE_I, "THC 19-23%, CBD <1%"),
        ]),
    ]),
    ("Candy Fruit", [
        ("Zkittlez / Candy", [
            S("Zkittlez", "Grape Ape x Grapefruit x unknown",
              "Rainbow-candy indica; tropical-berry and calm.",
              ["caryophyllene", "humulene", "linalool", "limonene"],
              TYPE_I, "THC 15-23%, CBD <1%"),
            S("Watermelon Zkittlez", "Zkittlez x Watermelon",
              "Sweet watermelon-candy indica; mellow.",
              ["caryophyllene", "linalool", "myrcene"],
              TYPE_I, "THC 18-23%, CBD <1%"),
            S("Fruity Pebbles OG", "Green Ribbon x Granddaddy Purple x Tahoe",
              "FPOG; sweet cereal-fruit hybrid; euphoric.",
              ["caryophyllene", "limonene", "myrcene"],
              TYPE_I, "THC 18-24%, CBD <1%"),
            S("Grape Gasoline", "Jet Fuel Gelato x Grape Pie",
              "Grape-diesel exotic; pungent-sweet and potent.",
              ["caryophyllene", "limonene", "myrcene"],
              TYPE_I, "THC 22-28%, CBD <1%"),
            S("Zoap", "Rainbow Sherbet x Pink Guava",
              "Soapy-floral candy exotic; balanced and heavy.",
              ["limonene", "caryophyllene", "linalool"],
              TYPE_I, "THC 22-28%, CBD <1%"),
        ]),
    ]),
    ("Grape / Wine", [
        ("Grape", [
            S("Grape Stomper", "Chemdawg Sour Diesel x Purple Elephant",
              "Sweet grape-candy sativa lean; bright and giddy.",
              ["caryophyllene", "myrcene", "limonene"],
              TYPE_I, "THC 18-24%, CBD <1%"),
            S("Grape Pie", "Cherry Pie x Grape Stomper",
              "Grape-berry dessert; a Sunday Driver parent.",
              ["myrcene", "caryophyllene", "limonene"],
              TYPE_I, "THC 18-22%, CBD <1%"),
            S("Sour Grapes", "Granddaddy Purple x Sour Diesel",
              "Grape-fuel hybrid; sweet, sour, and calming.",
              ["myrcene", "caryophyllene", "limonene"],
              TYPE_I, "THC 17-22%, CBD <1%"),
        ]),
    ]),
]),

# ==========================================================================
# CLADE I - SPECIALTY CANNABINOID & BALANCED / HEMP
# ==========================================================================
("Specialty Cannabinoid & Balanced", [
    ("Type III - CBD-Dominant", [
        ("High-CBD", [
            S("Charlotte's Web", "Hemp-line high-CBD selection",
              "Landmark CBD hemp cultivar; earthy-pine, minimal high.",
              ["myrcene", "pinene", "caryophyllene", "bisabolol"],
              TYPE_III, "CBD 13-20%, THC <0.3%"),
            S("ACDC", "Cannatonic phenotype (high-CBD)",
              "~20:1 CBD:THC; clear, non-intoxicating relief.",
              ["myrcene", "pinene", "caryophyllene"],
              TYPE_III, "CBD 14-20%, THC <1% (~20:1)"),
            S("Harle-Tsu", "Harlequin x Sour Tsunami",
              "High-CBD relief cultivar; woody-citrus, gentle.",
              ["myrcene", "caryophyllene", "pinene", "terpinolene"],
              TYPE_III, "CBD 16-22%, THC <1% (~20:1)"),
            S("Sour Tsunami", "Sour Diesel x NYC Diesel (CBD selection)",
              "One of the first bred-for-CBD strains; diesel-sweet.",
              ["myrcene", "caryophyllene", "pinene"],
              TYPE_III, "CBD 10-13%, THC 6-11% (leans III)"),
            S("Ringo's Gift", "Harle-Tsu x ACDC",
              "Very high-CBD tribute cultivar; earthy and mild.",
              ["myrcene", "pinene", "caryophyllene"],
              TYPE_III, "CBD 15-20%, THC <1% (up to 24:1)"),
            S("Suzy Q", "High-CBD Californian selection",
              "CBD-dominant medicinal cultivar; herbal-earthy.",
              ["myrcene", "pinene", "terpinolene"],
              TYPE_III, "CBD 12-18%, THC <1%"),
            S("Remedy", "Cannatonic x Afghan Skunk",
              "Sedative high-CBD cultivar; floral-lemon and calm.",
              ["linalool", "myrcene", "pinene", "caryophyllene"],
              TYPE_III, "CBD 12-18%, THC <1% (~15:1)"),
            S("Charlotte's Angel", "Dutch high-CBD ACDC-line",
              "European CBD cultivar; pine-earth, clear-headed.",
              ["pinene", "myrcene", "caryophyllene"],
              TYPE_III, "CBD 10-16%, THC <1%"),
        ]),
    ]),
    ("Type II - Balanced (Mixed Ratio)", [
        ("1:1 & Mixed", [
            S("Cannatonic", "MK Ultra x G13 Haze",
              "Foundational balanced cultivar; ~1:1, mellow-earthy.",
              ["myrcene", "pinene", "caryophyllene", "limonene"],
              TYPE_II, "THC 6-12%, CBD 6-17% (mixed ~1:1)"),
            S("Harlequin", "Colombian Gold x Thai x Swiss x Nepali",
              "Reliable ~5:2 CBD:THC sativa; woody-mango, clear.",
              ["myrcene", "pinene", "caryophyllene", "terpinolene"],
              TYPE_II, "CBD 8-16%, THC 4-7% (mixed)"),
            S("Pennywise", "Harlequin x Jack the Ripper",
              "Balanced ~1:1 indica; coffee-citrus and calm.",
              ["myrcene", "caryophyllene", "pinene", "linalool"],
              TYPE_II, "THC 8-12%, CBD 8-15% (~1:1)"),
            S("CBD Critical Mass", "Critical Mass x high-CBD line",
              "High-yield balanced cultivar; earthy-sweet, ~1:1.",
              ["myrcene", "caryophyllene", "limonene"],
              TYPE_II, "CBD 5-13%, THC 5-8% (mixed)"),
            S("Stephen Hawking Kush", "Harle-Tsu x Sin City Kush",
              "Balanced dessert indica; cherry-mint, ~1:1 to 5:1.",
              ["myrcene", "caryophyllene", "linalool"],
              TYPE_II, "CBD 5-11%, THC 5-8% (mixed)"),
            S("Dance World", "Dancehall x Juanita la Lagrimosa",
              "Uplifting balanced cultivar; citrus-earth, ~1:1.",
              ["myrcene", "caryophyllene", "pinene"],
              TYPE_II, "CBD 8-12%, THC 8-12% (~1:1)"),
            S("Argyle", "CBD-rich indica hybrid",
              "Balanced medicinal indica; earthy-berry and gentle.",
              ["myrcene", "caryophyllene", "pinene"],
              TYPE_II, "CBD 5-10%, THC 5-8% (mixed)"),
        ]),
    ]),
    ("Type IV - CBG-Dominant", [
        ("High-CBG", [
            S("White CBG", "Oregon CBD Type-IV CBG clone x The White",
              "First commercial CBG-dominant flower; creamy lemon-diesel pine.",
              ["bisabolol", "caryophyllene", "guaiol"],
              TYPE_IV, "CBG 15-20%, THC <0.3%"),
            S("Panakeia", "First stabilized THC-free CBG cultivar",
              "Non-intoxicating CBG variety; herbal-sweet.",
              ["myrcene", "caryophyllene", "pinene"],
              TYPE_IV, "CBG ~10-16%, THC <0.3%"),
            S("Stem Cell CBG", "CBG-dominant hemp line",
              "High-CBG cultivar; clean pine-citrus, clear.",
              ["pinene", "myrcene", "limonene"],
              TYPE_IV, "CBG 10-15%, THC <0.3%"),
            S("John Snow CBG", "CBG-rich hemp selection",
              "CBG-forward cultivar; frosty and earthy.",
              ["myrcene", "pinene", "caryophyllene"],
              TYPE_IV, "CBG 9-15%, THC <0.3%"),
            S("Jack Frost CBG", "CBG hemp cultivar",
              "Balanced-terpene CBG hemp; sweet-pine.",
              ["pinene", "myrcene", "caryophyllene"],
              TYPE_IV, "CBG 8-14%, THC <0.3%"),
        ]),
    ]),
    ("THCV-Rich (Propyl)", [
        ("High-THCV", [
            S("Doug's Varin", "Harlequin x Thai landrace (propyl/THCV line)",
              "Most THCV-rich named cultivar (~15-24% THCV); sharp citrus-clear.",
              ["terpinolene", "caryophyllene", "limonene", "pinene"],
              THCV, "THCV ~15-24%, THC ~19-21%, CBD low"),
            S("Pink Boost Giesel", "Pink Boost x Giesel (Chem D x MA Super Skunk)",
              "Symbiotic Genetics cross; grapefruit-fuel, possible THCV note.",
              ["caryophyllene", "limonene", "myrcene"],
              THCV, "THC ~18-24%, possible THCV from Pink Boost, CBD low"),
            S("Willie Nelson", "Vietnamese Black x South African",
              "Sativa landrace hybrid; often THCV-elevated, sweet-sour.",
              ["terpinolene", "pinene", "myrcene"],
              THCV, "THC 16-22%, some THCV, CBD <0.5%"),
            S("Pineapple Purps", "THCV-rich sativa selection",
              "Tropical high-THCV cultivar; energetic and clear.",
              ["terpinolene", "ocimene", "pinene"],
              THCV, "THCV ~4-8%, THC 10-15%, CBD low"),
        ]),
    ]),
    ("Minor & Oxidative Cannabinoids", [
        ("CBN / CBC Focus", [
            S("Death Bubba", "Bubba Kush phenotype (Canada)",
              "Heavy sedative indica; ages readily toward CBN.",
              ["myrcene", "caryophyllene", "limonene", "pinene"],
              CBN, "THC 20-27%, CBD <1%; CBN rises with age"),
            S("Bubble Gum", "Indiana Bubble Gum heirloom hybrid",
              "Sweet candy hybrid; classic aged-CBN sedative note.",
              ["myrcene", "caryophyllene", "limonene"],
              CBN, "THC 15-19%, CBD <1%; notable CBN when cured/aged"),
            S("Ace of Spades", "Black Cherry Soda x Jack the Ripper",
              "Sweet-sour hybrid; balanced, mildly CBC/CBN-forward.",
              ["terpinolene", "caryophyllene", "myrcene"],
              CBN, "THC 18-22%, minor CBC/CBN, CBD <1%"),
            S("Bediol", "Standardized medical cultivar (Bedrocan)",
              "Pharma-grade balanced cultivar; consistent ~1:2 THC:CBD.",
              ["myrcene", "pinene", "caryophyllene"],
              TYPE_II, "THC ~6%, CBD ~8% (standardized mixed)"),
        ]),
    ]),
]),

]  # end TREE


# --------------------------------------------------------------------------
# EXPANSION - additional sub-families merged into the clades above by name,
# taking the wheel past 300 strains while keeping one arc per clade.
# --------------------------------------------------------------------------
MORE = [

("Equatorial Sativa Landraces", [
    ("More Landrace Sativa", [
        ("Indochina & Insular", [
            S("Laotian", "Laos landrace (sativa)",
              "Indochina lowland sativa; sweet, clear, long-flowering.",
              ["terpinolene", "ocimene", "myrcene"], TYPE_I,
              "THC 15-20%, CBD <0.5%"),
            S("Luang Prabang", "Northern Laos landrace",
              "Mekong highland sativa; incense-citrus and racy.",
              ["terpinolene", "pinene", "limonene"], TYPE_I,
              "THC 14-19%, CBD <0.5%"),
            S("Aceh", "Sumatran landrace (Indonesia)",
              "Equatorial island sativa; spicy-sweet and dreamy.",
              ["myrcene", "terpinolene", "caryophyllene"], TYPE_I,
              "THC 14-18%, CBD <0.5%"),
            S("Vietnamese Highland", "Vietnam highland landrace",
              "Cool-mountain sativa; herbal-pine and energetic.",
              ["terpinolene", "pinene", "ocimene"], TYPE_I,
              "THC 15-20%, CBD <0.5%"),
        ]),
        ("More African", [
            S("Ethiopian Highland", "Ethiopian landrace (sativa)",
              "Horn-of-Africa highland sativa; spicy and clear.",
              ["terpinolene", "myrcene", "pinene"], TYPE_I,
              "THC 14-19%, CBD <0.5%"),
            S("Zambian", "Zambian landrace (sativa)",
              "Central African sativa; sweet-herbal and soaring.",
              ["terpinolene", "ocimene", "caryophyllene"], TYPE_I,
              "THC 15-20%, CBD <0.5%"),
            S("Transkei", "South African landrace (Transkei)",
              "Wild-coast sativa; grassy-citrus and buzzy.",
              ["terpinolene", "pinene", "myrcene"], TYPE_I,
              "THC 14-19%, CBD <0.5%"),
        ]),
        ("More Latin American", [
            S("Brazilian", "Brazilian landrace (sativa)",
              "South American lowland sativa; a White Widow ancestor.",
              ["terpinolene", "myrcene", "limonene"], TYPE_I,
              "THC 14-18%, CBD <0.5%"),
            S("Santa Marta Gold", "Colombian landrace (Sierra Nevada)",
              "Golden Colombian sativa; sweet and euphoric.",
              ["terpinolene", "pinene", "limonene", "myrcene"], TYPE_I,
              "THC 15-21%, CBD <0.5%"),
            S("Guerreran", "Mexican landrace (Guerrero)",
              "Pacific-coast sativa; citrus-earthy and uplifting.",
              ["terpinolene", "ocimene", "pinene"], TYPE_I,
              "THC 14-19%, CBD <0.5%"),
        ]),
    ]),
]),

("Asian Indica Landraces", [
    ("More Hash Landraces", [
        ("Mediterranean & Middle East", [
            S("Lebanese", "Lebanese landrace (Beqaa Valley)",
              "Red/blond hashish landrace; low-key earthy-spice, often CBD-rich.",
              ["myrcene", "pinene", "caryophyllene"], TYPE_II,
              "THC 8-14%, CBD 4-8% (often mixed)"),
            S("Moroccan", "Moroccan landrace (Ketama, Rif)",
              "Kif hashplant landrace; herbal-earthy and mellow.",
              ["myrcene", "caryophyllene", "pinene"], TYPE_II,
              "THC 8-12%, CBD 3-7% (mixed)"),
            S("Turkish", "Anatolian landrace (indica)",
              "Old-world hashplant; sweet-earthy and calming.",
              ["myrcene", "humulene", "caryophyllene"], TYPE_I,
              "THC 12-17%, CBD 1-3%"),
            S("Syrian", "Syrian landrace (indica)",
              "Levantine hashplant; spicy-resinous and heavy.",
              ["myrcene", "caryophyllene", "pinene"], TYPE_I,
              "THC 13-18%, CBD <2%"),
        ]),
        ("Central Asian Extra", [
            S("Kandahar", "Afghan landrace (Kandahar)",
              "Southern Afghan broadleaf; dense hash resin.",
              ["myrcene", "caryophyllene", "humulene"], TYPE_I,
              "THC 15-20%, CBD <1%"),
            S("Tashkurgan", "Central Asian landrace (indica)",
              "High-plateau charas indica; earthy-incense.",
              ["myrcene", "pinene", "caryophyllene"], TYPE_I,
              "THC 13-18%, CBD <1%"),
        ]),
    ]),
]),

("Haze Lineage", [
    ("More Haze & Citrus Sativa", [
        ("Citrus Sativa", [
            S("Tangie", "California Orange x Skunk",
              "Zesty tangerine sativa; a modern citrus benchmark.",
              ["limonene", "myrcene", "pinene", "caryophyllene"], TYPE_I,
              "THC 19-22%, CBD <0.5%"),
            S("Agent Orange", "Orange Velvet x Jack the Ripper",
              "Orange-cream hybrid; bright, buzzy mood-lift.",
              ["limonene", "terpinolene", "caryophyllene"], TYPE_I,
              "THC 17-21%, CBD <0.5%"),
            S("Clementine", "Tangie x Lemon Skunk",
              "Sweet citrus sativa; energetic and clear.",
              ["limonene", "terpinolene", "myrcene", "caryophyllene"], TYPE_I,
              "THC 19-24%, CBD <0.5%"),
            S("Lemon Tree", "Lemon Skunk x Sour Diesel",
              "Loud lemon-fuel hybrid; happy and giggly.",
              ["limonene", "caryophyllene", "myrcene"], TYPE_I,
              "THC 18-25%, CBD <0.5%"),
        ]),
        ("Haze Hybrids II", [
            S("Casey Jones", "Trainwreck x Thai x Sour Diesel",
              "Sweet-diesel sativa; fast, energetic express.",
              ["caryophyllene", "myrcene", "terpinolene"], TYPE_I,
              "THC 18-22%, CBD <0.5%"),
            S("Laughing Buddha", "Thai x Jamaican sativa",
              "Fruity tropical sativa; giddy and upbeat.",
              ["terpinolene", "ocimene", "myrcene"], TYPE_I,
              "THC 18-22%, CBD <0.5%"),
            S("Kali China", "Kali Mist x China Yunnan",
              "Spicy-citrus sativa; clear cerebral lift.",
              ["terpinolene", "myrcene", "pinene"], TYPE_I,
              "THC 16-20%, CBD <0.5%"),
            S("Nevil's Wreck", "Trainwreck x A5 Haze",
              "Neville's high-yield haze-wreck; pine-citrus power.",
              ["terpinolene", "caryophyllene", "pinene"], TYPE_I,
              "THC 20-24%, CBD <0.5%"),
        ]),
    ]),
]),

("Skunk Lineage", [
    ("More Skunk & Cheese", [
        ("Cheese & Funk", [
            S("Cheese Quake", "UK Cheese x Querkle",
              "Grape-cheese hybrid; funky, sweet, and mellow.",
              ["myrcene", "caryophyllene", "limonene"], TYPE_I,
              "THC 15-20%, CBD <0.5%"),
            S("Sour Cheese", "UK Cheese x Sour Diesel",
              "Tangy cheese-fuel hybrid; pungent and lively.",
              ["myrcene", "caryophyllene", "limonene"], TYPE_I,
              "THC 16-20%, CBD <0.5%"),
            S("Cheesus", "UK Cheese x (Skunk hybrid)",
              "Extra-loud Cheese cut; savory and heavy.",
              ["myrcene", "caryophyllene", "humulene"], TYPE_I,
              "THC 16-21%, CBD <0.5%"),
        ]),
        ("Fruity Skunk II", [
            S("Grapefruit", "Cinderella 99 x indica selection",
              "Sweet grapefruit-citrus hybrid; uplifting and bright.",
              ["limonene", "myrcene", "caryophyllene"], TYPE_I,
              "THC 16-22%, CBD <0.5%"),
            S("Orange Crush", "California Orange selection",
              "Candied-orange Skunk hybrid; happy and clear.",
              ["limonene", "myrcene", "pinene"], TYPE_I,
              "THC 15-20%, CBD <0.5%"),
            S("Chernobyl", "Trainwreck x Trinity x Jack the Ripper",
              "Lime-sherbet sativa hybrid; dreamy and light.",
              ["terpinolene", "ocimene", "caryophyllene"], TYPE_I,
              "THC 17-22%, CBD <0.5%"),
            S("Tangerine Dream", "G13 x Afghani x Neville's Haze",
              "Tangerine-citrus hybrid; smooth energetic lift.",
              ["limonene", "myrcene", "caryophyllene"], TYPE_I,
              "THC 18-22%, CBD <0.5%"),
        ]),
    ]),
]),

("Kush / OG Lineage", [
    ("More OG & Kush", [
        ("OG Cuts II", [
            S("Legend OG", "OG Kush phenotype (Legend cut)",
              "Potent classic OG cut; earthy-pine and heavy.",
              ["myrcene", "limonene", "caryophyllene"], TYPE_I,
              "THC 20-25%, CBD <1%"),
            S("Pure Kush", "OG Kush phenotype",
              "Sedative OG cut; earthy-citrus couch-lock.",
              ["myrcene", "caryophyllene", "limonene"], TYPE_I,
              "THC 20-25%, CBD <1%"),
            S("Abusive OG", "OG Kush cut (Abusive)",
              "Elite LA OG cut; lemon-pine and dense.",
              ["limonene", "myrcene", "caryophyllene"], TYPE_I,
              "THC 20-25%, CBD <1%"),
            S("Josh D OG", "Original OG Kush cut (Josh D)",
              "Foundational OG Kush lineage cut; classic gas-lemon.",
              ["caryophyllene", "limonene", "myrcene"], TYPE_I,
              "THC 20-25%, CBD <1%"),
        ]),
        ("Kush II", [
            S("Rockstar", "Rockbud x Sensi Star",
              "Grape-earth indica; relaxing and social.",
              ["myrcene", "caryophyllene", "pinene"], TYPE_I,
              "THC 18-24%, CBD <1%"),
            S("Godfather OG", "XXX OG x Alpha OG",
              "'Don of all OGs'; grape-fuel and knockout heavy.",
              ["myrcene", "limonene", "caryophyllene", "linalool"], TYPE_I,
              "THC 25-30%, CBD <1%"),
            S("Presidential OG", "OG Kush x Bubba Kush",
              "Lemon-pine OG indica; regal and sedative.",
              ["myrcene", "limonene", "caryophyllene"], TYPE_I,
              "THC 20-25%, CBD <1%"),
            S("Death Star", "Sensi Star x Sour Diesel",
              "Fuel-skunk OG-diesel indica; creeping and heavy.",
              ["caryophyllene", "myrcene", "limonene"], TYPE_I,
              "THC 20-25%, CBD <1%"),
        ]),
    ]),
]),

("Diesel / Chem Lineage", [
    ("More Diesel & Chem", [
        ("Diesel II", [
            S("Chocolate Diesel", "Chocolate Thai x Sour Diesel",
              "Coffee-fuel sativa; a Gorilla Glue #4 parent.",
              ["caryophyllene", "myrcene", "limonene"], TYPE_I,
              "THC 20-25%, CBD <1%"),
            S("Sour Tangie", "East Coast Sour Diesel x Tangie",
              "Citrus-fuel sativa; loud, bright, and racy.",
              ["caryophyllene", "limonene", "myrcene"], TYPE_I,
              "THC 20-24%, CBD <1%"),
            S("Underdawg", "Chemdawg x (OG lineage)",
              "Gassy Chem-OG hybrid; sharp and potent.",
              ["caryophyllene", "limonene", "humulene"], TYPE_I,
              "THC 20-25%, CBD <1%"),
            S("Alien Rock Candy", "Sour Dubble x Tahoe Alien",
              "Sweet-fuel candy hybrid; euphoric and heavy.",
              ["caryophyllene", "limonene", "myrcene"], TYPE_I,
              "THC 20-24%, CBD <1%"),
        ]),
    ]),
]),

("Cookies / Dessert Lineage", [
    ("More Dessert & Exotics", [
        ("Exotic Cookies II", [
            S("Gary Payton", "The Y (Cookies) x Snowman",
              "Cool, gassy-herbal exotic Cookies; potent balance.",
              ["caryophyllene", "limonene", "linalool"], TYPE_I,
              "THC 20-25%, CBD <1%"),
            S("Permanent Marker", "Biscotti x Jealousy x Sherbet BX",
              "Soapy-floral funk exotic; a 2023 breakout.",
              ["limonene", "caryophyllene", "linalool"], TYPE_I,
              "THC 24-30%, CBD <1%"),
            S("Apples and Bananas", "Blue Power x Gelatti x GMO x Grape Pie",
              "Fruity-gas exotic Cookies; sweet and heavy.",
              ["caryophyllene", "limonene", "myrcene"], TYPE_I,
              "THC 22-28%, CBD <1%"),
            S("Oreoz", "Cookies and Cream x Secret Weapon",
              "Chocolate-diesel dessert; rich and sedative.",
              ["caryophyllene", "limonene", "myrcene"], TYPE_I,
              "THC 22-28%, CBD <1%"),
            S("Pancakes", "London Pound Cake x Kush Mints",
              "Buttery-sweet Cookies indica; smooth and calm.",
              ["caryophyllene", "limonene", "linalool"], TYPE_I,
              "THC 20-26%, CBD <1%"),
            S("Cap Junky", "Alien Cookies x Kush Mints",
              "Loud gas-menthol exotic; extremely potent.",
              ["caryophyllene", "limonene", "linalool"], TYPE_I,
              "THC 25-34%, CBD <1%"),
        ]),
        ("Cake & Mints II", [
            S("London Pound Cake", "Sunset Sherbet x undisclosed",
              "Berry-citrus dessert Cookies; relaxing and sweet.",
              ["caryophyllene", "limonene", "linalool"], TYPE_I,
              "THC 22-29%, CBD <1%"),
            S("Jungle Cake", "Wedding Cake x White Fire #43",
              "Sweet-nutty Cake hybrid; frosty and balanced.",
              ["caryophyllene", "limonene", "myrcene"], TYPE_I,
              "THC 22-28%, CBD <1%"),
            S("Wedding Pie", "Wedding Cake x Grape Pie",
              "Tart grape-vanilla dessert indica; calm and rich.",
              ["caryophyllene", "myrcene", "limonene"], TYPE_I,
              "THC 20-25%, CBD <1%"),
            S("Cake Batter", "Girl Scout Cookies x Cherry Pie x GSC",
              "Doughy-sweet Cookies indica; heavy and smooth.",
              ["caryophyllene", "limonene", "linalool"], TYPE_I,
              "THC 20-26%, CBD <1%"),
        ]),
        ("Runtz II", [
            S("White Truffle", "Gorilla Butter phenotype (GMO line)",
              "Savory earthy-mushroom exotic; a GMO relative.",
              ["caryophyllene", "limonene", "humulene"], TYPE_I,
              "THC 20-27%, CBD <1%"),
            S("Peanut Butter Breath", "Do-Si-Dos x Mendo Breath",
              "Nutty-earthy Cookies indica; deeply relaxing.",
              ["limonene", "caryophyllene", "linalool"], TYPE_I,
              "THC 18-24%, CBD <1%"),
            S("Gastro Pop", "Apples and Bananas x Grape Gasoline",
              "Grape-candy gas exotic; loud, sweet, and heavy.",
              ["caryophyllene", "limonene", "myrcene"], TYPE_I,
              "THC 22-30%, CBD <1%"),
        ]),
    ]),
]),

("Purple / Grape & Berry Indica", [
    ("More Purple & Fruit", [
        ("Purple II", [
            S("Mendo Breath", "OGKB x Mendo Montage",
              "Vanilla-caramel indica; deeply relaxing nightcap.",
              ["caryophyllene", "limonene", "myrcene"], TYPE_I,
              "THC 18-24%, CBD <1%"),
            S("Forbidden Fruit", "Cherry Pie x Tangie",
              "Tropical cherry-citrus indica; lush and calming.",
              ["myrcene", "caryophyllene", "limonene", "linalool"], TYPE_I,
              "THC 18-24%, CBD <1%"),
            S("Blackberry Kush", "Afghani x Blackberry",
              "Sweet berry-fuel indica; heavy and sedating.",
              ["myrcene", "caryophyllene", "linalool", "pinene"], TYPE_I,
              "THC 16-24%, CBD <1%"),
            S("Grape Diamonds", "Grape Pie x Zkittlez",
              "Sugary grape-candy indica; smooth and mellow.",
              ["caryophyllene", "myrcene", "linalool"], TYPE_I,
              "THC 18-23%, CBD <1%"),
        ]),
        ("Berry II", [
            S("Raspberry Cough", "Cambodian x ICE",
              "Tart raspberry sativa hybrid; clear and lifted.",
              ["myrcene", "terpinolene", "caryophyllene"], TYPE_I,
              "THC 15-20%, CBD <1%"),
            S("Cherry AK", "Cherry Bomb x AK-47",
              "Sweet-cherry hybrid; balanced and social.",
              ["myrcene", "caryophyllene", "limonene"], TYPE_I,
              "THC 16-21%, CBD <1%"),
            S("Strawberry Banana", "Bubble Gum x Banana Kush",
              "Creamy strawberry indica; relaxed and happy.",
              ["limonene", "caryophyllene", "myrcene"], TYPE_I,
              "THC 22-26%, CBD <1%"),
            S("Wild Berry", "Blueberry x indica hybrid",
              "Mixed-berry indica; sweet and soothing.",
              ["myrcene", "caryophyllene", "pinene"], TYPE_I,
              "THC 16-20%, CBD <1%"),
        ]),
    ]),
]),

("Specialty Cannabinoid & Balanced", [
    ("More Balanced & Rare Cannabinoid", [
        ("CBD II", [
            S("Cannatsu", "Cannatonic x Sour Tsunami",
              "CBD-rich medicinal cross; earthy-sweet and gentle.",
              ["myrcene", "pinene", "caryophyllene"], TYPE_III,
              "CBD 10-16%, THC <1%"),
            S("Nordle", "Afghani x Skunk (Sensi CBD-rich)",
              "Balanced CBD-rich cultivar; hashy-earthy and calm.",
              ["myrcene", "caryophyllene", "pinene"], TYPE_II,
              "CBD 5-9%, THC 5-9% (~1:1)"),
            S("Valentine X", "ACDC-line high-CBD selection",
              "Ultra-high-CBD medical cultivar; ~25:1, clear-headed.",
              ["myrcene", "pinene", "terpinolene"], TYPE_III,
              "CBD 15-22%, THC <1% (~25:1)"),
            S("Sweet and Sour Widow", "White Widow high-CBD selection",
              "Balanced Widow cultivar; earthy-sweet ~1:1.",
              ["myrcene", "caryophyllene", "pinene"], TYPE_II,
              "CBD 6-8%, THC 6-8% (~1:1)"),
        ]),
        ("CBG & THCV II", [
            S("Matterhorn CBG", "CBG-dominant hemp cultivar",
              "High-CBG hemp; clean pine-lemon, non-intoxicating.",
              ["pinene", "myrcene", "limonene"], TYPE_IV,
              "CBG 10-15%, THC <0.3%"),
            S("Super Glue CBG", "CBG-dominant hemp line",
              "Resinous high-CBG hemp; earthy-diesel and clear.",
              ["myrcene", "caryophyllene", "pinene"], TYPE_IV,
              "CBG 9-14%, THC <0.3%"),
            S("Black Beauty", "THCV-rich sativa selection",
              "Rare high-THCV cultivar; sharp, clear, appetite-flattening.",
              ["terpinolene", "pinene", "ocimene"], THCV,
              "THCV ~4-8%, THC 8-14%, CBD low"),
        ]),
    ]),
]),

]  # end MORE


# --------------------------------------------------------------------------
# Anchor strains that MUST be present (from the brief)
# --------------------------------------------------------------------------
ANCHORS = [
    "Haze", "White Widow", "Early Pearl", "Skunk #1", "Amnesia Haze",
    "Jack Herer", "Cinderella 99", "Black Domina", "Thai", "Afghani",
    "Gorilla Glue #4", "Sour Diesel", "Cherry Pie", "Granddaddy Purple",
    "GSC", "Biscotti", "RS-11", "GMO", "SFV OG", "Tahoe OG", "Louis XIII",
    "Oaxacan",
]


# --------------------------------------------------------------------------
# Build hierarchy + flat registry, with progress reporting every 12 strains
# --------------------------------------------------------------------------
CHEMO_COLORS = {
    TYPE_I:   "#e07a3f",   # THC - orange
    TYPE_II:  "#8e6fb0",   # mixed - violet
    TYPE_III: "#4a9d5b",   # CBD - green
    TYPE_IV:  "#3f8fa8",   # CBG - teal
    THCV:     "#d4a53a",   # THCV - gold
    CBN:      "#9c5a3c",   # CBN - brown
}


def merged_tree():
    """Merge MORE sub-families into TREE clades by clade name, preserving order."""
    order = []
    clades = {}
    for clade_name, subs in TREE:
        if clade_name not in clades:
            clades[clade_name] = []
            order.append(clade_name)
        clades[clade_name].extend(subs)
    for clade_name, subs in MORE:
        if clade_name not in clades:
            clades[clade_name] = []
            order.append(clade_name)
        clades[clade_name].extend(subs)
    return [(name, clades[name]) for name in order]


def build():
    root = {"name": "Cannabis", "children": []}
    flat = []
    count = 0

    for clade_name, subfamilies in merged_tree():
        clade_node = {"name": clade_name, "children": []}
        for sub_name, groups in subfamilies:
            sub_node = {"name": sub_name, "children": []}
            for group_name, strains in groups:
                group_node = {"name": group_name, "children": []}
                for st in strains:
                    leaf = dict(st)
                    leaf["clade"] = clade_name
                    leaf["subfamily"] = sub_name
                    leaf["group"] = group_name
                    leaf["color"] = CHEMO_COLORS.get(st["chemotype"], "#888")
                    group_node["children"].append(leaf)

                    flat.append(leaf)
                    count += 1
                    if count % 12 == 0:
                        print("  [report] %3d strains built ... latest: "
                              "%-22s (%s / %s)"
                              % (count, st["name"], clade_name, st["chemotype"]))
                sub_node["children"].append(group_node)
            clade_node["children"].append(sub_node)
        root["children"].append(clade_node)

    if count % 12 != 0:
        print("  [report] %3d strains built (final batch)." % count)

    return root, flat, count


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    print("Potent Garden - building cannabis genetic clade wheel ...\n")

    root, flat, count = build()

    # ---- validation ------------------------------------------------------
    print("\nValidation")
    print("  leaf strains : %d" % count)
    names = {s["name"] for s in flat}

    # duplicate check
    from collections import Counter
    dupes = [n for n, c in Counter(s["name"] for s in flat).items() if c > 1]
    if dupes:
        print("  WARNING duplicate strain names: %s" % dupes)
    else:
        print("  duplicate names : none")

    # anchor check
    missing = [a for a in ANCHORS if a not in names]
    if missing:
        print("  MISSING anchors : %s" % missing)
    else:
        print("  anchors present : all %d" % len(ANCHORS))

    # chemotype coverage
    from collections import Counter as C2
    chemo_counts = C2(s["chemotype"] for s in flat)
    print("  chemotype coverage:")
    for k, v in chemo_counts.items():
        print("      %-40s %d" % (k, v))

    assert count >= 250, "Expected 250+ leaf strains, got %d" % count
    assert not missing, "Missing anchor strains: %s" % missing
    assert not dupes, "Duplicate strain names: %s" % dupes

    # clade/ring metadata for the visualization
    payload = {
        "meta": {
            "title": "Potent Garden - Cannabis Genetic Clade Wheel",
            "rings": ["Cannabis (root)", "Clade", "Sub-family", "Group", "Strain"],
            "strain_count": count,
            "clade_count": len(root["children"]),
            "chemotypes": CHEMO_COLORS,
            "generated_by": "build_data.py",
        },
        "tree": root,
        "strains": flat,
    }

    out_json = os.path.join(here, "potent_garden_clade_wheel.json")
    with open(out_json, "w") as f:
        json.dump(payload, f, indent=2)
    print("\nWrote %s (%d strains, %d clades)."
          % (os.path.basename(out_json), count, len(root["children"])))

    # Also emit a JS module so the HTML wheel opens by double-click without a
    # local server (file:// fetch is blocked by CORS in most browsers).
    out_js = os.path.join(here, "clade_wheel_data.js")
    with open(out_js, "w") as f:
        f.write("window.POTENT_GARDEN_DATA = ")
        json.dump(payload, f)
        f.write(";\n")
    print("Wrote %s (embedded data for the visualization)."
          % os.path.basename(out_js))

    # Emit the flat reference table (markdown) straight from the data.
    out_md = os.path.join(here, "strains_table.md")
    write_table(out_md, flat, count, len(root["children"]), chemo_counts)
    print("Wrote %s (flat reference table + references)."
          % os.path.basename(out_md))


def md_escape(s):
    return str(s).replace("|", "\\|")


def write_table(path, flat, count, n_clades, chemo_counts):
    from collections import OrderedDict
    # group rows by clade -> subfamily
    by_clade = OrderedDict()
    for s in flat:
        by_clade.setdefault(s["clade"], []).append(s)

    with open(path, "w") as f:
        f.write("# Potent Garden - Cannabis Genetic Clade Wheel: Strain Table\n\n")
        f.write("A 4-ring genetic clade (sunburst) taxonomy of **%d representative "
                "cultivars** across **%d clades**, chosen to span the plant's genetic "
                "and chemotype variability.\n\n" % (count, n_clades))
        f.write("- **Ring 1** Clade &middot; **Ring 2** Sub-family &middot; "
                "**Ring 3** Group &middot; **Ring 4** Strain (rows below)\n")
        f.write("- Terpenes are listed **top-first by typical dominance** "
                "(3-8 per strain).\n")
        f.write("- Chemotype uses the de Meijer / Hillig framework "
                "(Type I THC, II mixed, III CBD, IV CBG) plus THCV and CBN tags.\n\n")

        f.write("## Chemotype coverage\n\n")
        f.write("| Chemotype | Strains |\n|---|---|\n")
        for k, v in chemo_counts.items():
            f.write("| %s | %d |\n" % (k, v))
        f.write("\n")

        f.write("## Clade coverage\n\n")
        f.write("| Clade | Strains |\n|---|---|\n")
        for clade, rows in by_clade.items():
            f.write("| %s | %d |\n" % (clade, len(rows)))
        f.write("\n---\n\n")

        for clade, rows in by_clade.items():
            f.write("## %s  (%d strains)\n\n" % (clade, len(rows)))
            f.write("| Sub-family | Group | Strain | Parents | Description | "
                    "Terpenes (ordered) | Chemotype | Cannabinoids |\n")
            f.write("|---|---|---|---|---|---|---|---|\n")
            for s in rows:
                f.write("| %s | %s | **%s** | %s | %s | %s | %s | %s |\n" % (
                    md_escape(s["subfamily"]), md_escape(s["group"]),
                    md_escape(s["name"]), md_escape(s["parents"]),
                    md_escape(s["description"]),
                    md_escape(", ".join(s["terpenes"])),
                    md_escape(s["chemotype"]), md_escape(s["cannabinoids"]),
                ))
            f.write("\n")

        f.write(REFERENCES_MD)


REFERENCES_MD = """---

## References & methodology

Lineages, terpene dominance orders and chemotype classifications are grounded
in well-established cannabis-genetics knowledge and public aggregate lab/terpene
data, verified against the sources below. **Caveats:** many clone-only cuts
(OG Kush, Bubba, Tahoe, Louis XIII, Chemdawg, GG4, Cheese, GSC anchors, etc.)
have disputed or undocumented pedigrees - parentage is best-consensus, not a
verified breeder record. Terpene orders are typical-case and vary by phenotype,
batch and lab; treat cannabinoid percentages as indicative ranges rather than a
single assay. THCV/CBG/CBN figures are the least standardized data points.

### Chemotype & terpene framework (peer-reviewed)
- de Meijer et al. (2003), *The Inheritance of Chemical Phenotype in Cannabis
  sativa L.*, Genetics 163(1):335-346. (Type I/II/III single-locus B model.)
  https://pubmed.ncbi.nlm.nih.gov/12586720/
- Hillig & Mahlberg (2004), *A Chemotaxonomic Analysis of Cannabinoid Variation
  in Cannabis*, Am. J. Botany 91(6):966-975.
  https://bsapubs.onlinelibrary.wiley.com/doi/10.3732/ajb.91.6.966
- de Meijer & Hammond (2005), *...(II): Cannabigerol predominant plants*,
  Euphytica 145:189-198 (Type IV / CBG, B0 allele).
  https://link.springer.com/article/10.1007/s10681-005-1164-8
- de Meijer et al. (2016), *...(V): regulation of the propyl-/pentyl cannabinoid
  ratio*, Euphytica 210:291 (THCV / propyl locus Pr).
  https://link.springer.com/article/10.1007/s10681-016-1721-3
- Lewis et al. (2018), *Pharmacological Foundations of Cannabis Chemovars*,
  Planta Medica 84(4):225-233 (terpene-based chemovar framework).
  https://www.thieme-connect.de/products/ejournals/abstract/10.1055/a-0915-2550
- Hillig (2004), *A chemotaxonomic analysis of terpenoid variation in Cannabis.*

### Rare-cannabinoid pharmacology
- THCV (CB1/CB2 antagonist): Thomas et al. 2005, Br. J. Pharmacol. 146:917 -
  https://pmc.ncbi.nlm.nih.gov/articles/PMC1751228/
- CBG ("mother cannabinoid"): Calapai et al. 2022 -
  https://pmc.ncbi.nlm.nih.gov/articles/PMC9666035/
- CBN (oxidative THC degradation product, sedative) -
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7997633/

### Strain lineage / terpene / chemotype aggregators
- Leafly strain database - https://www.leafly.com/strains
- SeedFinder genealogy - https://en.seedfinder.eu/
- Strainpedia - https://www.strainpedia.com/
- Sensi Seeds - https://sensiseeds.com/ ; DNA Genetics - https://dnagenetics.com/
- Green House Seed Co. - https://shop.greenhouseseeds.nl/
- Royal Queen Seeds - https://www.royalqueenseeds.com/
- Phylos Bioscience "Galaxy" genotype project (population/lineage context).
- Abstrax Tech terpene profiles - https://abstraxtech.com/blogs/learn
- Cannigma strain profiles - https://cannigma.com/strains/

### Specialty / high-CBD, CBG, THCV cultivars
- Charlotte's Web - https://en.wikipedia.org/wiki/Charlotte's_Web_(cannabis)
- ACDC / Cannatonic (Resin Seeds) -
  https://seedfinder.eu/en/strain-info/cannatonic/resin-seeds
- Harle-Tsu, Sour Tsunami, Ringo's Gift (SoHum Seed Collective) - Leafly entries.
- White CBG (Oregon CBD) - https://www.leafly.com/strains/white-cbg
- Panakeia (Hemp Trading / UPV, THC-free CBG) -
  https://www.alchimiaweb.com/blogen/panakeia/
- Doug's Varin (high-THCV) - https://www.leafly.com/strains/dougs-varin
"""


if __name__ == "__main__":
    main()
