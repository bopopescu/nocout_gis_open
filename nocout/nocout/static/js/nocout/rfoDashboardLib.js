/**
 * This file contains the script to load RFO dashboard data & also maintain the filters
 * @for RFO Dashboard
 * @uses jQuery, Highcharts
 */

var chart_colors_list = [
        '#7cb5ec', '#434348', '#90ed7d', '#f7a35c', '#8085e9', 
        '#f15c80', '#e4d354', '#2b908f', '#f45b5b', '#91e8e1',
        '#2f7ed8', '#0d233a', '#8bbc21', '#910000', '#1aadce', 
        '#492970', '#f28f43', '#77a1e5', '#c42525', '#a6c96a',
        '#4572A7', '#AA4643', '#89A54E', '#80699B', '#3D96AE', 
        '#DB843D', '#92A8CD', '#A47D7C', '#B5CA92', '#d69e9f',
        '#1c3066', '#0a3c5d', '#2f6494', '#2f70a6', '#2c5d8a',
        '#2a5a85', '#1f21f2', '#1f5a78', '#1d4263', '#1c3f5e',
        '#001fb7', '#0d31ff', '#0b2536', '#0000ff', '#f04f2d',
        '#36939e', '#9e466b', '#453e5b', '#ffceb4', '#e0301e',
        '#23c5e3', '#c5e323', '#a8f2c3', '#6fd6a5', '#ffceb4',
        '#e1ac96', '#3c2e28', '#53856d', '#b24747', '#a5e79b',
        '#77e180', '#488864', '#8e92a2', '#ff0033', '#9bc7ae',
        '#528969', '#ffdeed', '#b296a2', '#fb6547', '#e58e7c'
    ];

/**
 * This event trigger when any filter control selectbox value changed
 * @event Change
 */
$('.filter_controls').change(function(e) {
    
    // When state select then show cities of that state only
    if ($(this).attr('name').indexOf('state') > -1) {
        var selected_val = $(this).val();
        $('select[name="city_selector"] option').show();
        if (selected_val) {
            $('select[name="city_selector"]').val('');
            $('select[name="city_selector"] option:not([parent_id="'+selected_val+'"])').hide();
            $('select[parent_id="'+selected_val+'"] option').show();
        }
    }

    initRfoDashboard();
});

/**
 * This function updates given filter selectbox values as per given data
 * @method updateFiltersContent
 * @param dataset {Array}, It contains the data which has to be populate in respective selectbox
 * @param filter_name {String}, It contains the prefix name(unique) of selectbox
 * @param filter_title {String}, It contains the filter title which shown in blank value of selectbox
 */
function updateFiltersContent(dataset, filter_name, filter_title) {
    var selector_id = 'select[name="' + filter_name + '_selector"]';
    if ($(selector_id).length) {
        
        var selectbox_html = '<option value="">Select '+filter_title+'</option>';
        if (filter_name == 'month') {
            var selectbox_html = '';
        }

        for (var i=0; i<dataset.length; i++) {
            if (filter_name == 'month') {
                try {
                    var id = dataset[i]['id'],
                        timestamp_obj = new Date(Number(id));

                    var value = month_dict[timestamp_obj.getMonth()] + ' - ' + timestamp_obj.getFullYear(),
                        selected_item = '';
                    
                    if (i == dataset.length - 1) {
                        selected_item = 'SELECTED="SELECTED"';
                    }

                    selectbox_html += '<option value="' + id + '" ' + selected_item + '>' + value + '</option>';
                } catch(e) {
                    // console.error(e);
                }
            } else {
                var parent_id = '';
                if (filter_name == 'city') {
                    parent_id = dataset[i]['state_id'];
                }
                try {
                    selectbox_html += '<option parent_id="' + parent_id + '" value="' + dataset[i]['id'] + '">' + dataset[i]['value'] + '</option>';
                } catch(e) {
                    // console.error(e);
                }
            }
        }

        $(selector_id).html(selectbox_html);
    }
}

/**
 * This function initializes RFO dashboard. It calls function to poplates charts/tables.
 * @method initRfoDashboard
 */
