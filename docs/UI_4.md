Task: Connect the form to the backend.

Create a service file services/api.ts.

Write a function predictViability(data: AssessmentFormData) that performs a POST request to http://<YOUR_IP>:8000/predict.

Update app/(tabs)/index.tsx to call this function on form submit.

Handle loading states (show a spinner on the button) and error handling (alert if API fails).

Note: Ensure the JSON body sent matches the snake_case expected by the Python backend (e.g., convert tissueStiffness to tissue_stiffness).