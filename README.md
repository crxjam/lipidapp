# lipidapp
# Lipid Electrophoresis Classifier

Browser-based tool for classifying lipid electrophoresis densitometry scans according to Fredrickson phenotype.

## Orientation

Gel inspection should be standardised with the cathodic end at the top when the gel is placed on a clean white background.

Bands are interpreted from application point towards the anode:

1. Chylomicrons / application point
2. Beta / LDL
3. Pre-beta / VLDL
4. Alpha / HDL
5. Albumin-associated staining may be seen in aged samples or samples with increased non-esterified fatty acids

## Classification targets

- Normal
- Type I
- Type IIa
- Type IIb
- Type III
- Type IV
- Type V
- Lipoprotein X suspected
- Poor quality / repeat recommended
- Unclassified

## Current status

Version 0.1 supports:
- scan upload
- manual feature entry
- rule-based Fredrickson classification
- confirmed label saving for future AI training

Automated densitometry curve extraction will be added next.
