package ptatoolkit.doop.factory;

import ptatoolkit.doop.DataBase;
import ptatoolkit.doop.Query;
import ptatoolkit.doop.basic.DoopInstanceMethod;
import ptatoolkit.doop.basic.DoopStaticMethod;
import ptatoolkit.pta.basic.Method;
import ptatoolkit.pta.basic.Variable;

import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class MethodFactory extends ElementFactory<Method> {

    private final Map<String, Variable> sig2this = new HashMap<>();
    private final Map<String, Set<Variable>> sig2params = new HashMap<>();
    private final Map<String, Set<Variable>> sig2ret = new HashMap<>();
    private final Set<String> privateMethods = new HashSet<>();

    public MethodFactory(DataBase db, VariableFactory varFactory) {
        db.query(Query.THIS_VAR).forEachRemaining(list -> {
            String sig = list.get(0);
            Variable thisVar = varFactory.get(list.get(1));
            sig2this.put(sig, thisVar);
        });

        db.query(Query.PARAMS).forEachRemaining(list -> {
            String sig = list.get(0);
            Variable param = varFactory.get(list.get(1));
            if (!sig2params.containsKey(sig)) {
                sig2params.put(sig, new HashSet<>(4));
            }
            sig2params.get(sig).add(param);
        });

        db.query(Query.RET_VARS).forEachRemaining(list -> {
            String sig = list.get(0);
            Variable ret = varFactory.get(list.get(1));
            if (!sig2ret.containsKey(sig)) {
                sig2ret.put(sig, new HashSet<>(4));
            }
            sig2ret.get(sig).add(ret);
        });

        db.query(Query.METHOD_MODIFIER).forEachRemaining(list -> {
            String sig = list.get(0);
            String mod = list.get(1);
            if (mod.equals("private")) {
                privateMethods.add(sig);
            }
        });
    }

    @Override
    protected Method createElement(String sig) {
        Variable thisVar = sig2this.get(sig);
        Set<Variable> params = sig2params.get(sig);
        if (params == null) {
            params = Collections.emptySet();
        }
        Set<Variable> retVars = sig2ret.get(sig);
        if (retVars == null) {
            retVars = Collections.emptySet();
        }
        boolean isPrivate = privateMethods.contains(sig);
        if (thisVar != null) { // sig represents an instance method
            return new DoopInstanceMethod(sig, thisVar, params, retVars,
                    isPrivate, ++count);
        } else { // sig represents a static method
            return new DoopStaticMethod(sig, params, retVars,
                    isPrivate, ++count);
        }
    }

}
