Task: Create a Results View component to display the analysis.

When the user submits the form, mock a successful API response for now.

Mock Response Structure:

JSON
{
  "viability_score": 78,
  "classification": "Accept",
  "confidence": 0.89,
  "risk_factors": ["cold_ischemia_hours approaching threshold"]
}
UI Requirements:

Display the Viability Score (0-100) prominently inside a large circle.

Color Coding: If score > 70 use Green; 40-69 use Yellow/Orange; < 40 use Red.

Display the Classification text ("Accept", "Marginal", "Decline") clearly below the score.

Display Risk Factors as a bulleted warning list if any exist.

Make this view a Modal or a conditionally rendered component that overlays the form when analysis is complete.