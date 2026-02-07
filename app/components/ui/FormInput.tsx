import React from 'react';
import { View, Text, TextInput, StyleSheet } from 'react-native';
import Colors from '@/constants/Colors';
import { useColorScheme } from '@/components/useColorScheme';

interface FormInputProps {
    label: string;
    value: string;
    onChangeText: (text: string) => void;
    placeholder?: string;
    keyboardType?: 'default' | 'numeric' | 'decimal-pad';
    unit?: string;
}

export function FormInput({
    label,
    value,
    onChangeText,
    placeholder,
    keyboardType = 'default',
    unit,
}: FormInputProps) {
    const colorScheme = useColorScheme();
    const colors = Colors[colorScheme ?? 'light'];

    return (
        <View style={styles.container}>
            <Text style={[styles.label, { color: colors.text }]}>{label}</Text>
            <View style={styles.inputRow}>
                <TextInput
                    style={[
                        styles.input,
                        {
                            backgroundColor: colors.backgroundSecondary,
                            borderColor: colors.border,
                            color: colors.textDark,
                        },
                    ]}
                    value={value}
                    onChangeText={onChangeText}
                    placeholder={placeholder}
                    placeholderTextColor={colors.tabIconDefault}
                    keyboardType={keyboardType}
                />
                {unit && <Text style={[styles.unit, { color: colors.text }]}>{unit}</Text>}
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
    inputRow: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    input: {
        flex: 1,
        height: 48,
        borderRadius: 8,
        borderWidth: 1,
        paddingHorizontal: 12,
        fontSize: 16,
    },
    unit: {
        marginLeft: 8,
        fontSize: 14,
        fontWeight: '500',
        minWidth: 40,
    },
});
