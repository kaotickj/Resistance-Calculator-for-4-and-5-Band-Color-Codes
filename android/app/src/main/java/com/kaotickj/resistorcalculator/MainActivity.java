package com.kaotickj.resistorcalculator;

import android.app.Activity;
import android.app.AlertDialog;
import android.os.Bundle;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.RectF;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.PopupMenu;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.ScrollView;
import android.widget.TextView;

import java.util.Arrays;

/** Touch-friendly, offline Android UI for the original PyQt6 calculator. */
public final class MainActivity extends Activity {
    private static final int BACKGROUND = 0xFF111318;
    private static final int CARD = 0xFF1A1D24;
    private static final int CARD_EDGE = 0xFF292E38;
    private static final int TEXT = 0xFFF4F6F8;
    private static final int MUTED = 0xFF9DA6B3;
    private static final int GREEN = 0xFF71CF8B;
    private static final int ACTION = 0xFF39764B;

    private int bandCount = 4;
    private final String[] colors = new String[6];
    private final LinearLayout[] bandRows = new LinearLayout[6];
    private final TextView[] colorButtons = new TextView[6];
    private final TextView[] roleLabels = new TextView[6];
    private final RadioButton[] modes = new RadioButton[3];
    private ResistorView preview;
    private TextView valueView;
    private TextView toleranceView;
    private TextView rangeView;
    private TextView tempcoView;
    private boolean isInitializing = true;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setStatusBarColor(BACKGROUND);
        getWindow().setNavigationBarColor(BACKGROUND);
        if (state != null) {
            bandCount = state.getInt("bands", 4);
            String[] saved = state.getStringArray("colors");
            if (saved != null) System.arraycopy(saved, 0, colors, 0, Math.min(6, saved.length));
        }
        buildUi();
        isInitializing = false;
        setMode(bandCount);
    }

    @Override protected void onSaveInstanceState(Bundle state) {
        super.onSaveInstanceState(state);
        state.putInt("bands", bandCount);
        state.putStringArray("colors", colors.clone());
    }

    private int dp(float value) { return Math.round(value * getResources().getDisplayMetrics().density); }

    private GradientDrawable rounded(int fill, int stroke, int corner) {
        GradientDrawable d = new GradientDrawable();
        d.setColor(fill);
        d.setCornerRadius(dp(corner));
        if (stroke != 0) d.setStroke(dp(1), stroke);
        return d;
    }

    private TextView label(String value, float sp, int color, boolean bold) {
        TextView t = new TextView(this);
        t.setText(value);
        t.setTextColor(color);
        t.setTextSize(sp);
        if (bold) t.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        return t;
    }

    private LinearLayout column() {
        LinearLayout l = new LinearLayout(this);
        l.setOrientation(LinearLayout.VERTICAL);
        return l;
    }

    private LinearLayout row() {
        LinearLayout l = new LinearLayout(this);
        l.setOrientation(LinearLayout.HORIZONTAL);
        l.setGravity(Gravity.CENTER_VERTICAL);
        return l;
    }

    private LinearLayout card(LinearLayout parent) {
        LinearLayout c = column();
        c.setBackground(rounded(CARD, CARD_EDGE, 14));
        c.setPadding(dp(16), dp(16), dp(16), dp(16));
        LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(-1, -2);
        p.bottomMargin = dp(14);
        parent.addView(c, p);
        return c;
    }

    private void buildUi() {
        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setBackgroundColor(BACKGROUND);
        scroll.setClipToPadding(false);
        LinearLayout content = column();
        content.setPadding(dp(16), dp(16), dp(16), dp(28));
        scroll.addView(content, new ScrollView.LayoutParams(-1, -2));
        setContentView(scroll);

        // App title, subtitle, and options.
        LinearLayout heading = row();
        LinearLayout headingText = column();
        TextView title = label("Resistor Color Code", 25, TEXT, true);
        headingText.addView(title);
        TextView subtitle = label("Resistance • Tolerance • Temperature", 12, MUTED, false);
        LinearLayout.LayoutParams sub = new LinearLayout.LayoutParams(-1, -2);
        sub.topMargin = dp(5);
        headingText.addView(subtitle, sub);
        heading.addView(headingText, new LinearLayout.LayoutParams(0, -2, 1));
        TextView menu = label("⋮", 28, TEXT, false);
        menu.setGravity(Gravity.CENTER);
        menu.setContentDescription("Help and about menu");
        menu.setBackground(rounded(0xFF242832, CARD_EDGE, 10));
        heading.addView(menu, new LinearLayout.LayoutParams(dp(46), dp(46)));
        menu.setOnClickListener(v -> showMenu(menu));
        LinearLayout.LayoutParams hp = new LinearLayout.LayoutParams(-1, -2);
        hp.bottomMargin = dp(20);
        content.addView(heading, hp);

        // Mode chooser.
        LinearLayout modeCard = card(content);
        modeCard.addView(label("Resistor type", 15, TEXT, true));
        RadioGroup modeGroup = new RadioGroup(this);
        modeGroup.setOrientation(RadioGroup.HORIZONTAL);
        LinearLayout.LayoutParams modesParams = new LinearLayout.LayoutParams(-1, -2);
        modesParams.topMargin = dp(12);
        modeCard.addView(modeGroup, modesParams);
        int[] choices = {4, 5, 6};
        for (int i = 0; i < 3; i++) {
            final int count = choices[i];
            RadioButton b = new RadioButton(this);
            b.setText(count + " bands");
            b.setTextSize(13);
            b.setTextColor(TEXT);
            b.setButtonTintList(android.content.res.ColorStateList.valueOf(GREEN));
            b.setId(View.generateViewId());
            modes[i] = b;
            modeGroup.addView(b, new RadioGroup.LayoutParams(0, dp(48), 1));
            b.setOnClickListener(v -> {
                if (!isInitializing && bandCount != count) {
                    Arrays.fill(colors, null);
                    setMode(count);
                }
            });
        }

        // Six possible band selectors. Rows remain the same view instances between modes.
        LinearLayout bandCard = card(content);
        bandCard.addView(label("Color bands", 17, TEXT, true));
        TextView hint = label("Tap a color to select its band", 12, MUTED, false);
        LinearLayout.LayoutParams hintP = new LinearLayout.LayoutParams(-1, -2);
        hintP.topMargin = dp(5);
        hintP.bottomMargin = dp(9);
        bandCard.addView(hint, hintP);
        for (int i = 0; i < 6; i++) {
            final int index = i;
            LinearLayout bandRow = row();
            bandRow.setMinimumHeight(dp(62));
            LinearLayout labels = column();
            labels.addView(label("Band " + (i + 1), 14, TEXT, true));
            TextView role = label("", 11, MUTED, false);
            labels.addView(role);
            roleLabels[i] = role;
            bandRow.addView(labels, new LinearLayout.LayoutParams(0, -2, 1));
            TextView chooser = label("", 14, TEXT, true);
            chooser.setGravity(Gravity.CENTER);
            chooser.setMinimumHeight(dp(44));
            chooser.setPadding(dp(10), 0, dp(10), 0);
            chooser.setOnClickListener(v -> chooseColor(index));
            colorButtons[i] = chooser;
            bandRow.addView(chooser, new LinearLayout.LayoutParams(dp(136), -2));
            bandRows[i] = bandRow;
            bandCard.addView(bandRow, new LinearLayout.LayoutParams(-1, -2));
        }

        // Live resistor drawing.
        LinearLayout previewCard = card(content);
        previewCard.addView(label("Preview", 17, TEXT, true));
        preview = new ResistorView(this);
        LinearLayout.LayoutParams previewParams = new LinearLayout.LayoutParams(-1, dp(110));
        previewParams.topMargin = dp(8);
        previewCard.addView(preview, previewParams);

        // Live engineering results.
        LinearLayout resultCard = card(content);
        resultCard.setBackground(rounded(0xFF171D19, 0xFF31523A, 14));
        TextView resultTitle = label("CALCULATED VALUE", 12, 0xFF8FA898, true);
        resultTitle.setGravity(Gravity.CENTER);
        resultCard.addView(resultTitle);
        valueView = label("—", 29, GREEN, true);
        valueView.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams vparams = new LinearLayout.LayoutParams(-1, -2);
        vparams.topMargin = dp(9);
        vparams.bottomMargin = dp(9);
        resultCard.addView(valueView, vparams);
        toleranceView = detail(resultCard);
        rangeView = detail(resultCard);
        tempcoView = detail(resultCard);

        Button calculate = new Button(this);
        calculate.setText("Calculate");
        calculate.setAllCaps(false);
        calculate.setTextSize(15);
        calculate.setTextColor(0xFFFFFFFF);
        calculate.setBackground(rounded(ACTION, 0xFF498C5D, 10));
        content.addView(calculate, new LinearLayout.LayoutParams(-1, dp(52)));
        calculate.setOnClickListener(v -> calculate());
    }

    private TextView detail(LinearLayout parent) {
        TextView t = label("", 13, 0xFFC5CEC8, false);
        t.setGravity(Gravity.CENTER);
        t.setPadding(0, dp(3), 0, dp(3));
        parent.addView(t, new LinearLayout.LayoutParams(-1, -2));
        return t;
    }

    private void setMode(int count) {
        if (count < 4 || count > 6) count = 4;
        bandCount = count;
        modes[count - 4].setChecked(true);
        String[] roles = ResistorCore.roles(count);
        for (int i = 0; i < 6; i++) {
            boolean visible = i < count;
            bandRows[i].setVisibility(visible ? View.VISIBLE : View.GONE);
            if (!visible) continue;
            roleLabels[i].setText(roles[i]);
            String[] valid = ResistorCore.options(count, i);
            if (!Arrays.asList(valid).contains(colors[i])) colors[i] = valid[0];
            refreshChip(i);
        }
        preview.invalidate();
        calculate();
    }

    private void refreshChip(int index) {
        String color = colors[index];
        if (color == null) return;
        TextView chip = colorButtons[index];
        chip.setText("●  " + ResistorCore.capitalized(color) + "  ▾");
        chip.setBackground(rounded(ResistorCore.COLOR_HEX.get(color), 0xFF58606A, 9));
        boolean darkText = Arrays.asList("yellow", "orange", "gray", "white", "gold", "silver").contains(color);
        chip.setTextColor(darkText ? 0xFF151515 : 0xFFFFFFFF);
        chip.setContentDescription("Band " + (index + 1) + ", " + color + ". Tap to change.");
    }

    private void chooseColor(int index) {
        final String[] available = ResistorCore.options(bandCount, index);
        final ListView list = new ListView(this);
        list.setDividerHeight(0);
        list.setBackgroundColor(CARD);
        list.setAdapter(new BaseAdapter() {
            @Override public int getCount() { return available.length; }
            @Override public Object getItem(int position) { return available[position]; }
            @Override public long getItemId(int position) { return position; }
            @Override public View getView(int position, View convert, ViewGroup parent) {
                String color = available[position];
                LinearLayout item = row();
                item.setPadding(dp(16), 0, dp(16), 0);
                item.setMinimumHeight(dp(52));
                TextView swatch = label("", 12, TEXT, false);
                swatch.setBackground(rounded(ResistorCore.COLOR_HEX.get(color), 0xFF808080, 30));
                item.addView(swatch, new LinearLayout.LayoutParams(dp(25), dp(25)));
                TextView name = label(ResistorCore.capitalized(color), 15, TEXT, false);
                LinearLayout.LayoutParams nameP = new LinearLayout.LayoutParams(0, -2, 1);
                nameP.leftMargin = dp(14);
                item.addView(name, nameP);
                if (color.equals(colors[index])) item.addView(label("✓", 21, GREEN, true));
                return item;
            }
        });
        AlertDialog dialog = new AlertDialog.Builder(this)
                .setTitle("Band " + (index + 1) + " • " + ResistorCore.roles(bandCount)[index])
                .setView(list)
                .setNegativeButton("Cancel", (d, which) -> d.dismiss())
                .create();
        list.setOnItemClickListener((parent, view, position, id) -> {
            colors[index] = available[position];
            refreshChip(index);
            preview.invalidate();
            calculate();
            dialog.dismiss();
        });
        dialog.show();
    }

    private void calculate() {
        try {
            ResistorCore.Result r = ResistorCore.calculate(bandCount, colors);
            valueView.setText(ResistorCore.formatResistance(r.ohms));
            toleranceView.setText("Tolerance   ±" + ResistorCore.formatPercent(r.tolerancePercent) + "%");
            rangeView.setText("Range   " + ResistorCore.formatResistance(r.minimumOhms)
                    + "  –  " + ResistorCore.formatResistance(r.maximumOhms));
            if (r.tempcoPpm == null) {
                tempcoView.setText("");
                tempcoView.setVisibility(View.GONE);
            } else {
                tempcoView.setText("Temperature coefficient   " + r.tempcoPpm + " ppm/°C");
                tempcoView.setVisibility(View.VISIBLE);
            }
        } catch (IllegalArgumentException ex) {
            valueView.setText("—");
            toleranceView.setText("");
            rangeView.setText("");
            tempcoView.setText("");
        }
    }

    private void showMenu(View anchor) {
        PopupMenu popup = new PopupMenu(this, anchor);
        popup.getMenu().add(0, 1, 0, "Usage instructions");
        popup.getMenu().add(0, 2, 1, "About");
        popup.setOnMenuItemClickListener(item -> {
            if (item.getItemId() == 1) showHelp();
            else showAbout();
            return true;
        });
        popup.show();
    }

    private void showHelp() {
        new AlertDialog.Builder(this)
                .setTitle("Usage instructions")
                .setMessage("Select a resistor type, then tap each band to select its color. The result updates automatically.\n\n"
                        + "4-band resistor\nBands 1–2: Significant digits\nBand 3: Multiplier\nBand 4: Tolerance\n\n"
                        + "5-band resistor\nBands 1–3: Significant digits\nBand 4: Multiplier\nBand 5: Tolerance\n\n"
                        + "6-band resistor\nBands 1–3: Significant digits\nBand 4: Multiplier\nBand 5: Tolerance\nBand 6: Temperature coefficient\n\n"
                        + "Orient the resistor so the separated tolerance band is near the right-hand end.")
                .setPositiveButton("Close", null).show();
    }

    private void showAbout() {
        new AlertDialog.Builder(this)
                .setTitle("Resistor Color Code Calculator")
                .setMessage("Version 3.0 (Android edition)\n\nDeveloped by Kaotick Jay\n"
                        + "github.com/kaotickj\n\n"
                        + "Android adaptation of the original Python/PyQt6 resistor calculator.\n"
                        + "Offline functionality. No permissions or advertisements.\n\n"
                        + "Licensed under the MIT License.")
                .setPositiveButton("Close", null).show();
    }

    /** Scalable canvas preview with lead wires and live selected color bands. */
    private final class ResistorView extends View {
        private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
        ResistorView(Context context) { super(context); setImportantForAccessibility(View.IMPORTANT_FOR_ACCESSIBILITY_YES); }

        @Override protected void onDraw(Canvas canvas) {
            super.onDraw(canvas);
            float w = getWidth(), h = getHeight();
            float left = w * .11f, right = w * .89f;
            float cy = h * .50f;
            paint.setStyle(Paint.Style.FILL);
            paint.setColor(0xFF707782);
            canvas.drawRoundRect(new RectF(0, cy - dp(2), w, cy + dp(2)), dp(2), dp(2), paint);
            paint.setColor(0xFF91856B);
            canvas.drawRoundRect(new RectF(left, cy - dp(34), right, cy + dp(34)), dp(25), dp(25), paint);
            paint.setColor(0xFFD6C69F);
            canvas.drawRoundRect(new RectF(left + dp(2), cy - dp(32), right - dp(2), cy + dp(32)), dp(23), dp(23), paint);
            float bandW = Math.max(dp(10), Math.min(dp(16), (right - left) * .065f));
            float firstX = left + (right - left) * .14f;
            float step = (right - left) * .72f / (bandCount - 1);
            for (int i = 0; i < bandCount; i++) {
                Integer shade = ResistorCore.COLOR_HEX.get(colors[i]);
                if (shade == null) continue;
                float x = firstX + i * step;
                paint.setColor(shade);
                canvas.drawRoundRect(new RectF(x - bandW / 2, cy - dp(29), x + bandW / 2, cy + dp(29)), dp(2), dp(2), paint);
            }
        }
    }
}
