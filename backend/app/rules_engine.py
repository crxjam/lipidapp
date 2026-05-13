from typing import Dict, Any


def classify_fredrickson(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Rule-based Fredrickson classification for lipid electrophoresis.

    Expected features:
    - origin_peak: bool
    - beta_increased: bool
    - prebeta_increased: bool
    - broad_beta: bool
    - lpx_suspected: bool
    - sample_quality_issue: bool
    - alpha_visible: bool
    """

    reasons = []

    if features.get("sample_quality_issue"):
        return {
            "classification": "Poor quality / repeat recommended",
            "confidence": "low",
            "reasons": ["Image or scan quality was insufficient for reliable classification."],
        }

    if features.get("lpx_suspected"):
        return {
            "classification": "Lipoprotein X suspected",
            "confidence": "moderate",
            "reasons": [
                "Broad diffuse band close to the application point.",
                "This is not a Fredrickson phenotype and should be correlated with cholestasis.",
            ],
        }

    origin = features.get("origin_peak", False)
    beta = features.get("beta_increased", False)
    prebeta = features.get("prebeta_increased", False)
    broad_beta = features.get("broad_beta", False)

    if broad_beta:
        return {
            "classification": "Type III",
            "confidence": "moderate",
            "reasons": [
                "Broad beta morphology detected.",
                "Pattern suggests increased IDL / remnant lipoproteins.",
                "Note: broad beta is specific but not sensitive for dysbetalipoproteinaemia.",
            ],
        }

    if origin and not beta and not prebeta:
        return {
            "classification": "Type I",
            "confidence": "moderate",
            "reasons": [
                "Chylomicron/origin band increased.",
                "Other lipoprotein bands are not significantly increased.",
                "LDL absence or marked reduction supports Type I.",
            ],
        }

    if beta and not prebeta and not origin:
        return {
            "classification": "Type IIa",
            "confidence": "moderate",
            "reasons": [
                "Predominant increased beta band.",
                "Pattern suggests increased LDL.",
            ],
        }

    if beta and prebeta and not origin:
        return {
            "classification": "Type IIb",
            "confidence": "moderate",
            "reasons": [
                "Both beta and pre-beta bands are increased.",
                "Pattern suggests increased LDL and VLDL.",
            ],
        }

    if prebeta and not beta and not origin:
        return {
            "classification": "Type IV",
            "confidence": "moderate",
            "reasons": [
                "Predominant increased pre-beta band.",
                "Pattern suggests increased VLDL.",
            ],
        }

    if origin and prebeta:
        return {
            "classification": "Type V",
            "confidence": "moderate",
            "reasons": [
                "Chylomicron/origin band increased.",
                "Pre-beta/VLDL band also increased.",
            ],
        }

    return {
        "classification": "Normal / unclassified",
        "confidence": "low",
        "reasons": [
            "No clear abnormal Fredrickson pattern detected using current rules.",
            "Beta band may be the predominant contributor with alpha and pre-beta contributions.",
        ],
    }
