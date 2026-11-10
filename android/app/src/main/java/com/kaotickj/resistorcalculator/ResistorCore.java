package com.kaotickj.resistorcalculator;

import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/** Faithful platform-independent port of the tables and arithmetic from resistanceCalculator.py. */
public final class ResistorCore {
    public static final String[] DIGIT = {"black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "gray", "white"};
    public static final String[] MULTIPLIER = {"black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "gray", "white", "gold", "silver"};
    public static final String[] TOLERANCE = {"brown", "red", "green", "blue", "violet", "gray", "gold", "silver"};
    public static final String[] TEMPCO = {"brown", "red", "orange", "yellow", "blue", "violet"};
    public static final Map<String, Integer> COLOR_HEX;
    private static final Map<String, Double> TOLERANCE_VALUES;
    private static final Map<String, Integer> TEMPCO_VALUES;

    static {
        Map<String, Integer> colors = new LinkedHashMap<>();
        colors.put("black", 0xFF17191D); colors.put("brown", 0xFF795548);
        colors.put("red", 0xFFD64545); colors.put("orange", 0xFFF28C28);
        colors.put("yellow", 0xFFF2CF43); colors.put("green", 0xFF36965B);
        colors.put("blue", 0xFF3478C9); colors.put("violet", 0xFF8255B8);
        colors.put("gray", 0xFF9CA3AF); colors.put("white", 0xFFF3F4F6);
        colors.put("gold", 0xFFD4AF37); colors.put("silver", 0xFFC0C0C0);
        COLOR_HEX = Collections.unmodifiableMap(colors);
        Map<String, Double> tolerance = new LinkedHashMap<>();
        tolerance.put("brown", 1.0); tolerance.put("red", 2.0);
        tolerance.put("green", 0.5); tolerance.put("blue", 0.25);
        tolerance.put("violet", 0.1); tolerance.put("gray", 0.01);
        tolerance.put("gold", 5.0); tolerance.put("silver", 10.0);
        TOLERANCE_VALUES = Collections.unmodifiableMap(tolerance);
        Map<String, Integer> tempco = new LinkedHashMap<>();
        tempco.put("brown", 100); tempco.put("red", 50);
        tempco.put("orange", 15); tempco.put("yellow", 25);
        tempco.put("blue", 10); tempco.put("violet", 5);
        TEMPCO_VALUES = Collections.unmodifiableMap(tempco);
    }

    private ResistorCore() { }

    public static final class Result {
        public final double ohms;
        public final double tolerancePercent;
        public final double minimumOhms;
        public final double maximumOhms;
        public final Integer tempcoPpm;

        private Result(double ohms, double tolerancePercent, Integer tempcoPpm) {
            this.ohms = ohms;
            this.tolerancePercent = tolerancePercent;
            this.minimumOhms = ohms * (1 - tolerancePercent / 100);
            this.maximumOhms = ohms * (1 + tolerancePercent / 100);
            this.tempcoPpm = tempcoPpm;
        }
    }

    public static String[] roles(int bands) {
        if (bands < 4 || bands > 6) throw new IllegalArgumentException("Band count must be 4, 5 or 6");
        int digits = bands == 4 ? 2 : 3;
        String[] result = new String[bands];
        result[0] = "1st significant digit";
        result[1] = "2nd significant digit";
        if (digits == 3) result[2] = "3rd significant digit";
        result[digits] = "Multiplier";
        result[digits + 1] = "Tolerance";
        if (bands == 6) result[5] = "Temperature coefficient";
        return result;
    }

    public static String[] options(int bands, int index) {
        if (bands < 4 || bands > 6 || index < 0 || index >= bands) {
            throw new IllegalArgumentException("Invalid band index");
        }
        if (index < (bands == 4 ? 2 : 3)) return DIGIT.clone();
        if (index == (bands == 4 ? 2 : 3)) return MULTIPLIER.clone();
        if (index == (bands == 4 ? 3 : 4)) return TOLERANCE.clone();
        return TEMPCO.clone();
    }

    public static Result calculate(int bands, String[] colors) {
        if (bands < 4 || bands > 6) throw new IllegalArgumentException("Band count must be 4, 5 or 6");
        if (colors == null || colors.length < bands) throw new IllegalArgumentException("Missing band colors");
        int digits = bands == 4 ? 2 : 3;
        int significant = 0;
        for (int i = 0; i < digits; i++) {
            int digit = Arrays.asList(DIGIT).indexOf(colors[i]);
            if (digit < 0) throw new IllegalArgumentException("Invalid digit color: " + colors[i]);
            significant = significant * 10 + digit;
        }
        int multiplierIndex = Arrays.asList(MULTIPLIER).indexOf(colors[digits]);
        if (multiplierIndex < 0) throw new IllegalArgumentException("Invalid multiplier color");
        int exponent = multiplierIndex < 10 ? multiplierIndex : (multiplierIndex == 10 ? -1 : -2);
        Double tolerance = TOLERANCE_VALUES.get(colors[digits + 1]);
        if (tolerance == null) throw new IllegalArgumentException("Invalid tolerance color");
        Integer tempco = null;
        if (bands == 6) {
            tempco = TEMPCO_VALUES.get(colors[5]);
            if (tempco == null) throw new IllegalArgumentException("Invalid temperature coefficient color");
        }
        return new Result(significant * Math.pow(10, exponent), tolerance, tempco);
    }

    public static String formatResistance(double value) {
        double abs = Math.abs(value);
        if (abs >= 1e9) return String.format(Locale.US, "%.2f GΩ", value / 1e9);
        if (abs >= 1e6) return String.format(Locale.US, "%.2f MΩ", value / 1e6);
        if (abs >= 1e3) return String.format(Locale.US, "%.2f kΩ", value / 1e3);
        return String.format(Locale.US, "%.2f Ω", value);
    }

    public static String formatPercent(double value) {
        return String.format(Locale.US, "%.2f", value).replaceAll("\\.?0+$", "");
    }

    public static String capitalized(String color) {
        return color.substring(0, 1).toUpperCase(Locale.US) + color.substring(1);
    }
}
