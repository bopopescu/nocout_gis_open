//Global Variables
var gauge_chart_val_style = "font-size:18px;border:1px solid #DADADA;background:#EEEEEE;"+
                            "padding:0px 5px;border-radius:3px;text-shadow: 1.5px 1.5px 2px #CCCCCC;",
    gauge_val_default_color = "",
    solid_gauge_chart_ids = [
        "down-all",
        "latency-all",
        "packetloss-all",
        "temperature-idu-wimax",
        "down-wimax",
        "down-pmp",
        "latency-wimax",
        "latency-pmp",
        "packetloss-wimax",
        "packetloss-pmp",
        "temperature-fan-wimax",
        "temperature-acb-wimax"
    ],
    solid_gauge_url_obj = {
        "down-all" : {
            "url" : "",
            "trends_url" : "",
            "text" : "Down"
        },
        "latency-all" : {
            "url" : "",
            "trends_url" : "",
            "text" : "Latency"
        },
        "packetloss-all" : {
            "url" : "",
            "trends_url" : "",
            "text" : "Packet Drop"
        },
        "temperature-idu-wimax" : {
            "url" : "",
            "trends_url" : "",
            "text" : "Temperature IDU WiMAX"
        },
        "down-wimax" : {
            "url" : "",
            "trends_url" : "",
            "text" : "Down WiMAX"
        },
        "down-pmp" : {
            "url" : "",
            "trends_url" : "",
            "text" : "Down PMP"
        },
        "latency-wimax" : {
            "url" : "",
            "trends_url" : "",
            "text" : "Latency WiMAX"
        },
        "latency-pmp" : {
            "url" : "",
            "trends_url" : "",
            "text" : "Latency PMP"
        },
        "packetloss-wimax" : {
            "url" : "",
            "trends_url" : "",
            "text" : "Packet Drop WiMAX"
        },
        "packetloss-pmp" : {
            "url" : "",
            "trends_url" : "",
            "text" : "Packet Drop PMP"
        },
        "temperature-fan-wimax" : {
            "url" : "",
            "trends_url" : "",
            "text" : "Temperature Fan Wimax"
        },
        "temperature-acb-wimax" : {
            "url" : "",
            "trends_url" : "",
            "text" : "Temperature ACB WiMAX"
        }
    },
    pie_chart_ids = [
        "wimax_sales_opportunity",
        "pmp_sales_opportunity",
        "wimax_sector_capacity",
        "pmp_sector_capacity",
        "wimax_backhaul_capacity",
        "pmp_backhaul_capacity",
        "mfr_cause_code",
        "tcl_pop_backhaul_capacity"
    ],
    pie_chart_url_obj = {
        "wimax_sales_opportunity" : {
            "url" : "",
            "trends_url" : "",
            "text" : "Wimax Sales Opportunity"
        },
        "pmp_sales_opportunity" : {
            "url" : "",
            "trends_url" : "",
            "text" : "PMP Sales Opportunity"
        },
        "wimax_sector_capacity" : {
            "url" : "",
            "trends_url" : "",
            "text" : "Wimax Sector Capacity"
        },
        "pmp_sector_capacity" : {
            "url" : "",
            "trends_url" : "",
            "text" : "PMP Sector Capacity"
        },
        "wimax_backhaul_capacity" : {
            "url" : "",
            "trends_url" : "",
            "text" : "Wimax Backhaul Capacity"
        },
        "pmp_backhaul_capacity" : {
            "url" : "",
            "trends_url" : "",
            "text" : "PMP Backhaul Capacity"
        },
        "mfr_cause_code" : {
            "url" : "",
            "trends_url" : "",
            "text" : "MFR Caused Code"
        },
        "tcl_pop_backhaul_capacity" : {
            "url" : "",
            "trends_url" : "",
            "text" : "TCL POP Backhaul Capacity"
        }
    },
    area_chart_ids = [
        "id_mfr_processed_chart"
    ],
    area_chart_url_obj = {
      "id_mfr_processed_chart" : {
        "url" : "",
        "trends_url" : "",
        "text" : "MFR Processed"
      }
    },
    all_charts_array = [],
    charts_info_list_chunks = [],
    dashboard_call_counter = 0;

/**
 * This function initialize main dashboard & it is recursive function
 * @method initDashboard
 */