function initRfoDashboard() {
    var display_type = $('select[name="display_selector"]').val(),
        selected_month = $('select[name="month_selector"]').val(),
        selected_state = $('select[name="state_selector"]').val(),
        selected_city = $('select[name="city_selector"]').val(),
        load_table = true,
        load_chart = false;

    if (selected_month) {
        selected_month = Number(selected_month) / 1000;
    }

    if (display_type == 'both') {
        load_chart = true;
        load_table = true;
        if ($('.chart_view_container').hasClass('hide')) {
            $('.chart_view_container').removeClass('hide');
        }
        if ($('.both_view_seperator').hasClass('hide')) {
            $('.both_view_seperator').removeClass('hide');
        }
        if ($('.table_view_container').hasClass('hide')) {
            $('.table_view_container').removeClass('hide');
        }

    } else if (display_type == 'chart') {
        load_chart = true;
        load_table = false;
        if ($('.chart_view_container').hasClass('hide')) {
            $('.chart_view_container').removeClass('hide');
        }
        if (!$('.both_view_seperator').hasClass('hide')) {
            $('.both_view_seperator').addClass('hide');
        }
        if (!$('.table_view_container').hasClass('hide')) {
            $('.table_view_container').addClass('hide');
        }
    } else {
        load_chart = false;
        load_table = true;
        if (!$('.chart_view_container').hasClass('hide')) {
            $('.chart_view_container').addClass('hide');
        }
        if (!$('.both_view_seperator').hasClass('hide')) {
            $('.both_view_seperator').addClass('hide');
        }
        if ($('.table_view_container').hasClass('hide')) {
            $('.table_view_container').removeClass('hide');
        }
    }

    if (load_table) {
        // Load All data datatables
        dataTableInstance.createDataTable(
            'rfo_data_table',
            all_data_headers,
            all_data_url + '?month=' + String(selected_month)+'&state_name=' + selected_state + '&city_name='+ selected_city,
            false
        );

        // Load Summation data datatables
        dataTableInstance.createDataTable(
            'rfo_summation_table',
            summation_headers,
            summation_url + '?month=' + String(selected_month)+'&state_name=' + selected_state + '&city_name='+ selected_city,
            false
        );
    }

    if (load_chart) {
        loadRFOColumnChart(summation_url,String(selected_month), selected_state, selected_city);
    }

    // Hide Loading Spinner
    hideSpinner();
}

/**
 * This function fetch data & loads master cause code column chart
 * @method loadRFOColumnChart
 * @param ajax_url {String}, If contains the API url to fetch master cause code data
 * @param month {Integer}, It contains epoch timestamp for selected month
 * @param selected_state {String}, If contains the selected state value(if any)
 * @param selected_city {String}, If contains the selected city value(if any)
 */
function loadRFOColumnChart(ajax_url, month, selected_state, selected_city) {

    $.ajax({
        url: ajax_url + '?month='+month+'&request_for_chart=1&state_name=' + selected_state + '&city_name='+ selected_city,
        type: 'GET',
        success: function(response) {

            if (typeof(response) == 'string') {
                response = JSON.parse(response);
            }

            if (response['result'] == 'ok') {
                var current_dateobj = new Date(Number(month) * 1000),
                    month_txt = month_dict[current_dateobj.getMonth()],
                    year_txt = current_dateobj.getFullYear(),
                    year_month_str = month_txt && year_txt ? month_txt + ' ' + year_txt : '';
                var column_series_data = [],
                    categories = [];

                for (var i=0;i<response['aaData'].length;i++) {
                    categories.push(response['aaData'][i]['master_causecode'])
                    column_series_data.push({
                        'name': response['aaData'][i]['master_causecode'],
                        'type': 'column',
                        'data': [response['aaData'][i]['outage_in_minutes']]
                    })
                }

                // Initialize column chart for master cause code
                $('#rfo_column_chart_container').highcharts({
                    chart: {
                        type: 'column'
                    },
                    colors: chart_colors_list,
                    title: {
                        text: 'PB TT RFO Analysis ' + year_month_str,
                        align: 'left'
                    },
                    xAxis: {
                        categories: [''],
                        title: {
                            text: 'Master Cause Code'
                        }
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: 'Outage In Minutes'
                        },
                        labels: {
                            overflow: 'justify'
                        }
                    },
                    tooltip: {
                        formatter: function () {
                            var series_name = this.series.name ? $.trim(this.series.name) : "Value",
                                tooltip_html = "";

                            tooltip_html += '<ul><li><b>Master Cause Code</b></li><br/>';
                            tooltip_html += '<li>'+series_name+' : '+this.point.y+'</li><br/></ul>';

                            return tooltip_html;
                        }
                    },
                    legend: {
                        itemDistance : 15,
                        itemMarginBottom : 5,
                        borderColor : "#CCCCCC",
                        borderWidth : "1",
                        borderRadius : "8",
                        itemStyle: {
                            color: '#555555',
                            fontSize : '10px'
                        },
                        layout: 'vertical',
                        align: 'right',
                        verticalAlign: 'top'
                        // width : "100%"
                    },
                    credits: {
                        enabled: false
                    },
                    plotOptions: {
                        column: {
                            pointWidth: 12,
                            groupPadding: 0
                        },
                        series: {
                            point: {
                                events: {
                                    click: function(e) {
                                        // Show Loading Spinner
                                        showSpinner();

                                        var series_name = this.series.name,
                                            series_value = this.y;
                                        
                                        // Fetch clicked point sub cause code data
                                        var sub_data_url = '';
                                        sub_data_url += all_data_url;
                                        sub_data_url += '?month='+month;
                                        sub_data_url += '&request_for_chart=1&search[value]='+series_name;
                                        sub_data_url += '&state_name=' + selected_state;
                                        sub_data_url += '&city_name='+ selected_city

                                        // Call "createFaultPieChart" to show pie chart in popup
                                        createFaultPieChart(sub_data_url, series_name);
                                    }
                                }
                            }
                        }
                    },
                    series: column_series_data,
                    noData: {
                        style: {
                            fontWeight: 'bold',
                            fontSize: '20px',
                            color: '#539fb8',
                        }
                    }
                });
            }
        },
        error: function(err) {
            console.log(err.statusText);
        }
    });
}

