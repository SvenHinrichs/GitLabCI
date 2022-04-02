within AixLib.Fluid.HeatPumps.Data.ScrollWaterToWater.Heating;
 record Viessmann_BW301A21_28kW_5_94COP_R410A =
   AixLib.Fluid.HeatPumps.Data.ScrollWaterToWater.Generic (
     volRat = 2.30110444908,
     V_flow_nominal = 0.00375267244467,
     leaCoe = 0.000707240954117,
     etaEle = 0.812921232304,
     PLos = 143.194897625,
     dTSup = 0.472690462405,
     UACon = 19837.0958847,
     UAEva = 42613.4241528)
   "Calibrated parameters for Viessmann Vitocal 300G BW 301.A21"
   annotation (
     defaultComponentPrefixes = "parameter",
     defaultComponentName="datHeaPum",
     preferredView="info",
   Documentation(info="<html>
 <p>
 Generated by Filip Jorissen on 2017-05-19.
 </p>
 </html>"),  
   __Dymola_LockedEditing="Model from IBPSA");
