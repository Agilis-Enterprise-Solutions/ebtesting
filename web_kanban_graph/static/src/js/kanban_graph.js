odoo.define('web_kanban_graph.widget', function (require) {
		"use strict";
		var AbstractField = require('web.AbstractField');
		var field_registry = require('web.field_registry');
		var utils = require('web.utils');
/**
 * Kanban widgets: Graph
 * Parabolic Graph
 */
var KanbanParabolicGraphWidget = AbstractField.extend({
    className: "o_kanban_parabolic_graph",
    cssLibs: [
        '/web/static/lib/nvd3/nv.d3.css'
    ],
    jsLibs: [
        '/web/static/lib/nvd3/d3.v3.js',
        '/web/static/lib/nvd3/nv.d3.js',
        '/web/static/src/js/libs/nvd3.js'
    ],
    start: function() {
        var self = this;
        var field_value = JSON.parse(self.value);
        var id_dict = _.pluck(field_value, 'id');
        nv.utils.windowResize(this._onResize);
        this.$el.append($("<svg id='chart_line"+id_dict+"' class='oe_graph'>"));
        this.svg = '#chart_line'+id_dict;
        self.line(field_value);
    },
    line: function (data) {
        var self = this;
        var xAxis,yAxis = "";
        var xval = [0,0];
        var yval = [0,0];
        var interval = 0.1;
        var xinterval = 1;
        var title = "";
        if(data){
        	xval = data[0].x_val;
        	yval = data[0].y_val;
        	title = data[0].title;
        }
        nv.addGraph(function() {
        	  var chart = nv.models.lineChart()
        	  				.margin({left: 100})  //Adjust chart margins to give the x-axis some breathing room.
        	                .useInteractiveGuideline(true)//We want nice looking tooltips and a guideline!
        	                .options({
        	                	duration: 350,
        	                	interpolate: 'cardinal',
        	                	yDomain: yval,
        	                	xDomain: xval,
	    	                	
        	                })
        	                .showYAxis(true)        //Show the y-axis
        	                .showXAxis(true)
        	                .noData("No Data Available To Display Graph")
        	                ;
        	  if(data){
	        	  for (var i = 0; i < data[0]['values'].length; i++) {
	        		  xAxis = data[0]['values'][i].labels[1];
	                  yAxis = data[0]['values'][i].yaxis;
	        	  }
	        	  if(yval[1] > 10){interval=1;}
	        	  if(yval[1] > 50){interval=5;}
	        	  if(yval[1] > 100){interval=10;}
	        	  if(yval[1] > 500){interval=25;}
	        	  if(yval[1] > 1000){interval=50;}
	        	  if(xval[1] > 50){xinterval = 5;}
	        	  if(xval[1] > 100){xinterval=10;}
	        	  if(xval[1] > 500){xinterval=25;}
	        	  if(xval[1] > 1000){xinterval=50;}
	        	  chart.xAxis     //Chart x-axis settings
	        	      .axisLabel(xAxis)
	        	      .tickValues(d3.range(xval[0], xval[1], xinterval))
	
	        	  chart.yAxis  //Chart y-axis settings
	        	      .axisLabel(yAxis)
	        	      .tickValues(d3.range(yval[0], yval[1], interval))
	        	      
	        	  /* Done setting the chart up? Time to render it!*/
	        	  var myData = chartData(data);   //You need data...
	        	  if(data[0]['values'].length >=1){
		        	  var text = d3.select(self.svg) //I try to add title as text
			        	  .append("text")
			        	  .attr("x", 500)             
						  .attr("y", 10)
						  .attr("text-anchor", "middle")  
			        	  .text(title);
	        	  }
	        	  d3.select(self.svg)
	        	      .datum(myData)
	        	      .transition().duration(500)  
	        	      .call(chart);
	        	  nv.utils.windowResize(chart.update);
        	  }
        	  return chart;
	      	});
	        
	        function chartData(data){
	        	var line_data = [];
	            var data_dict = {};
	            var tick = -1;
	            var tickLabels = [];
	            var label, tickLabel;
	            var identity = function (p) {return p;};
	            var tickValues = [];
	            var tickFormat; 
	        	for (var i = 0; i < data[0]['values'].length; i++) {
	        		 if (data[0]['values'][i].labels[0] !== tickLabel) {
	                     tickLabel = data[0]['values'][i].labels[0];
	                     tickValues.push(tick);
	                     tickLabels.push(tickLabel);
	                     tick++;
	                 }
	        		 label = data[0]['values'][i].labels[1];
	                 if (!data_dict[label]) {
	                      data_dict[label] = {
	                          values: [],
	                          key: label,
	                      };
	                  }
	                  data_dict[label].values.push({
	                      x: data[0]['values'][i].labels[0], y: data[0]['values'][i].value,
	                  });
	                  line_data = _.map(data_dict, identity);
	        	 }
	             data = line_data;
	        	 return data;
	        }
    },
});
field_registry.add("kanban_parabolic_graph", KanbanParabolicGraphWidget);


/**
 * Kanban widgets: Graph
 * Line Chart
 */
var KanbanLineGraphWidget = AbstractField.extend({
    className: "o_kanban_line_graph",
    cssLibs: [
        '/web/static/lib/nvd3/nv.d3.css'
    ],
    jsLibs: [
        '/web/static/lib/nvd3/d3.v3.js',
        '/web/static/lib/nvd3/nv.d3.js',
        '/web/static/src/js/libs/nvd3.js'
    ],
    start: function() {
        var self = this;
        var field_value = JSON.parse(self.value);
        var id_dict = _.pluck(field_value, 'id');
        nv.utils.windowResize(this._onResize);
        this.$el.append($("<svg id='chart_line"+id_dict+"' class='oe_graph'>"));
        this.svg = '#chart_line'+id_dict;
        self.line(field_value);
    },
    line: function (data) {
        var self = this;
        var xAxis,yAxis = "";
        var xval = [0,0];
        var yval = [0,0];
        var interval = 0.1;
        var xinterval = 1;
        var title="";
        if(data){
        	xval = data[0].x_val;
        	yval = data[0].y_val;
        	title = data[0].title;
        }
        nv.addGraph(function() {
        	  var chart = nv.models.lineChart()
        	                .margin({left: 100})  //Adjust chart margins to give the x-axis some breathing room.
        	                .useInteractiveGuideline(true)//We want nice looking tooltips and a guideline!
        	                .options({
        	                	duration: 350,
        	                	yDomain: yval,
        	                	xDomain: xval
        	                })
        	                .showLegend(true)       //Show the legend, allowing users to turn on/off line series.
        	                .showYAxis(true)        //Show the y-axis
        	                .showXAxis(true)
        	                .noData("No Data Available To Display Graph")
        	                ;
        	  if(data){
	        	  for (var i = 0; i < data[0]['values'].length; i++) {
	        		  xAxis = data[0]['values'][i].labels[1];
	                  yAxis = data[0]['values'][i].yaxis;
	        	  }
	        	  if(yval[1] > 10){interval=1;}
	        	  if(yval[1] > 50){interval=5;}
	        	  if(yval[1] > 100){interval=10;}
	        	  if(yval[1] > 500){interval=25;}
	        	  if(yval[1] > 1000){interval=50;}
	        	  if(xval[1] > 50){xinterval = 5;}
	        	  if(xval[1] > 100){xinterval=10;}
	        	  if(xval[1] > 500){xinterval=25;}
	        	  if(xval[1] > 1000){xinterval=50;}
	        	  chart.xAxis     //Chart x-axis settings
	        	      .axisLabel(xAxis)
	        	      .tickValues(d3.range(xval[0], xval[1], xinterval))
	
	        	  chart.yAxis  //Chart y-axis settings
	        	      .axisLabel(yAxis)
	        	      .tickValues(d3.range(yval[0], yval[1], interval))
	        	  /* Done setting the chart up? Time to render it!*/
	        	   
	        	  var myData = chartData(data);
	        	  //You need data...
	        	  if(data[0]['values'].length >=1){
	        		  var text = d3.select(self.svg) //I try to add title as text
			        	  .append("text")
			        	  .attr("x", 500)             
						  .attr("y", 10)
						  .attr("text-anchor", "middle")  
			        	  .text(title);
	        	  }
	        	 
	        	  d3.select(self.svg)
	        	      .datum(myData)
	        	      .transition().duration(500)        	     
	        	      .call(chart);
	        	  nv.utils.windowResize(chart.update);
        	  }
        	  return chart;
	      	});
        var data_dict = {};
	        function chartData(data){
	            var label;
	        var  values=[], horizontal=[], horizontal2=[],  vertical=[], vertical2=[];
	       
	        if (data[0]['values'].length>=1){
	            label = data[0]['values'][0].labels[1];
	           
	        	for (var i = 0; i < data[0]['values'].length; i++) {
	        		values.push({
	                      x: data[0]['values'][i].labels[0], y: data[0]['values'][i].value,
	                  });
	        	 }
	        }
	        	
	        	if ((data[0]['horizontal'])&& (data[0]['h1_value'])){
	        	for (var i = 0; i < data[0]['horizontal'].length; i++) {
	                    horizontal.push({  x:data[0]['horizontal'][i].valuess, y:data[0]['h1_value'] });
	        	 }
	        	}	            
	        	if ((data[0]['horizontal'])&& (data[0]['h2_value'])){
	        	for (var i = 0; i < data[0]['horizontal'].length; i++) {
	        		horizontal2.push({
	                      x:data[0]['horizontal'][i].valuess, y:data[0]['h2_value']
	                  });
	        	}
	        	 }
	        	if ((data[0]['horizontal'])&&(data[0]['v1_value'])){
	        	for (var i = 0; i < data[0]['vertical'].length; i++) {
	                  vertical.push({
	                      x:data[0]['v1_value'] ,y:data[0]['vertical'][i].value
	                  });
	        	 }
	        	}
	        	if ((data[0]['horizontal'])&&(data[0]['v2_value'])){
	        	for (var i = 0; i < data[0]['vertical'].length; i++) {
	        		vertical2.push({
	                      x:data[0]['v2_value'] ,y:data[0]['vertical'][i].value
	                  });
	        	 }
	        	
	        }
	          	 if ((data[0]['v1_value'])&&(data[0]['v2_value']))
	          		 {
	        	 return  [
	        		     {
	        		        values: values,
	        		        key: label,
	        		        color: '#7777ff',
	        		      },
	        		    {
	        		        values: vertical,      //values - represents the array of {x,y} data points
	        		        key: 'V1', //key  - the name of the series.
	        		        color:'#F08080', //color - optional: choose your own line color.
	        		      },
	        		      {
	        		        values: vertical2,
	        		        key: 'V2',
	        		        color: '#F08080',
	        		      },
	        		      {
	        		        values: horizontal,
	        		        key: 'H1',
	        		        color: '#F08080',
	        		      },
	        		      {
	        		        values: horizontal2,
	        		        key: 'H2',
	        		        color: '#F08080',
		        		      },
	        		    ];
	          		 }

	          	 else if((data[0]['h1_value'])&&(data[0]['v1_value']))
	          		 {
	          		 return  [
	          			 {
		        		        values: values,
		        		        key: label,
		        		        color: '#7777ff',
		        		      },
	          			 {
		        		        values: horizontal,
		        		        key: 'H1',
		        		        color: '#F08080',
		        		      },
	        		      {
		        		        values: vertical,      //values - represents the array of {x,y} data points
		        		        key: 'V1', //key  - the name of the series.
		        		        color:'#F08080', //color - optional: choose your own line color.
		        		      },];
	          	 }
	          	 else 
	          		 {
	          		 alert("Entered value for  maximum dry density  is out off intersection range (or) Entered Value makes a straight line so there is no intersection point")
	          		 return[
	          			 {
		        		        values: values,
		        		        key: label,
		        		        color: '#7777ff',
		        		      },
	          		 ];
	          		 }
	        }
    },
});
field_registry.add("kanban_line_graph", KanbanLineGraphWidget);
});
