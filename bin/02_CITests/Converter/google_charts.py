class google_charts(object):

	def __init__(self,chart_type):
		
		self.chart_type = chart_type
		
	def read_ref(self):
		ref = open("Test","r")
		## Anzahl Einträge Zählen
		## Modelica to Python
	
	def linechart(self):
	html_file = open("demofile3.txt", "w")
	### Write linechart Syntax
	html_file.write("
	
		<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);"

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
		
##############################################################################################		
		
		
          ['Year', 'Sales', 'Expenses'],
          ['2004',  1000,      400],
          ['2005',  1170,      460],
          ['2006',  660,       1120],
          ['2007',  1030,      540]
        ]);

#############################################################################################
        var options = {
          title: 'Company Performance',
          curveType: 'function',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="curve_chart" style="width: 900px; height: 500px"></div>
  </body>
</html>



if  __name__ == '__main__':
	"""Parser"""
	# Configure the argument parser
	parser = argparse.ArgumentParser(description = "Check the Style of Packages")
	check_test_group = parser.add_argument_group("arguments to run check tests")
	check_test_group.add_argument("-t", "--chart-type", default="linechart", help="Set your chart type")
	
	# Parse the arguments
	args = parser.parse_args()
	
	## Load Bib
	from google_charts import google_charts
	func_chart = google_charts(chart_type = args.chart_type)
	
	
	
	
	