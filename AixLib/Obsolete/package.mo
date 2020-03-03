within AixLib;
package Obsolete "Classes that are obsolete and will be removed in later versions"
  extends Modelica.Icons.Package;

annotation (Documentation(info="<html><p>
  This package contains classes that are obsolete and will be removed
  from the corresponding library in a future release.
</p>
<h3>
  How To
</h3>
<ol>
  <li>Extend BaseClass model for red frame with dashed line:
  <span style=\"font-family: Courier New;\">extends
  AixLib.Obsolete.BaseClasses.ObsoleteModel;</span>
  </li>
  <li>Add following argument to model annotation at bottom of the
  model: <span style=\"font-family: Courier New;\">obsolete = \"Obsolete
  model - a description, e.g. which model to use instead\",</span>
  </li>
</ol>
<ul>
  <li>November 27, 2019, by Philipp Mehrfeld:<br/>
    Add How To.
  </li>
</ul>
</html>"));
end Obsolete;
