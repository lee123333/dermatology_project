$.ajaxSetup({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
});

function init(seconds) {
    update(seconds);
}
// update progess with the timer.
function update (seconds) {
    textRenderer(seconds);
}
// refresh the text of the bar.
function textRenderer (seconds) {
    var sec = seconds % 60;  
    var min = Math.floor(seconds / 60);  
    min = min.toString().padStart(2, '0');
    sec = sec.toString().padStart(2, '0');

    $(".text").text('time '+min + ":" + sec);		
}
function timer (startTime) {
    // 當前時間。
    var currentTime = new Date().getTime();
    
    // 當前時間 - 起始時間 = 經過時間。(因為不需要毫秒，所以將結果除以1000。)
    var diffSec = Math.round((currentTime - startTime) / 1000);
    // update progess.  
    update(diffSec);   
    
}


$(document).ready(function(){
    // $('#result').css('display','none');
    var formData = {};
    var func_list = document.getElementById('func_list').getAttribute('data-json').replace(/[\[\]\'()]/g, '').split(/,\s*/);

    var gene_list = document.getElementById('gene_list').getAttribute('data-json').replace(/[\[\]\'()]/g, '').split(/,\s*/);
    console.log(func_list)
    $('#func').autocomplete({
        source:func_list,
        minLength: 3,
        delay: 0,
    });
    $('#genes').autocomplete({
        source:gene_list,
        minLength: 4,
        delay: 0,
        width:10,
    });
    $('#submit').click(function(){

        // $('#submit').css('display','none');
        // $('.circle').show();
        const startTime = new Date().getTime();
        const time=0
        init(time);
        var timerId = setInterval( function () { timer(startTime); }, 1000);
            // 遍历所有复选框，如果选中则将其值加入 formData

        $('#func,#genes').each(function () {
            formData[this.name] = $(this).val();
        });



    console.log(formData);
    $.ajax({
        url: '/web_tool/ajax_test/', 
        data: formData,
        async: true,

        success: function(response){

            // $('#circle').hide();
            // $('#submit').show();
            $('#result').show();
       
            // clearInterval(timerId)

            console.log(response)
            var columns = [];
            if (response.columns_name.length > 0) {
                // 取得第一行的字典
                var firstRow = response.columns_name;
                // console.log(firstRow)
                for (var i = 0; i < firstRow.length; i++) {
                    var currentInfo = firstRow[i];
                    columns.push({ data: currentInfo, title: currentInfo }); // 將每個鍵作為 data 和 title
                }
                console.log(columns)

            }
            
            table=$('#123').DataTable({
                "bDestroy": true,
                lengthChange: false, // "Show X entries"
                data: response.data,
                scrollX: true,
                scrollCollapse: true,
                columns: columns
            });

                    },
                    error: function(){
                        alert('Something error');}
                    
            
            });
                


    })
   
    $('#123').on('click', 'td', function () {
        // table_detail = $('#result_table tbody').DataTable()
 
        $('#container').empty()
        var tabledetail = $('<table>').addClass('table table-hover').attr('id', 'result_table')
        $('#container').append(tabledetail);
        form_data_list={}
        var columnIndex = $(this).index(); // 獲取點擊的欄位的索引
        console.log(columnIndex)
        var columnName = $('#123 thead th').eq(columnIndex).text();
        console.log(columnName)
        form_data_list['patient_number'] = columnName;
        data_number=parseInt($(this).text());
        var $tr = $(this).closest('tr'); // 获取点击的td元素所在的tr元素
        var rowData = table.row($tr).data();
        console.log(rowData);
        form_data_list['Func_refGene'] = rowData['Func_refGene'];
        form_data_list['Gene_refGene'] = rowData['Gene_refGene'];
        console.log(form_data_list);
        if (Number.isInteger(data_number) && data_number !== 0){
            $.ajax({
                url: '/web_tool/ajax_find_alldata/', 
                data: form_data_list,
                async: true,
                beforeSend:function(){
                    var count=0
                    tID= setInterval(timedCount , 50);
                        function timedCount() {
                        count=count+0.05;
                        swal({
                            title: "Running...",
                            text: "It may take several minutes.\nPlease be patient.\n \nRunning time: "+parseInt(count)+" seconds\nClick anywhere of the page \nif the running time does not change",                       
                            button: false,
                        });
                    };
                },   
                success: function(response){
                    swal.close();
                    clearInterval(tID);
                    delete tID
                    var columns_for_tabledetail = [];
                    if (response.columns_name.length > 0) {
                        // 取得第一行的字典
                        var Row = response.columns_name;
                        // console.log(firstRow)
                        for (var i = 0; i < Row.length; i++) {
                            var Info = Row[i];
                            columns_for_tabledetail.push({ data: Info, title:Info }); // 將每個鍵作為 data 和 title
                        }
                        console.log(columns_for_tabledetail)
        
                    }
                    table_detail = $('#result_table').DataTable({
                        "bDestroy": true,
                        "destroy": true,
                        data: response.data,
                        scrollX: true,
                        scrollCollapse: true,
                        columns: columns_for_tabledetail,
                        "bAutoWidth": false
                    });
                   
                    
                   
                    },
                error: function(){
                    alert('Something error');}
                            
                    
                    });
                    $("#staticBackdrop").modal("show");

        }
      
        
    });
    // $("select").change(function() {

    //     let counterIntervalId = startCounter();

    //     var formData = {};
    //     $('select').each(function () {
    //         formData[this.name] = $(this).val();
    //     });

    //     var formData = {};
    //     $('select').each(function () {
    //         formData[this.name] = $(this).val();
    //     });

    //     $.ajax({
    //         url: '/stock/ajax_finlabBacktest/', 
    //         data: formData,
    //         success: function(response){
    //             loadingContainer.hide();
    //             loadingbackground.hide();
    //             secondsCounter.hide();
    //             clearInterval(counterIntervalId);

    //             // 將每個100 轉換為 null
    //             var new_highcharts_data = response.highcharts_data.map(item => ({
    //                 name: item.name,
    //                 data: item.data.map(value => value === 100 ? null : value)
    //             }));

    //             all_output(response.all_result_data)
    //             highcharts(new_highcharts_data, response.date_list)
    //         }
    //     });
    // });


})