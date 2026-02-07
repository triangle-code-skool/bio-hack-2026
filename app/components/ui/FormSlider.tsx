import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import Slider from '@react-native-community/slider';
import Colors from '@/constants/Colors';
import { useColorScheme } from '@/components/useColorScheme';

interface FormSliderProps {
    label: string;
    value: number;
    onValueChange: (value: number) => void;
    minimumValue: number;
    maximumValue: number;
    step?: number;
    unit?: string;
}

export function FormSlider({
    label,
    value,
    onValueChange,
    minimumValue,
    maximumValue,
    step = 1,
    unit,
}: FormSliderProps) {
    const colorScheme = useColorScheme();
    const colors = Colors[colorScheme ?? 'light'];

    return (
        <View style={styles.container}>
            <View style={styles.labelRow}>
                <Text style={[styles.label, { color: colors.text }]}>{label}</Text>
                <Text style={[styles.value, { color: colors.textDark }]}>
                    {value}{unit}
                </Text>
            </View>
            <Slider
                style={styles.slider}
                value={value}
                onValueChange={onValueChange}
                minimumValue={minimumValue}
                maximumValue={maximumValue}
                step={step}
                minimumTrackTintColor={colors.tint}
                maximumTrackTintColor={colors.border}
                thumbTintColor={colors.tint}
            />
            <View style={styles.rangeRow}>
                <Text style={[styles.rangeText, { color: colors.tabIconDefault }]}>{minimumValue}</Text>
                <Text style={[styles.rangeText, { color: colors.tabIconDefault }]}>{maximumValue}</Text>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        marginBottom: 16,
    },
    labelRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 8,
    },
    label: {
        fontSize: 14,
        fontWeight: '500',
    },
    value: {
        fontSize: 16,
        fontWeight: '600',
    },
    slider: {
        width: '100%',
        height: 40,
    },
    rangeRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
    },
    rangeText: {
        fontSize: 12,
    },
});
