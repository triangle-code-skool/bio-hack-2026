import React, { useState } from 'react';
import {
  StyleSheet,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  View,
  Alert,
} from 'react-native';

import Colors from '@/constants/Colors';
import { useColorScheme } from '@/components/useColorScheme';
import {
  Card,
  FormInput,
  FormSlider,
  FormPicker,
  SegmentedControl,
  Button,
} from '@/components/ui';
import { ResultsView } from '@/components/ResultsView';
import {
  AssessmentFormData,
  initialFormData,
  OrganType,
  CauseOfDeath,
  EchogenicityGrade,
  AnalysisResult,
  mockAnalysisResult,
} from '@/types/assessment';
import { predictViability } from '@/services/api';

const ORGAN_TYPES: OrganType[] = ['Kidney', 'Liver', 'Heart', 'Lung'];
const CAUSES_OF_DEATH: CauseOfDeath[] = ['Trauma', 'CVA', 'Anoxia', 'Other'];
const ECHOGENICITY_GRADES: EchogenicityGrade[] = [1, 2, 3, 4, 5];

// Set to true to use mock data instead of real API
const USE_MOCK_API = false;

export default function NewAssessmentScreen() {
  const colorScheme = useColorScheme();
  const colors = Colors[colorScheme ?? 'light'];
  const [formData, setFormData] = useState<AssessmentFormData>(initialFormData);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [showResults, setShowResults] = useState(false);

  const updateUltrasound = <K extends keyof AssessmentFormData['ultrasound']>(
    key: K,
    value: AssessmentFormData['ultrasound'][K]
  ) => {
    setFormData((prev) => ({
      ...prev,
      ultrasound: { ...prev.ultrasound, [key]: value },
    }));
  };

  const updateClinical = <K extends keyof AssessmentFormData['clinical']>(
    key: K,
    value: AssessmentFormData['clinical'][K]
  ) => {
    setFormData((prev) => ({
      ...prev,
      clinical: { ...prev.clinical, [key]: value },
    }));
  };

  // Track raw string values for inputs to preserve decimal points during typing
  const [rawInputs, setRawInputs] = useState<Record<string, string>>({});

  const parseNumericInput = (text: string, inputKey: string): number | null => {
    // Store the raw text to preserve trailing decimals (e.g., "0.")
    setRawInputs((prev) => ({ ...prev, [inputKey]: text }));

    if (text === '' || text === '.') return null;
    // Don't parse if text ends with a decimal (user is still typing)
    if (text.endsWith('.')) {
      const num = parseFloat(text.slice(0, -1));
      return isNaN(num) ? null : num;
    }
    const num = parseFloat(text);
    return isNaN(num) ? null : num;
  };

  const formatNumericValue = (value: number | null, inputKey: string): string => {
    // If we have a raw input that ends with a decimal, use it
    const rawInput = rawInputs[inputKey];
    if (rawInput !== undefined && (rawInput.endsWith('.') || rawInput === '.')) {
      return rawInput;
    }
    return value !== null ? String(value) : '';
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      let result: AnalysisResult;

      if (USE_MOCK_API) {
        // Simulate API delay with mock data
        await new Promise((resolve) => setTimeout(resolve, 1500));
        result = mockAnalysisResult;
      } else {
        // Call real API
        result = await predictViability(formData);
      }

      setAnalysisResult(result);
      setShowResults(true);
    } catch (error) {
      console.error('Analysis failed:', error);
      Alert.alert(
        'Analysis Failed',
        error instanceof Error
          ? error.message
          : 'Unable to connect to the prediction server. Please check your connection and try again.',
        [{ text: 'OK' }]
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNewAssessment = () => {
    setShowResults(false);
    setAnalysisResult(null);
    setFormData(initialFormData);
  };

  const handleCloseResults = () => {
    setShowResults(false);
  };

  return (
    <>
      <KeyboardAvoidingView
        style={styles.keyboardView}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <ScrollView
          style={[styles.scrollView, { backgroundColor: colors.backgroundSecondary }]}
          contentContainerStyle={styles.contentContainer}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          {/* Section 1: Ultrasound Metrics */}
          <Card title="Ultrasound Metrics">
            <FormInput
              label="Tissue Stiffness"
              value={formatNumericValue(formData.ultrasound.tissueStiffness, 'tissueStiffness')}
              onChangeText={(text) => updateUltrasound('tissueStiffness', parseNumericInput(text, 'tissueStiffness'))}
              placeholder="Enter value"
              keyboardType="decimal-pad"
              unit="kPa"
            />

            <FormInput
              label="Resistive Index (RI)"
              value={formatNumericValue(formData.ultrasound.resistiveIndex, 'resistiveIndex')}
              onChangeText={(text) => updateUltrasound('resistiveIndex', parseNumericInput(text, 'resistiveIndex'))}
              placeholder="0.0 - 1.0"
              keyboardType="decimal-pad"
            />

            <FormInput
              label="Shear Wave Velocity"
              value={formatNumericValue(formData.ultrasound.shearWaveVelocity, 'shearWaveVelocity')}
              onChangeText={(text) => updateUltrasound('shearWaveVelocity', parseNumericInput(text, 'shearWaveVelocity'))}
              placeholder="Enter value"
              keyboardType="decimal-pad"
              unit="m/s"
            />

            <FormSlider
              label="Perfusion Uniformity"
              value={formData.ultrasound.perfusionUniformity}
              onValueChange={(value) => updateUltrasound('perfusionUniformity', Math.round(value))}
              minimumValue={0}
              maximumValue={100}
              step={1}
              unit="%"
            />

            <SegmentedControl
              label="Echogenicity Grade"
              options={ECHOGENICITY_GRADES}
              selectedValue={formData.ultrasound.echogenicityGrade}
              onValueChange={(value) => updateUltrasound('echogenicityGrade', value)}
            />

            <FormSlider
              label="Edema Index"
              value={formData.ultrasound.edemaIndex}
              onValueChange={(value) => updateUltrasound('edemaIndex', Math.round(value))}
              minimumValue={0}
              maximumValue={10}
              step={1}
            />
          </Card>

          {/* Section 2: Clinical Metadata */}
          <Card title="Clinical Metadata">
            <FormPicker
              label="Organ Type"
              options={ORGAN_TYPES}
              selectedValue={formData.clinical.organType}
              onValueChange={(value) => updateClinical('organType', value)}
              placeholder="Select organ type"
            />

            <FormInput
              label="Cold Ischemia Time"
              value={formatNumericValue(formData.clinical.coldIschemiaTime, 'coldIschemiaTime')}
              onChangeText={(text) => updateClinical('coldIschemiaTime', parseNumericInput(text, 'coldIschemiaTime'))}
              placeholder="Enter hours"
              keyboardType="decimal-pad"
              unit="hrs"
            />

            <FormInput
              label="Warm Ischemia Time"
              value={formatNumericValue(formData.clinical.warmIschemiaTime, 'warmIschemiaTime')}
              onChangeText={(text) => updateClinical('warmIschemiaTime', parseNumericInput(text, 'warmIschemiaTime'))}
              placeholder="Enter minutes"
              keyboardType="numeric"
              unit="mins"
            />

            <FormInput
              label="Donor Age"
              value={formatNumericValue(formData.clinical.donorAge, 'donorAge')}
              onChangeText={(text) => updateClinical('donorAge', parseNumericInput(text, 'donorAge'))}
              placeholder="Enter age"
              keyboardType="numeric"
              unit="yrs"
            />

            <FormInput
              label="KDPI/DRI Score"
              value={formatNumericValue(formData.clinical.kdpiDriScore, 'kdpiDriScore')}
              onChangeText={(text) => updateClinical('kdpiDriScore', parseNumericInput(text, 'kdpiDriScore'))}
              placeholder="Enter percentile"
              keyboardType="numeric"
              unit="%"
            />

            <FormPicker
              label="Cause of Death"
              options={CAUSES_OF_DEATH}
              selectedValue={formData.clinical.causeOfDeath}
              onValueChange={(value) => updateClinical('causeOfDeath', value)}
              placeholder="Select cause"
            />
          </Card>

          {/* Footer: Submit Button */}
          <View style={styles.footer}>
            <Button
              title="Analyze Organ Viability"
              onPress={handleSubmit}
              loading={isSubmitting}
            />
          </View>
        </ScrollView>
      </KeyboardAvoidingView>

      {/* Results Modal */}
      <ResultsView
        visible={showResults}
        result={analysisResult}
        onClose={handleCloseResults}
        onNewAssessment={handleNewAssessment}
      />
    </>
  );
}

const styles = StyleSheet.create({
  keyboardView: {
    flex: 1,
  },
  scrollView: {
    flex: 1,
  },
  contentContainer: {
    padding: 16,
    paddingBottom: 40,
  },
  footer: {
    marginTop: 8,
  },
});
