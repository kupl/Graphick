package ptatoolkit.pta.basic;

import java.util.Collection;

/**
 * The abstraction of method.
 */
public abstract class Method extends AttributeElement {

	private final Collection<Variable> params;
	private final Collection<Variable> retVars;
	private final boolean isPrivate;

	protected Method(Collection<Variable> params,
					 Collection<Variable> retVars,
					 boolean isPrivate) {
		this.params = params;
		this.retVars = retVars;
		this.isPrivate = isPrivate;
	}

	public Collection<Variable> getParameters() {
		return params;
	}

	/**
	 *
	 * @return all parameters. For instance methods, this variable
	 * will also be returned.
	 */
	public abstract Collection<Variable> getAllParameters();

	public Collection<Variable> getRetVars() {
		return retVars;
	}

	public abstract boolean isInstance();

	public boolean isStatic() {
		return !isInstance();
	}

	public boolean isPrivate() { return isPrivate; }
}
