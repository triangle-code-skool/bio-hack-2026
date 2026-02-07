/**
 * UltraViab Clinical Color Palette
 * Primary Blue (#007AFF), Clean White backgrounds, Slate Gray text
 */

const primaryBlue = "#007AFF";
const slateGray = "#64748B";
const cleanWhite = "#FFFFFF";
const lightGray = "#F8FAFC";

export default {
  primary: primaryBlue,
  text: slateGray,
  textDark: "#1E293B",
  background: cleanWhite,
  backgroundSecondary: lightGray,
  border: "#E2E8F0",
  success: "#22C55E",
  warning: "#F59E0B",
  error: "#EF4444",
  light: {
    text: slateGray,
    textDark: "#1E293B",
    background: cleanWhite,
    backgroundSecondary: lightGray,
    tint: primaryBlue,
    tabIconDefault: "#CBD5E1",
    tabIconSelected: primaryBlue,
    border: "#E2E8F0",
  },
  dark: {
    text: "#E2E8F0",
    textDark: "#F8FAFC",
    background: "#0F172A",
    backgroundSecondary: "#1E293B",
    tint: primaryBlue,
    tabIconDefault: "#475569",
    tabIconSelected: primaryBlue,
    border: "#334155",
  },
};
