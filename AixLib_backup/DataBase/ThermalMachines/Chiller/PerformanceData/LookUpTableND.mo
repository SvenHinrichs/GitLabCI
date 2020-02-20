within AixLib.DataBase.ThermalMachines.Chiller.PerformanceData;
model LookUpTableND "N-dimensional table with data for heat pump"
  extends
    AixLib.DataBase.ThermalMachines.Chiller.PerformanceData.BaseClasses.PartialPerformanceData;
  parameter Real nConv=100
    "Gain value multiplied with relative compressor speed n to calculate matching value based on sdf tables";
  parameter SDF.Types.InterpolationMethod interpMethod=SDF.Types.InterpolationMethod.Linear
    "Interpolation method";
  parameter SDF.Types.ExtrapolationMethod extrapMethod=SDF.Types.ExtrapolationMethod.None
    "Extrapolation method";
  parameter String filename_Pel=
      "modelica://Resources/Data/Fluid/BaseClasses/PerformanceData/LookUpTableND/VZH088AG.sdf"
                                   "File name of sdf table data"
    annotation (Dialog(group="Electrical Power",loadSelector(filter="SDF Files (*.sdf);;All Files (*.*)", caption="Select SDF file")));
  parameter String dataset_Pel="/Pel"
                                  "Dataset name"
    annotation (Dialog(group="Electrical Power"));
  parameter String dataUnit_Pel="W"
                                   "Data unit"
    annotation (Dialog(group="Electrical Power"));
  parameter String scaleUnits_Pel[3]={"K","K",""}
                                                 "Scale units"
    annotation (Dialog(group="Electrical Power"));
  parameter String filename_QCon=
      "modelica://Resources/Data/Fluid/BaseClasses/PerformanceData/LookUpTableND/VZH088AG.sdf"
                                    "File name of sdf table data"
    annotation (Dialog(group="Condenser heat flow",loadSelector(filter="SDF Files (*.sdf);;All Files (*.*)", caption="Select SDF file")));
  parameter String dataset_QCon="/QCon"
                                   "Dataset name"
    annotation (Dialog(group="Condenser heat flow"));
  parameter String dataUnit_QCon="W"
                                    "Data unit"
    annotation (Dialog(group="Condenser heat flow"));
  parameter String scaleUnits_QCon[3]={"K","K",""}
                                                  "Scale units"
    annotation (Dialog(group="Condenser heat flow"));

  Modelica.Blocks.Math.Gain nConGain(final k=nConv)
    "Convert relative speed n to an absolute value for interpolation in sdf tables"
    annotation (Placement(transformation(
        extent={{-8,-8},{8,8}},
        rotation=-90,
        origin={0,68})));
 Modelica.Blocks.Math.UnitConversions.To_degC t_Co_in
    annotation (extent=[-88,38; -76,50], Placement(transformation(extent={{-6,-6},
            {6,6}},
        rotation=-90,
        origin={46,44})));
  Modelica.Blocks.Math.UnitConversions.To_degC t_Ev_ou annotation (extent=[-88,38;
        -76,50], Placement(transformation(extent={{-6,-6},{6,6}},
        rotation=-90,
        origin={-40,46})));
  Modelica.Blocks.Math.Add calcRedQCon
    "Calculates condenser heat flow with total energy balance" annotation (
      Placement(transformation(
        extent={{-6,6},{6,-6}},
        rotation=-90,
        origin={-80,-86})));
  Utilities.Logical.SmoothSwitch switchPel
    "If HP is off, no heat will be exchanged"
    annotation (Placement(transformation(extent={{-10,-10},{10,10}},
        rotation=-90,
        origin={50,-60})));
  Utilities.Logical.SmoothSwitch switchQEva
    "If chiller is off, no heat will be exchanged"
    annotation (Placement(transformation(extent={{-10,-10},{10,10}},
        rotation=-90,
        origin={-50,-56})));
  Modelica.Blocks.Sources.Constant constZero(final k=0)
    "Power if HP is turned off"
    annotation (Placement(transformation(extent={{-6,-6},{6,6}},
        rotation=-90,
        origin={-4,-18})));
  SDF.NDTable nDTableQEva(
    final nin=3,
    final readFromFile=true,
    final filename=filename_QCon,
    final dataset=dataset_QCon,
    final dataUnit=dataUnit_QCon,
    final scaleUnits=scaleUnits_QCon,
    final interpMethod=interpMethod,
    final extrapMethod=extrapMethod)
    "SDF-Table data for evaporator heat flow"
    annotation (Placement(transformation(extent={{-12,-12},{12,12}},
        rotation=-90,
        origin={-42,-10})));
  SDF.NDTable nDTablePel(
    final nin=3,
    final readFromFile=true,
    final filename=filename_Pel,
    final dataset=dataset_Pel,
    final dataUnit=dataUnit_Pel,
    final scaleUnits=scaleUnits_Pel,
    final interpMethod=interpMethod,
    final extrapMethod=extrapMethod) "SDF table data for electrical power"
                                     annotation (Placement(transformation(
        extent={{-12,-12},{12,12}},
        rotation=-90,
        origin={50,-10})));
  Modelica.Blocks.Routing.Multiplex3 multiplex3_1(
    final n1=1,
    final n2=1,
    final n3=1) "Concat all inputs into an array"
    annotation (Placement(transformation(extent={{-8,-8},{8,8}},
        rotation=-90,
        origin={0,20})));

  Modelica.Blocks.Logical.GreaterThreshold greaterThreshold(final threshold=
        Modelica.Constants.eps) annotation (Placement(transformation(
        extent={{-6,-6},{6,6}},
        rotation=270,
        origin={-72,46})));
