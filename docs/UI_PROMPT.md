I am building the frontend for a hackathon project called UltraViab.

Tech Stack:

Framework: React Native with Expo (Managed Workflow)

Language: TypeScript

Navigation: Expo Router (File-based routing)

Styling: StyleSheet (Keep it clean, clinical, and minimal)

Project Goal: A mobile app for real-time organ viability assessment using ultrasound-derived features.

Directory Structure:

Plaintext
mobile/
├── app/
│   ├── (tabs)/
│   │   ├── index.tsx     # Home / Assessment Input Form
│   │   └── history.tsx   # History List
│   └── _layout.tsx       # Root layout
Data Requirements: The app needs to collect specific inputs to send to a backend API.

Ultrasound Features: Tissue Stiffness (kPa), Resistive Index (RI), Shear Wave Velocity (m/s), Perfusion Uniformity (%), Echogenicity Grade (1-5), Edema Index (0-10).

Clinical Metadata: Cold Ischemia Time (hours), Organ Type (Kidney/Liver/Heart/Lung), Donor Age (years), KDPI/DRI (percentile), Cause of Death (Categorical), Warm Ischemia Time (min).

Please acknowledge you understand the stack and data requirements.

Task: Set up the basic navigation structure using Expo Router.

Create a root app/_layout.tsx that sets up the Stack.

Create app/(tabs)/_layout.tsx to handle the tab navigation. Use a "Medical/Health" icon for the Home tab and a "Clock/History" icon for the History tab.

Create placeholder screens for app/(tabs)/index.tsx (Title: "New Assessment") and app/(tabs)/history.tsx (Title: "Assessment History").

Ensure the color theme uses a clinical palette: Primary Blue (#007AFF), Clean White backgrounds, and Slate Gray text.