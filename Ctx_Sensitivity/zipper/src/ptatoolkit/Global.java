package ptatoolkit;

public class Global {

    private static boolean debug = false;

    public static void setDebug(boolean debug) {
        Global.debug = debug;
    }

    public static boolean isDebug() {
        return debug;
    }

    public static final int UNDEFINE = -1;

    // Zipper
    private static String flow = null;

    public static String getFlow() {
        return flow;
    }

    public static void setFlow(String flow) {
        Global.flow = flow;
    }

    private static boolean enableWrappedFlow = true;

    public static boolean isEnableWrappedFlow() {
        return enableWrappedFlow;
    }

    public static void setEnableWrappedFlow(boolean enableWrappedFlow) {
        Global.enableWrappedFlow = enableWrappedFlow;
    }

    private static boolean enableUnwrappedFlow = true;

    public static boolean isEnableUnwrappedFlow() {
        return enableUnwrappedFlow;
    }

    public static void setEnableUnwrappedFlow(boolean enableUnwrappedFlow) {
        Global.enableUnwrappedFlow = enableUnwrappedFlow;
    }

    private static boolean isExpress = false;

    public static boolean isExpress() {
        return isExpress;
    }

    public static void setExpress(boolean isExpress) {
        Global.isExpress = isExpress;
    }


    private static int thread = UNDEFINE;

    public static int getThread() {
        return thread;
    }

    public static void setThread(int thread) {
        Global.thread = thread;
    }

    // Scaler
    private static int tst = UNDEFINE;

    public static int getTST() {
        return tst;
    }

    public static void setTST(int tst) {
        Global.tst = tst;
    }

    private static boolean listContext = false;

    public static boolean isListContext() {
        return listContext;
    }

    public static void setListContext(boolean listContext) {
        Global.listContext = listContext;
    }
}
