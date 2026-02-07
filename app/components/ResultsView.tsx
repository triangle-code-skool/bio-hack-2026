import React from 'react';
import {
    View,
    Text,
    StyleSheet,
    Modal,
    TouchableOpacity,
    ScrollView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import Colors from '@/constants/Colors';
import { useColorScheme } from '@/components/useColorScheme';
import { AnalysisResult, Classification } from '@/types/assessment';
import { Button } from '@/components/ui';

interface ResultsViewProps {
    visible: boolean;
    result: AnalysisResult | null;
    onClose: () => void;
    onNewAssessment: () => void;
}

const getScoreColor = (score: number): string => {
    if (score >= 70) return '#22C55E'; // Green
    if (score >= 40) return '#F59E0B'; // Yellow/Orange
    return '#EF4444'; // Red
};

const getClassificationStyle = (classification: Classification) => {
    switch (classification) {
        case 'Accept':
            return { color: '#22C55E', icon: 'checkmark-circle' as const };
        case 'Marginal':
            return { color: '#F59E0B', icon: 'alert-circle' as const };
        case 'Decline':
            return { color: '#EF4444', icon: 'close-circle' as const };
    }
};

const formatRiskFactor = (factor: string): string => {
    // Convert snake_case to readable text
    return factor
        .split('_')
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
};

export function ResultsView({
    visible,
    result,
    onClose,
    onNewAssessment,
}: ResultsViewProps) {
    const colorScheme = useColorScheme();
    const colors = Colors[colorScheme ?? 'light'];

    if (!result) return null;

    const scoreColor = getScoreColor(result.viability_score);
    const classificationStyle = getClassificationStyle(result.classification);

    return (
        <Modal
            visible={visible}
            animationType="slide"
            presentationStyle="pageSheet"
            onRequestClose={onClose}
        >
            <View style={[styles.container, { backgroundColor: colors.background }]}>
                {/* Header */}
                <View style={styles.header}>
                    <TouchableOpacity onPress={onClose} style={styles.closeButton}>
                        <Ionicons name="close" size={28} color={colors.text} />
                    </TouchableOpacity>
                    <Text style={[styles.headerTitle, { color: colors.textDark }]}>
                        Analysis Results
                    </Text>
                    <View style={styles.closeButton} />
                </View>

                <ScrollView
                    contentContainerStyle={styles.content}
                    showsVerticalScrollIndicator={false}
                >
                    {/* Viability Score Circle */}
                    <View style={styles.scoreContainer}>
                        <View style={[styles.scoreCircle, { borderColor: scoreColor }]}>
                            <Text style={[styles.scoreValue, { color: scoreColor }]}>
                                {result.viability_score}
                            </Text>
                            <Text style={[styles.scoreLabel, { color: colors.text }]}>
                                Viability Score
                            </Text>
                        </View>
                    </View>

                    {/* Classification */}
                    <View style={styles.classificationContainer}>
                        <Ionicons
                            name={classificationStyle.icon}
                            size={32}
                            color={classificationStyle.color}
                        />
                        <Text
                            style={[styles.classificationText, { color: classificationStyle.color }]}
                        >
                            {result.classification}
                        </Text>
                    </View>

                    {/* Confidence */}
                    <View style={[styles.confidenceContainer, { backgroundColor: colors.backgroundSecondary }]}>
                        <Text style={[styles.confidenceLabel, { color: colors.text }]}>
                            Confidence Level
                        </Text>
                        <Text style={[styles.confidenceValue, { color: colors.textDark }]}>
                            {Math.round(result.confidence * 100)}%
                        </Text>
                    </View>

                    {/* Risk Factors */}
                    {result.risk_factors.length > 0 && (
                        <View style={[styles.riskContainer, { backgroundColor: '#FEF3C7', borderColor: '#F59E0B' }]}>
                            <View style={styles.riskHeader}>
                                <Ionicons name="warning" size={20} color="#F59E0B" />
                                <Text style={styles.riskTitle}>Risk Factors</Text>
                            </View>
                            {result.risk_factors.map((factor, index) => (
                                <View key={index} style={styles.riskItem}>
                                    <Text style={styles.bulletPoint}>•</Text>
                                    <Text style={styles.riskText}>{formatRiskFactor(factor)}</Text>
                                </View>
                            ))}
                        </View>
                    )}
                </ScrollView>

                {/* Footer Actions */}
                <View style={[styles.footer, { borderTopColor: colors.border }]}>
                    <Button
                        title="New Assessment"
                        onPress={onNewAssessment}
                        style={{ flex: 1 }}
                    />
                </View>
            </View>
        </Modal>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    header: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingHorizontal: 16,
        paddingVertical: 12,
        borderBottomWidth: 1,
        borderBottomColor: '#E2E8F0',
    },
    closeButton: {
        width: 44,
        height: 44,
        alignItems: 'center',
        justifyContent: 'center',
    },
    headerTitle: {
        fontSize: 18,
        fontWeight: '600',
    },
    content: {
        padding: 24,
        alignItems: 'center',
    },
    scoreContainer: {
        marginBottom: 32,
    },
    scoreCircle: {
        width: 180,
        height: 180,
        borderRadius: 90,
        borderWidth: 8,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'transparent',
    },
    scoreValue: {
        fontSize: 56,
        fontWeight: '700',
    },
    scoreLabel: {
        fontSize: 14,
        fontWeight: '500',
        marginTop: 4,
    },
    classificationContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 24,
    },
    classificationText: {
        fontSize: 28,
        fontWeight: '700',
        marginLeft: 8,
    },
    confidenceContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        width: '100%',
        padding: 16,
        borderRadius: 12,
        marginBottom: 24,
    },
    confidenceLabel: {
        fontSize: 16,
        fontWeight: '500',
    },
    confidenceValue: {
        fontSize: 20,
        fontWeight: '600',
    },
    riskContainer: {
        width: '100%',
        padding: 16,
        borderRadius: 12,
        borderWidth: 1,
        marginBottom: 24,
    },
    riskHeader: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 12,
    },
    riskTitle: {
        fontSize: 16,
        fontWeight: '600',
        color: '#92400E',
        marginLeft: 8,
    },
    riskItem: {
        flexDirection: 'row',
        alignItems: 'flex-start',
        marginBottom: 8,
    },
    bulletPoint: {
        fontSize: 16,
        color: '#92400E',
        marginRight: 8,
        lineHeight: 22,
    },
    riskText: {
        flex: 1,
        fontSize: 14,
        color: '#92400E',
        lineHeight: 22,
    },
    footer: {
        padding: 16,
        borderTopWidth: 1,
    },
});