function initDashboard() {

    // Initialize all speedometer(solid gauge) charts
    initSpeedometerCharts_dashboard(function(response) {
        // Initialize all pie charts
        initPieCharts_dashboard(function(response) {
            // Initialize all area charts
            initAreaCharts_dashboard(function(response) {
                // Start Server calling with the created list of charts
                createChartAPIChunks_dashboard(all_charts_array);
            });
        });
    });
}


/**
 * This function initialize all the solid gauge chart
 * @method initSpeedometerCharts_dashboard
 */
function initSpeedometerCharts_dashboard(callback) {
    // Initialize all the speedometer(solid gauge) charts
    for(var i=0;i<solid_gauge_chart_ids.length;i++) {
        if($("#"+solid_gauge_chart_ids[i]).length > 0 && solid_gauge_url_obj[solid_gauge_chart_ids[i]]["url"]) {
            // Get chart
            // get_speedometer_chart(
            //     solid_gauge_url_obj[solid_gauge_chart_ids[i]]["url"],
            //     "#"+solid_gauge_chart_ids[i],
            //     solid_gauge_url_obj[solid_gauge_chart_ids[i]]["text"]

            // );
            if(solid_gauge_url_obj[solid_gauge_chart_ids[i]]["url"]) {
                all_charts_array.push({
                    "url"  : solid_gauge_url_obj[solid_gauge_chart_ids[i]]["url"],
                    "id"   : "#"+solid_gauge_chart_ids[i],
                    "text" : solid_gauge_url_obj[solid_gauge_chart_ids[i]]["text"],
                    "type" : 'speedometer'
                });
            }
        }
    }

    callback(true);
}

/**
 * This function initialize all the pie chart
 * @method initPieCharts_dashboard
 */
function initPieCharts_dashboard(callback) {
    // Initialize all the speedometer(solid gauge) charts
    for(var i=0;i<pie_chart_ids.length;i++) {
        if($("#"+pie_chart_ids[i]).length > 0 && pie_chart_url_obj[pie_chart_ids[i]]["url"]) {
            // Get chart
            // highcharts_piechart(
            //     pie_chart_url_obj[pie_chart_ids[i]]["url"],
            //     "#"+pie_chart_ids[i],
            //     pie_chart_url_obj[pie_chart_ids[i]]["text"]
            // );
            if(pie_chart_url_obj[pie_chart_ids[i]]["url"]) {
                all_charts_array.push({
                    "url"  : pie_chart_url_obj[pie_chart_ids[i]]["url"],
                    "id"   : "#"+pie_chart_ids[i],
                    "text" : pie_chart_url_obj[pie_chart_ids[i]]["text"],
                    "type" : 'pie'
                });
            }
        }
    }

    callback(true);
}

/**
 * This function initialize all the area or areaspline chart
 * @method initAreaCharts_dashboard
 */
function initAreaCharts_dashboard(callback) {
    // Initialize all the speedometer(solid gauge) charts
    for(var i=0;i<area_chart_ids.length;i++) {
        if($("#"+area_chart_ids[i]).length > 0 && area_chart_url_obj[area_chart_ids[i]]["url"]) {
            // Get chart for latency of wimax.
            // highcharts_areachart(
            //     area_chart_url_obj[area_chart_ids[i]]["url"],
            //     "#"+area_chart_ids[i],
            //     area_chart_url_obj[area_chart_ids[i]]["text"]
            // );
            if(area_chart_url_obj[area_chart_ids[i]]["url"]) {
                all_charts_array.push({
                    "url"  : area_chart_url_obj[area_chart_ids[i]]["url"],
                    "id"   : "#"+area_chart_ids[i],
                    "text" : area_chart_url_obj[area_chart_ids[i]]["text"],
                    "type" : 'area'
                });
            }
        }
    }

    callback(true);
}

/**
 * This function makes parallel ajax call for charts
 * @method createChartAPIChunks_dashboard
 * @param charts_info_list {Array}, It contains the json object array of all dashboard charts
 */
function createChartAPIChunks_dashboard(charts_info_list) {
    var chunk_size = process_count ? process_count : 1;

    if(charts_info_list && charts_info_list.length > 0) {
        while (charts_info_list.length > 0) {
            charts_info_list_chunks.push(charts_info_list.splice(0, chunk_size));
        }
    }

    var chunk_counter = 0;

    if(charts_info_list_chunks[0]) {
        startChunksAjaxCall(chunk_counter);
    }
}

/**
 * This function loops the given counter chunk to start their ajax calls by calling further functions
 * @method startChunksAjaxCall
 * @param counter {Number}, It contains the integer value for charts_info_list_chunks index to be used
 */
