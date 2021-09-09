within AixLib.Fluid.Movers.Validation;
model ControlledFlowMachineDynamic
  "Fans with different control signals as input and a dynamic speed signal"
  extends Modelica.Icons.Example;
  extends AixLib.Fluid.Movers.Validation.BaseClasses.ControlledFlowMachine(
    fan4(energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial),
    fan1(energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial),
    fan2(energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial),
    fan3(energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial));

  extends AixLib.Icons.ibpsa;
  annotation (
experiment(Tolerance=1e-6, StopTime=600),
__Dymola_Commands(file="modelica://AixLib/Resources/Scripts/Dymola/Fluid/Movers/Validation/ControlledFlowMachineDynamic.mos"
        "Simulate and plot"),
    Documentation(info="<html>
This example demonstrates the use of the flow model with four different configurations.
At steady-state, all flow models have the same mass flow rate and pressure difference.
</html>"),
Diagram(coordinateSystem(preserveAspectRatio=true, extent={{-160,-100},{160, 160}})));

end ControlledFlowMachineDynamic;
