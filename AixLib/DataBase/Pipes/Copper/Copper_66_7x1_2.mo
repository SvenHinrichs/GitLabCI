within AixLib.DataBase.Pipes.Copper;
record Copper_66_7x1_2 "Copper 66.7x1.2"

  extends PipeBaseDataDefinition(
    d_i=0.0643,
    d_o=0.0667,
    d=8900,
    lambda=393,
    c=390);
  // Constant chemical values assumed

  annotation (Documentation(revisions="<html><ul>
  <li>
    <i>July 9, 2013&#160;</i> by Ole Odendahl:<br/>
    Formatted documentation appropriately
  </li>
  <li>
    <i>June 29, 2011&#160;</i> by Ana Constantin:<br/>
    Implemented.
  </li>
</ul>
</html>",
info="<html><h4>
  <span style=\"color:#008000\">Overview</span>
</h4>
<p>
  Record for copper pipe
</p>
<p>
  Source:
</p>
<ul>
  <li>DIN EN 1057:2010-06
  </li>
  <li>Table 3, Page 14
  </li>
</ul>
</html>"));
end Copper_66_7x1_2;
