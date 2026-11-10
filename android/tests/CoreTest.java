import com.kaotickj.resistorcalculator.ResistorCore;
import java.util.Arrays;

public final class CoreTest {
    private static int assertions;
    private static void check(boolean yes, String msg) {
        if (!yes) throw new AssertionError(msg);
        assertions++;
    }
    private static void close(double got, double want, String label) {
        check(Math.abs(got - want) < Math.max(.00000001, Math.abs(want) * .0000000001), label + " expected " + want + " got " + got);
    }
    private static void caseOf(int count, double ohms, double percent, Integer tempco, String... colors) {
        ResistorCore.Result r = ResistorCore.calculate(count, colors);
        close(r.ohms, ohms, "ohms");
        close(r.tolerancePercent, percent, "tolerance");
        close(r.minimumOhms, ohms * (1-percent/100), "min");
        close(r.maximumOhms, ohms * (1+percent/100), "max");
        check(tempco == null ? r.tempcoPpm == null : tempco.equals(r.tempcoPpm), "tempco");
    }
    public static void main(String[] args) {
        for (int bands = 4; bands <= 6; bands++) {
            String[] roles = ResistorCore.roles(bands);
            int digits = bands == 4 ? 2 : 3;
            check(roles.length == bands, "roles length");
            check("Multiplier".equals(roles[digits]), "multiplier role " + bands);
            check("Tolerance".equals(roles[digits + 1]), "tolerance role " + bands);
            for (int i = 0; i < bands; i++) {
                check(roles[i] != null, "missing role " + bands + "/" + i);
                check(ResistorCore.options(bands, i).length > 0, "no choices");
            }
        }
        caseOf(4, 270, 5, null, "red", "violet", "brown", "gold");
        caseOf(4, 4.7, 10, null, "yellow", "violet", "gold", "silver");
        caseOf(4, 0.10, 0.01, null, "brown", "black", "silver", "gray");
        caseOf(5, 10000, 1, null, "brown", "black", "black", "red", "brown");
        caseOf(5, 1000, 0.5, null, "brown", "black", "black", "brown", "green");
        caseOf(6, 100000, 1, 5, "brown", "black", "black", "orange", "brown", "violet");
        caseOf(6, 1.00, 0.25, 10, "brown", "black", "black", "silver", "blue", "blue");
        check(ResistorCore.formatResistance(1e3).equals("1.00 kΩ"), "kilo formatting");
        check(ResistorCore.formatResistance(1e6).equals("1.00 MΩ"), "mega formatting");
        check(ResistorCore.formatResistance(1e9).equals("1.00 GΩ"), "giga formatting");
        check(ResistorCore.formatPercent(.01).equals("0.01"), "percent precision");
        check(ResistorCore.formatPercent(10).equals("10"), "percent integer");
        boolean rejected = false;
        try { ResistorCore.calculate(4, new String[]{"gold","black","black","gold"}); }
        catch (IllegalArgumentException ex) { rejected = true; }
        check(rejected, "reject invalid digit");
        System.out.println("PASSED " + assertions + " core checks");
    }
}