function startChunksAjaxCall(counter) {
    
    var current_chunk = charts_info_list_chunks[counter];

    if(current_chunk && current_chunk.length > 0) {

        for(var j=0;j<current_chunk.length;j++) {

            var current_chart = current_chunk[j],
                chart_type = current_chart.type,
                url = current_chart.url,
                dom_id = current_chart.id,
                text = current_chart.text;

            if(url && dom_id) {
                makeDashboardAjaxCall(url, dom_id, text, chart_type, counter);
            }
        }
    } else {
        // Recursive calling after 5 min.
        setTimeout(function() {
            initDashboard();
        },300000);
    }
}

/**
 * This function makes ajax call as per given params & calls further functions to create charts
 * @method makeDashboardAjaxCall
 * @param url {String}, It contains the url on which ajax request is to be sent
 * @param domElement {String}, It contains the dom element id on which the chart is to be created
 * @param chart_title {String}, It contains the text shown on top of chart
 * @param chart_type {String}, It contains the type of chart which is to be created.
   It used to call different functions for different charts
 */
function makeDashboardAjaxCall(url, domElement, chart_title, chart_type, calling_counter) {

    // Increment the chunks counter
    calling_counter++;

    var extra_data = "";

    if(chart_type == 'speedometer') {
        extra_data = {
            'dashboard_name': domElement
        };
    }

    $.ajax({
        url : url,
        data : extra_data,
        type : "GET",
        success : function(result) {
            
            var response = "";
            
            if(typeof result == 'string') {
                response = JSON.parse(result);
            } else {
                response = result;
            }

            if(response.success == 1) {
                if(chart_type == 'speedometer') {
                        
                    updateSpeedometerChart(response.data.objects, domElement, chart_title, function(status) {
                        dashboard_call_counter++;
                        if(dashboard_call_counter >= process_count) {
                            dashboard_call_counter = 0;

                            startChunksAjaxCall(calling_counter);
                        }

                    });

                } else if(chart_type == 'area') {
                    
                    // If rf network availability url then call 
                    if(url.indexOf('rf_network_availability') > -1) {

                        var chart_prename = domElement.split("#")[1].split("_chart")[0];

                        // Create Chart
                        createHighChart_nocout(response.data.objects,chart_prename,'#333333',true, function(status) {
                            dashboard_call_counter++;

                            if(dashboard_call_counter >= process_count) {
                                dashboard_call_counter = 0;

                                startChunksAjaxCall(calling_counter);
                            }
                        });
                    } else {
                        updateAreaChart(response.data.objects,domElement, function(status) {
                            dashboard_call_counter++;

                            if(dashboard_call_counter >= process_count) {
                                dashboard_call_counter = 0;

                                startChunksAjaxCall(calling_counter);
                            }
                        });
                    }

                } else if(chart_type == 'pie') {

                    updatePieChart(response.data.objects,domElement, function(status) {
                        dashboard_call_counter++;
                        if(dashboard_call_counter >= process_count) {
                            dashboard_call_counter = 0;

                            startChunksAjaxCall(calling_counter);
                        }
                    });

                } else {
                    // pass
                }
            } else {
                dashboard_call_counter++;
                if(dashboard_call_counter >= process_count) {
                    dashboard_call_counter = 0;

                    startChunksAjaxCall(calling_counter);
                }
            }
        },
        error : function(err) {
            // hideSpinner();
            $.gritter.add({
                // (string | mandatory) the heading of the notification
                title: chart_title,
                // (string | mandatory) the text inside the notification
                text: err.statusText,
                // (bool | optional) if you want it to fade out on its own or just sit there
                sticky: false,
                // Time in ms after which the gritter will dissappear.
                time : 1500
            });

            dashboard_call_counter++;

            if(dashboard_call_counter >= process_count) {
                dashboard_call_counter = 0;

                startChunksAjaxCall(calling_counter);
            }
        }
    });
}

/**
 * This function creates or update area chart highchart as per given param
 * @method updateAreaChart
 */