equation
  connect(switchPel.y, Pel) annotation (Line(points={{50,-71},{50,-82},{0,-82},
          {0,-110}},
               color={0,0,127}));

  connect(constZero.y,switchQEva. u3) annotation (Line(points={{-4,-24.6},{-4,
          -24},{-4,-24},{-4,-28},{-4,-30},{-58,-30},{-58,-42},{-58,-42},{-58,
          -44},{-58,-44}},     color={0,0,127}));
  connect(constZero.y, switchPel.u3) annotation (Line(points={{-4,-24.6},{-4,
          -30},{42,-30},{42,-48}},
                          color={0,0,127}));
  connect(nDTableQEva.y,switchQEva. u1)
    annotation (Line(points={{-42,-23.2},{-42,-44}},
                                                color={0,0,127}));
  connect(nDTablePel.y, switchPel.u1)
    annotation (Line(points={{50,-23.2},{50,-34},{58,-34},{58,-48}},
                                                  color={0,0,127}));
  connect(multiplex3_1.y,nDTableQEva. u) annotation (Line(points={{-1.55431e-15,
          11.2},{-1.55431e-15,4.4},{-42,4.4}},
                                          color={0,0,127}));
  connect(multiplex3_1.y, nDTablePel.u) annotation (Line(points={{-1.77636e-15,11.2},
          {-1.77636e-15,4.4},{50,4.4}},      color={0,0,127}));
  connect(sigBus.T_flow_co,t_Co_in. u) annotation (Line(
      points={{1.075,104.07},{46,104.07},{46,51.2}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(sigBus.T_ret_ev,t_Ev_ou. u) annotation (Line(
      points={{1.075,104.07},{-40,104.07},{-40,53.2}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(sigBus.N, greaterThreshold.u) annotation (Line(
      points={{1.075,104.07},{-72,104.07},{-72,53.2}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-3,6},{-3,6}},
      horizontalAlignment=TextAlignment.Right));
  connect(greaterThreshold.y,switchQEva. u2) annotation (Line(points={{-72,
          39.4},{-72,-36},{-50,-36},{-50,-44}},
                                          color={255,0,255}));
  connect(greaterThreshold.y, switchPel.u2) annotation (Line(points={{-72,39.4},
          {-72,-36},{50,-36},{50,-48}}, color={255,0,255}));
  connect(sigBus.N, nConGain.u) annotation (Line(
      points={{1.075,104.07},{1.77636e-15,104.07},{1.77636e-15,77.6}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-3,6},{-3,6}},
      horizontalAlignment=TextAlignment.Right));
  connect(nConGain.y, multiplex3_1.u3[1]) annotation (Line(points={{
          -1.55431e-15,59.2},{-6,59.2},{-6,29.6},{-5.6,29.6}}, color={0,0,127}));
  connect(t_Ev_ou.y, multiplex3_1.u1[1]) annotation (Line(points={{-40,39.4},{
          -40,36},{5.6,36},{5.6,29.6}}, color={0,0,127}));
  connect(t_Co_in.y, multiplex3_1.u2[1]) annotation (Line(points={{46,37.4},{46,
          32},{0,32},{0,29.6}}, color={0,0,127}));
  connect(switchPel.y, calcRedQCon.u2) annotation (Line(points={{50,-71},{50,
          -76},{-76.4,-76},{-76.4,-78.8}}, color={0,0,127}));
  connect(switchQEva.y, calcRedQCon.u1) annotation (Line(points={{-50,-67},{
          -50,-72},{-83.6,-72},{-83.6,-78.8}}, color={0,0,127}));
  connect(calcRedQCon.y, QCon)
    annotation (Line(points={{-80,-92.6},{-80,-110}}, color={0,0,127}));
  connect(switchQEva.y, QEva) annotation (Line(points={{-50,-67},{-50,-88},{
          80,-88},{80,-110}}, color={0,0,127}));
  annotation (Icon(graphics={
    Line(points={{-60.0,40.0},{-60.0,-40.0},{60.0,-40.0},{60.0,40.0},{30.0,40.0},{30.0,-40.0},{-30.0,-40.0},{-30.0,40.0},{-60.0,40.0},{-60.0,20.0},{60.0,20.0},{60.0,0.0},{-60.0,0.0},{-60.0,-20.0},{60.0,-20.0},{60.0,-40.0},{-60.0,-40.0},{-60.0,40.0},{60.0,40.0},{60.0,-40.0}}),
    Line(points={{0.0,40.0},{0.0,-40.0}}),
    Rectangle(fillColor={255,255,0},
      fillPattern=FillPattern.Solid,
      extent={{-60.0,0.0},{-30.0,20.0}},
          lineColor={0,0,0}),
    Rectangle(fillColor={255,215,136},
      fillPattern=FillPattern.Solid,
      extent={{-60.0,-40.0},{-30.0,-20.0}}),
    Rectangle(fillColor={255,255,0},
      fillPattern=FillPattern.Solid,
      extent={{-60,-20},{-30,0}},
          lineColor={0,0,0}),
    Rectangle(fillColor={255,255,0},
      fillPattern=FillPattern.Solid,
      extent={{-60,-40},{-30,-20}},
          lineColor={0,0,0}),
    Rectangle(fillColor={255,255,0},
      fillPattern=FillPattern.Solid,
      extent={{-30,-40},{0,-20}},
          lineColor={0,0,0}),
    Rectangle(fillColor={255,255,0},
      fillPattern=FillPattern.Solid,
      extent={{0,-40},{30,-20}},
          lineColor={0,0,0}),
    Rectangle(fillColor={255,255,0},
      fillPattern=FillPattern.Solid,
      extent={{30,-40},{60,-20}},
          lineColor={0,0,0}),
    Rectangle(fillColor={255,255,0},
      fillPattern=FillPattern.Solid,
      extent={{30,-20},{60,0}},
          lineColor={0,0,0}),
    Rectangle(fillColor={255,255,0},
      fillPattern=FillPattern.Solid,
      extent={{0,-20},{30,0}},
          lineColor={0,0,0}),
    Rectangle(fillColor={255,255,0},
      fillPattern=FillPattern.Solid,
      extent={{0,0},{30,20}},
          lineColor={0,0,0}),
    Rectangle(fillColor={255,255,0},
      fillPattern=FillPattern.Solid,
      extent={{30,0},{60,20}},
          lineColor={0,0,0}),
    Rectangle(fillColor={255,255,0},
      fillPattern=FillPattern.Solid,
      extent={{0,20},{30,40}},
          lineColor={0,0,0}),
    Rectangle(fillColor={255,255,0},
      fillPattern=FillPattern.Solid,
      extent={{30,20},{60,40}},
          lineColor={0,0,0}),
    Rectangle(fillColor={255,255,0},
      fillPattern=FillPattern.Solid,
      extent={{-60,20},{-30,40}},
          lineColor={0,0,0}),
    Rectangle(fillColor={255,255,0},
      fillPattern=FillPattern.Solid,
      extent={{-30,20},{0,40}},
          lineColor={0,0,0}),
    Rectangle(fillColor={255,255,0},
      fillPattern=FillPattern.Solid,
      extent={{-30,0},{0,20}},
          lineColor={0,0,0}),
    Rectangle(fillColor={255,255,0},
      fillPattern=FillPattern.Solid,
      extent={{-30,-20},{0,0}},
          lineColor={0,0,0})}),                Documentation(info="<html><p>
  Basic models showing the concept of using n-dimensional table data
  for the innerCycle of the heat pump model. This model assumes one
  provides data for inverter controlled heat pumps or chillers.
  However, this basis structure can be used to create own models, where
  electrical power and condenser depend on other inputs, such as
  ambient temperature.
</p>
</html>", revisions="<html>
<ul>
  <li>
    <i>May 22, 2019&#160;</i> by Julian Matthes:<br/>
    First implementation (see issue <a href=
    \"https://github.com/RWTH-EBC/AixLib/issues/715\">#715</a>)
  </li>
</ul>
</html>"));
end LookUpTableND;
