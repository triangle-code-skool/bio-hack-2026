import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Modal, FlatList } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import Colors from '@/constants/Colors';
import { useColorScheme } from '@/components/useColorScheme';

interface FormPickerProps<T extends string> {
    label: string;
    options: T[];
    selectedValue: T | null;
    onValueChange: (value: T) => void;
    placeholder?: string;
}

export function FormPicker<T extends string>({
    label,
    options,
    selectedValue,
    onValueChange,
    placeholder = 'Select an option',
}: FormPickerProps<T>) {
    const colorScheme = useColorScheme();
    const colors = Colors[colorScheme ?? 'light'];
    const [isOpen, setIsOpen] = useState(false);

    return (
        <View style={styles.container}>
            <Text style={[styles.label, { color: colors.text }]}>{label}</Text>
            <TouchableOpacity
                style={[
                    styles.picker,
                    { backgroundColor: colors.backgroundSecondary, borderColor: colors.border },
                ]}
                onPress={() => setIsOpen(true)}
                activeOpacity={0.7}
            >
                <Text
                    style={[
                        styles.pickerText,
                        { color: selectedValue ? colors.textDark : colors.tabIconDefault },
                    ]}
                >
                    {selectedValue ?? placeholder}
                </Text>
                <Ionicons name="chevron-down" size={20} color={colors.text} />
            </TouchableOpacity>

            <Modal visible={isOpen} transparent animationType="fade">
                <TouchableOpacity
                    style={styles.modalOverlay}
                    activeOpacity={1}
                    onPress={() => setIsOpen(false)}
                >
                    <View style={[styles.modalContent, { backgroundColor: colors.background }]}>
                        <Text style={[styles.modalTitle, { color: colors.textDark }]}>{label}</Text>
                        <FlatList
                            data={options}
                            keyExtractor={(item) => item}
                            renderItem={({ item }) => (
                                <TouchableOpacity
                                    style={[
                                        styles.option,
                                        { borderBottomColor: colors.border },
                                        item === selectedValue && { backgroundColor: colors.backgroundSecondary },
                                    ]}
                                    onPress={() => {
                                        onValueChange(item);
                                        setIsOpen(false);
                                    }}
                                >
                                    <Text style={[styles.optionText, { color: colors.textDark }]}>{item}</Text>
                                    {item === selectedValue && (
                                        <Ionicons name="checkmark" size={20} color={colors.tint} />
                                    )}
                                </TouchableOpacity>
                            )}
                        />
                    </View>
                </TouchableOpacity>
            </Modal>
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
    picker: {
        height: 48,
        borderRadius: 8,
        borderWidth: 1,
        paddingHorizontal: 12,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
    },
    pickerText: {
        fontSize: 16,
    },
    modalOverlay: {
        flex: 1,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        justifyContent: 'center',
        alignItems: 'center',
    },
    modalContent: {
        width: '80%',
        maxHeight: '60%',
        borderRadius: 12,
        paddingVertical: 16,
    },
    modalTitle: {
        fontSize: 18,
        fontWeight: '600',
        paddingHorizontal: 16,
        paddingBottom: 12,
    },
    option: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingVertical: 14,
        paddingHorizontal: 16,
        borderBottomWidth: 1,
    },
    optionText: {
        fontSize: 16,
    },
});
