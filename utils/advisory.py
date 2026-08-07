def get_priority(risk):

    if risk >= 0.70:
        return "Critical", "🔴"

    elif risk >= 0.50:
        return "High", "🟠"

    elif risk >= 0.30:
        return "Moderate", "🟡"

    else:
        return "Low", "🟢"


def generate_advisory(hazard, infra, social, compound):

    advice = []

    ###################################################
    # Overall Priority
    ###################################################

    if compound >= 0.70:

        advice.append({
            "title": "Immediate Action Required",
            "icon": "🚨",
            "text":
            "This district exhibits extremely high compound disaster risk. "
            "Immediate preparedness measures and emergency resource allocation "
            "are recommended."
        })

    elif compound >= 0.50:

        advice.append({
            "title": "High Priority",
            "icon": "⚠",
            "text":
            "Maintain continuous monitoring and strengthen preparedness "
            "before future flood events."
        })

    elif compound >= 0.30:

        advice.append({
            "title": "Moderate Priority",
            "icon": "🟡",
            "text":
            "Routine monitoring is recommended together with gradual "
            "risk reduction planning."
        })

    else:

        advice.append({
            "title": "Low Priority",
            "icon": "🟢",
            "text":
            "Current compound risk is relatively low. Continue standard monitoring."
        })

    ###################################################
    # Hazard
    ###################################################

    if hazard >= 0.60:

        advice.append({

            "title":"Hazard Management",

            "icon":"🌧",

            "text":

            """Recommended actions:

• Improve flood forecasting

• Strengthen early warning systems

• Improve embankment monitoring

• Prepare evacuation shelters

• Increase emergency response readiness"""
        })

    ###################################################
    # Infrastructure
    ###################################################

    if infra >= 0.60:

        advice.append({

            "title":"Infrastructure Improvement",

            "icon":"🏗",

            "text":

            """Recommended actions:

• Upgrade drainage systems

• Improve road accessibility

• Protect power infrastructure

• Improve healthcare accessibility

• Strengthen communication systems"""
        })

    ###################################################
    # Social
    ###################################################

    if social >= 0.60:

        advice.append({

            "title":"Community Support",

            "icon":"👥",

            "text":

            """Recommended actions:

• Community awareness programmes

• Support vulnerable households

• Improve evacuation planning

• Improve sanitation

• Strengthen local disaster committees"""
        })

    ###################################################
    # Triple Exposure
    ###################################################

    if hazard >= 0.60 and infra >= 0.60 and social >= 0.60:

        advice.append({

            "title":"Integrated Intervention",

            "icon":"🔴",

            "text":

            """All three vulnerability dimensions are elevated.

This district should receive the highest priority for integrated disaster management rather than isolated interventions."""
        })

    return advice