/**
 * This function fetch & load sub cause code pie chart as per the given params
 * @method createFaultPieChart
 * @param api_url {String}, It contains the url of api to fetch sub cause code data
 * @param master_causecode_name {String}, It contains name of master code for which the sub cause code data is to be drawn
 */
function createFaultPieChart(api_url, master_causecode_name) {

    var middle_legends = {
            itemDistance : 15,
            itemMarginBottom : 5,
            borderColor : "#CCCCCC",
            borderWidth : "1",
            borderRadius : "8",
            itemStyle: {
                color: '#555555',
                fontSize : '10px'
            }
        },
        side_legends = {
            itemDistance : 15,
            itemMarginBottom : 5,
            borderColor : "#CCCCCC",
            borderWidth : "1",
            borderRadius : "8",
            itemStyle: {
                color: '#555555',
                fontSize : '10px'
            },
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        };

    $.ajax({
        url: api_url,
        type: 'GET',
        success: function(all_data_response) {
            if (typeof(all_data_response) == 'string') {
                all_data_response = JSON.parse(all_data_response);
            }

            if (all_data_response['result'] == 'ok') {
                var data_list = all_data_response['aaData'],
                    pie_chart_data = [],
                    pie_dict = {},
                    names_list = [];
                for(var j=0; j<data_list.length; j++) {
                    var sub_causecode = data_list[j]['sub_causecode'] ? data_list[j]['sub_causecode'] : 'NA',
                        outage_time = data_list[j]['outage_in_minutes'] ? parseFloat(data_list[j]['outage_in_minutes']) : 0;

                    if (names_list.indexOf(sub_causecode) == -1) {
                        pie_dict[sub_causecode] = 0;
                        names_list.push(sub_causecode);
                    }

                    pie_dict[sub_causecode] += outage_time;
                }
                
                for(var key in pie_dict) {
                    if (pie_dict.hasOwnProperty(key)) {
                        pie_chart_data.push([key, pie_dict[key]])
                    }
                }

                var bootbox_html = '';

                bootbox_html += '<div class="pie_chart_container" align="center">\
                                    <div id="fault_pie_chart"></div>\
                                </div>';

                bootbox.dialog({
                    message: bootbox_html,
                    title: '<i class="fa fa-bar-chart">&nbsp;</i> Fault Segment - '+master_causecode_name
                });

                // Update Modal width to 90%;
                $(".modal-dialog").css("width","90%");
                
                var chart_legends = middle_legends;
                // If more items in chart then show legends in right side(vertically)
                if (pie_chart_data.length > 5) {
                    chart_legends = side_legends;
                }

                $('#fault_pie_chart').highcharts({
                    chart: {
                        type: 'pie'
                    },
                    colors: chart_colors_list,
                    title: {
                        text: ''
                    },
                    xAxis: {
                        // categories: categories,
                        title: {
                            text: 'Sub Cause Code'
                        }
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: 'Outage In Minutes'
                        },
                        labels: {
                            overflow: 'justify'
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
                    legend: chart_legends,
                    tooltip: {
                        formatter: function () {
                            var point_name = this.key ? $.trim(this.key) : "Value",
                                tooltip_html = "";

                            tooltip_html += '<ul><li><b>'+master_causecode_name+'</b></li><br/>';
                            tooltip_html += '<li>'+point_name+' : '+this.point.y+'</li><br/></ul>';

                            return tooltip_html;
                        }
                    },
                    credits: {
                        enabled: false
                    },
                    series: [{
                        data: pie_chart_data,
                        name: master_causecode_name,
                        title: master_causecode_name
                    }],
                    noData: {
                        style: {
                            fontWeight: 'bold',
                            fontSize: '20px',
                            color: '#539fb8',
                        }
                    }
                });
                
                // Hide Loading Spinner
                hideSpinner();
            }
        },
        error: function(err) {
            // console.log(err.statusText);
            // Hide Loading Spinner
            hideSpinner();
        }
    });
}