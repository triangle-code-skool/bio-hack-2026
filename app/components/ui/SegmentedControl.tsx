import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import Colors from '@/constants/Colors';
import { useColorScheme } from '@/components/useColorScheme';

interface SegmentedControlProps<T extends string | number> {
    label: string;
    options: T[];
    selectedValue: T;
    onValueChange: (value: T) => void;
    renderOption?: (option: T) => string;
}

export function SegmentedControl<T extends string | number>({
    label,
    options,
    selectedValue,
    onValueChange,
    renderOption,
}: SegmentedControlProps<T>) {
    const colorScheme = useColorScheme();
    const colors = Colors[colorScheme ?? 'light'];

    return (
        <View style={styles.container}>
            <Text style={[styles.label, { color: colors.text }]}>{label}</Text>
            <View style={[styles.segmentContainer, { backgroundColor: colors.backgroundSecondary, borderColor: colors.border }]}>
                {options.map((option, index) => {
                    const isSelected = option === selectedValue;
                    return (
                        <TouchableOpacity
                            key={String(option)}
                            style={[
                                styles.segment,
                                isSelected && { backgroundColor: colors.tint },
                                index === 0 && styles.firstSegment,
                                index === options.length - 1 && styles.lastSegment,
                            ]}
                            onPress={() => onValueChange(option)}
                            activeOpacity={0.7}
                        >
                            <Text
                                style={[
                                    styles.segmentText,
                                    { color: isSelected ? '#FFFFFF' : colors.text },
                                ]}
                            >
                                {renderOption ? renderOption(option) : String(option)}
                            </Text>
                        </TouchableOpacity>
                    );
                })}
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        marginBottom: 16,
    },
    label: {
        fontSize: 14,
        fontWeight: '500',
        marginBottom: 8,
    },
    segmentContainer: {
        flexDirection: 'row',
        borderRadius: 8,
        borderWidth: 1,
        overflow: 'hidden',
    },
    segment: {
        flex: 1,
        paddingVertical: 12,
        alignItems: 'center',
        justifyContent: 'center',
    },
    firstSegment: {
        borderTopLeftRadius: 7,
        borderBottomLeftRadius: 7,
    },
    lastSegment: {
        borderTopRightRadius: 7,
        borderBottomRightRadius: 7,
    },
    segmentText: {
        fontSize: 14,
        fontWeight: '500',
    },
});
