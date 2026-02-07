Build the Assessment Form in app/(tabs)/index.tsx.

Please create a scrollable form using ScrollView and KeyboardAvoidingView. The form needs to capture the following state. Use appropriate input types for each:

Section 1: Ultrasound Metrics (Group these visually in a Card)

Tissue Stiffness (kPa): Numeric input.

Resistive Index (RI): Numeric input (decimal).

Shear Wave Velocity (m/s): Numeric input.

Perfusion Uniformity (%): Slider or Numeric input (0-100).

Echogenicity Grade: Segmented Control or Dropdown (1 to 5).

Edema Index: Slider or Stepper (0 to 10).

Section 2: Clinical Metadata (Group these visually in a second Card)

Organ Type: Dropdown/Picker (Options: Kidney, Liver, Heart, Lung).

Cold Ischemia Time (hrs): Numeric input.

Warm Ischemia Time (mins): Numeric input.

Donor Age: Numeric input.

KDPI/DRI Score: Numeric input.

Cause of Death: Dropdown (Options: Trauma, CVA, Anoxia, Other).

Footer:

Add a large, high-contrast "Analyze Organ Viability" button at the bottom.

Define a TypeScript interface named AssessmentFormData for this state.