function updatePieChart(chartData, domElement, callback) {
    // Pie Chart Color(Use default colors if API doesn't pass any color list)
    var default_chart_colors = window.Highcharts.getOptions().colors,
        colors_list = chartData.chart_data[0].color ? chartData.chart_data[0].color : default_chart_colors;

    // In case of update
    if($(domElement).highcharts()) {
        var chart = $(domElement).highcharts();
        for(var x=0;x<chart.series.length;x++) {
            if(chart.series[x] && chartData.chart_data[0].data[x]) {
                var series = chart.series[x];
                // Update Data
                series.update(chartData.chart_data[0].data[x]);
                // Update Color
                series.update({
                    colors : colors_list
                });
            }
        }
    } else {

        var pie_chart = $(domElement).highcharts({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                // text: chartData.chart_data[0].title
                text: ""
            },
            credits: {
                enabled: false
            },
            legend:{
                itemDistance : 15,
                itemMarginBottom : 5,
                // itemWidth : 138,
                borderColor : "#CCCCCC",
                borderWidth : "1",
                borderRadius : "8",
                itemStyle: {
                    color: '#555555',
                    fontSize : '10px'
                }
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true
                }
            },
            series: [{
                type: 'pie',
                name: chartData.chart_data[0].name,
                colors: colors_list,
                data: chartData.chart_data[0].data
            }],
            lang: {
                noData: 'Data is not available.'
            },
            noData: {
                style: {
                    fontWeight: 'bold',
                    fontSize: '20px',
                    color: '#539fb8',
                }
            },
        });
    }

    callback(true);
}

/**
 * This function creates or update area chart highchart as per given param
 * @method updateAreaChart
 */
function updateAreaChart(chartData, domElement, callback) {
    // In case of update
    if($(domElement).highcharts()) {

        var chart = $(domElement).highcharts();

        for(var x=0;x<chart.series.length;x++) {
            if(chart.series[x] && chartData.chart_data[0].data[x]) {
                var series = chart.series[x];
                series.update(chartData.chart_data[0].data[x]);
            }
        }
    // In case of create
    } else {

        $(domElement).highcharts({
            chart: {
                type: 'areaspline'
            },
            title: {
                // text: 'MFR Processed'
                text: ''
            },
            credits: {
                enabled: false
            },
            legend: {
                itemDistance : 15,
                itemMarginBottom : 5,
                // borderColor : "#FFF",
                borderWidth : "1",
                borderRadius : "5",
                itemStyle: {
                    // color: '#FFF',
                    fontSize : '12px'
                }
            },
            yAxis: {
                title: {
                    text: 'Process Values'
                }
            },
            xAxis: {
                title: {
                    text: "Month"
                },
                type: 'datetime',
                dateTimeLabelFormats: {
                    millisecond: '%H:%M:%S.%L',
                    second: '%H:%M:%S',
                    minute: '%H:%M',
                    hour: '%H:%M',
                    day: '%e. %b',
                    week: '%e. %b',
                    month: '%b \'%y',
                    year: '%Y'
                }
            },
            tooltip: {
                headerFormat: '{point.x:%e/%m/%Y (%b)  %l:%M %p}<br>',
                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
                shared: true,
                crosshairs: true,
                useHTML: true,
                valueSuffix: chartData.chart_data[0].valuesuffix
            },
            series: chartData.chart_data[0].data,
            lang: {
                noData: 'Data is not available.'
            },
            noData: {
                style: {
                    fontWeight: 'bold',
                    fontSize: '20px',
                    color: '#539fb8',
                }
            },
        });
    }
    callback(true);
}


/**
 * This function creates or update solid gauge highchart as per given param
 * @method updateSpeedometerChart
 */
function updateSpeedometerChart(chartData, div_id, div_text, callback) {

    var val_count = chartData.chart_data[0].data[0].count,
        val_color = chartData.chart_data[0].data[0].color,
        max = chartData.chart_data[0].data[0].max,
        stops = chartData.chart_data[0].data[0].stops;

    // If chart is created on given dom element then destriy chart n then create again
    if($(div_id).highcharts()) {
        $(div_id).highcharts().destroy();
    }

    // Create New Solid Gauge Chart
    var gaugeOptions = {
        chart: {
            type: 'solidgauge'
        },
        // title: null,
        title: "",
        pane: {
            center: ['50%', '85%'],
            size: '140%',
            startAngle: -90,
            endAngle: 90,
            background: {
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                innerRadius: '60%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },
        tooltip: {
            enabled: false
        },
        credits: {
            enabled: false
        },
        // the value axis
        yAxis: {
            lineWidth: 0,
            minorTickInterval: null,
            tickPixelInterval: 400,
            tickWidth: 0,
            title: {
                y: -70
            },
            labels: {
                y: 16
            }
        },
        plotOptions: {
            solidgauge: {
                dataLabels: {
                    y: 5,
                    borderWidth: 0,
                    useHTML: true
                }
            }
        }
    };

    gauge_val_default_color = val_count != 0 ? val_color : "#333333";

    $(div_id).highcharts(Highcharts.merge(gaugeOptions, {
        yAxis: {
            min: 0,
            max: max,
            tickInterval: max,
            title: {
                // text: div_text
                text: ""
            },
            stops: stops,
        },
        series: [{
            name: div_text,
            data: [val_count],
            dataLabels: {
            format: '<div style="text-align:center"><span style="'+gauge_chart_val_style+'color:' +
                ((Highcharts.theme && Highcharts.theme.contrastTextColor) || gauge_val_default_color) + '">{y:1f}</span><br/>'+
                '<span style="font-size:12px;color:silver">Hosts</span></div>'
            },
            tooltip: {
                valueSuffix: ' revolutions/min'

            }
        }]
    }));
    callback(true);
}


/**
 * This event trigger when any trends icon is clicked
 * @event click
 */
$("#main_dashboard_container .box-body h5 strong i, #main_dashboard_container .box-body h4 strong i").click(function(e) {

    // show the loader
    showSpinner();

    var trends_id = e.currentTarget.id ? e.currentTarget.id : "",
        chart_dom_id = trends_id.split("_trend")[0],
        trends_url = "",
        window_title = "";

    if(solid_gauge_chart_ids.indexOf(chart_dom_id) > -1) {
        trends_url = solid_gauge_url_obj[chart_dom_id]["trends_url"] ? $.trim(solid_gauge_url_obj[chart_dom_id]["trends_url"]) : "";
        window_title = solid_gauge_url_obj[chart_dom_id]["text"] ? solid_gauge_url_obj[chart_dom_id]["text"]+" - " : "";
    } else if(area_chart_ids.indexOf(chart_dom_id) > -1) {
        trends_url = area_chart_url_obj[chart_dom_id]["trends_url"] ? $.trim(area_chart_url_obj[chart_dom_id]["trends_url"]) : "";
        window_title = area_chart_url_obj[chart_dom_id]["text"] ? area_chart_url_obj[chart_dom_id]["text"]+" - " : "";
    } else if(pie_chart_ids.indexOf(chart_dom_id) > -1) {
        trends_url = pie_chart_url_obj[chart_dom_id]["trends_url"] ? $.trim(pie_chart_url_obj[chart_dom_id]["trends_url"]) : "";
        window_title = pie_chart_url_obj[chart_dom_id]["text"] ? pie_chart_url_obj[chart_dom_id]["text"]+" - " : "";
    } else {
        // pass
    }

    if(trends_url) {
        $.ajax({
            "url" : base_url+""+trends_url,
            "type" : "GET",
            success : function(result) {
                var response = "";
                if(typeof result == 'string') {
                    response = JSON.parse(result);
                } else {
                    response = result;
                }

                if(response.success) {
                    var useful_data = response.data.objects,
                        condition = useful_data && useful_data.chart_data && useful_data.chart_data.length > 0;

                    if(condition) {

                        var popup_html = "";

                        popup_html += "<div class='trends_chart_container' align='center' style='position:relative;overflow:auto;'>";
                        popup_html += "<div id='trends_chart' style='position:relative;width:100%;'></div>";
                        popup_html += "<div class='clearfix'></div>";
                        popup_html += "</div>";

                        /*Call the bootbox to show the popup with datatable*/
                        bootbox.dialog({
                            message: popup_html,
                            title: '<i class="fa fa-signal">&nbsp;</i> '+window_title+'Trends'
                        });


                        // Update Modal width to 90%;
                        $(".modal-dialog").css("width","90%");
                        
                        // Create Chart
                        createHighChart_nocout(useful_data,'trends','#333333', false, function(status) {
                            // 
                        });

                        try {
                            setTimeout(function() {
                                // Resize the window to show highchart in proper bounds
                                $(window).resize();
                            },100)
                        } catch(e) {
                            // Pass
                        }
                    }
                } else {
                    $.gritter.add({
                        title: window_title+'Trends',
                        text: response.message,
                        sticky: false,
                        time : 1000
                    });
                }

            },
            error : function(err) {
                // console.log(err.statusText);
            },
            complete : function() {
                // hide the loader
                hideSpinner();
            }

        });
    } else {
        // hide the loader
        hideSpinner();
    }
});