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
    $('#result').css('display','none');

    var formData = {}; 
    $('#submit').click(function(){
        $('#result').css('display','none');
        var selectedValues = [];
        $('#submit').css('display','none');
        $('.circle').show();
        const startTime = new Date().getTime();
        const time=0
        init(time);
        var timerId = setInterval( function () { timer(startTime); }, 1000);
            // 遍历所有复选框，如果选中则将其值加入 formData

        $('input,select').each(function () {
            formData[this.name] = $(this).val();
        });
        var checkboxes = document.querySelectorAll('input[name=interest]:checked');
        checkboxes.forEach(function(checkbox) {
            selectedValues.push(checkbox.value);
        });
        formData['checkbox_value'] = selectedValues;


    console.log(formData);
    $.ajax({
        url: '/web_tool/ajax_filter_web/', 
        data: formData,
        async: true,

        success: function(response){

            $('#circle').hide();
            $('#submit').show();
            $('#result').show();
       
            clearInterval(timerId)

            console.log(response)
            var columns_for_one_sig = [];
            var columns_for_two_sig = [];
            var columns_for_all_sig = [];
            if (response.columns_name_for_one_sig.length > 0) {
                // 取得第一行的字典
                var firstRow = response.columns_name_for_one_sig;
                // console.log(firstRow)
                for (var i = 0; i < firstRow.length; i++) {
                    var currentInfo = firstRow[i];
                    columns_for_one_sig.push({ data: currentInfo, title: currentInfo }); // 將每個鍵作為 data 和 title
                }
                // console.log(columns)

            }
            if (response.columns_name_for_two_sig.length > 0) {
                // 取得第一行的字典
                var firstRow_for_two_sig = response.columns_name_for_two_sig;
                // console.log(firstRow)
                for (var i = 0; i < firstRow_for_two_sig.length; i++) {
                    var currentInfo_for_two = firstRow_for_two_sig[i];
                    columns_for_two_sig.push({ data: currentInfo_for_two, title: currentInfo_for_two }); // 將每個鍵作為 data 和 title
                }
                // console.log(columns)

            }
            if (response.columns_name_for_all_sig.length > 0) {
                // 取得第一行的字典
                var firstRow_for_all = response.columns_name_for_all_sig;
                // console.log(firstRow)
                for (var i = 0; i < firstRow_for_all.length; i++) {
                    var currentInfo_for_all = firstRow_for_all[i];
                    columns_for_all_sig.push({ data: currentInfo_for_all, title: currentInfo_for_all }); // 將每個鍵作為 data 和 title
                }
                // console.log(columns)

            }
            
            table_one_sig=$('#one_siganl_table').DataTable({
                "bDestroy": true,
                lengthChange: false, // "Show X entries"
                data: response.data_for_one_sig,
                scrollX: true,
                scrollCollapse: true,
                columns: columns_for_one_sig
            });
            table_two_sig=$('#two_siganl_table').DataTable({
                "bDestroy": true,
                lengthChange: false, // "Show X entries"
                data: response.data_for_two_sig,
                scrollX: true,
                scrollCollapse: true,
                columns: columns_for_two_sig
            });
            table_all_sig=$('#all_siganl_table').DataTable({
                "bDestroy": true,
                lengthChange: false, // "Show X entries"
                data: response.data_for_all_sig,
                scrollX: true,
                scrollCollapse: true,
                columns: columns_for_all_sig
            });

                    },
                    error: function(){
                        alert('Something error');}
                    
            
            });
                


    })
   
    $('#two_siganl_table').on('click', 'td', function () {
        // table_detail = $('#result_table tbody').DataTable()
 
        $('#container').empty()
        var tabledetail = $('<table>').addClass('table table-hover').attr('id', 'result_table')
        $('#container').append(tabledetail);
        form_data_list={}
        var columnIndex = $(this).index(); // 獲取點擊的欄位的索引
        console.log(columnIndex)
        var columnName = $('#two_siganl_table thead th').eq(columnIndex).text();
        console.log(columnName)
        form_data_list['patient_number'] = columnName;
        data_number=parseInt($(this).text());
        var $tr = $(this).closest('tr'); // 获取点击的td元素所在的tr元素
        var rowData = table_two_sig.row($tr).data();
        console.log(rowData);
        form_data_list['Func_refGene'] = rowData['Func_refGene'];
        form_data_list['Gene_refGene'] = rowData['Gene_refGene'];
        console.log(form_data_list);
        mergedObj = Object.assign({}, form_data_list, formData);
        console.log(mergedObj);

        if (Number.isInteger(data_number) && data_number !== 0){
            $.ajax({
                url: '/web_tool/ajax_for_two_sig_detail/', 
                data: mergedObj,
                async: true,
                // beforeSend:function(){
                //     var count=0
                //     tID= setInterval(timedCount , 50);
                //         function timedCount() {
                //         count=count+0.05;
                //         swal({
                //             title: "Running...",
                //             text: "It may take several minutes.\nPlease be patient.\n \nRunning time: "+parseInt(count)+" seconds\nClick anywhere of the page \nif the running time does not change",                       
                //             button: false,
                //         });
                //     };
                // },   
                success: function(response){
                    // swal.close();
                    // clearInterval(tID);
                    // delete tID
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
    $('#one_siganl_table').on('click', 'td', function () {
        // table_detail = $('#result_table tbody').DataTable()
 
        $('#container').empty()
        var tabledetail = $('<table>').addClass('table table-hover').attr('id', 'result_table')
        $('#container').append(tabledetail);
        form_data_list={}
        var columnIndex = $(this).index(); // 獲取點擊的欄位的索引
        console.log(columnIndex)
        var columnName = $('#one_siganl_table thead th').eq(columnIndex).text();
        console.log(columnName)
        form_data_list['patient_number'] = columnName;
        data_number=parseInt($(this).text());
        var $tr = $(this).closest('tr'); // 获取点击的td元素所在的tr元素
        var rowData = table_one_sig.row($tr).data();
        console.log(rowData);
        form_data_list['Gene_refGene'] = rowData['Gene_refGene'];
        console.log(form_data_list);
        mergedObj = Object.assign({}, form_data_list, formData);
        console.log(mergedObj);

        if (Number.isInteger(data_number) && data_number !== 0){
            $.ajax({
                url: '/web_tool/ajax_for_one_sig_detail/', 
                data: mergedObj,
                async: true,
                // beforeSend:function(){
                //     var count=0
                //     tID= setInterval(timedCount , 50);
                //         function timedCount() {
                //         count=count+0.05;
                //         swal({
                //             title: "Running...",
                //             text: "It may take several minutes.\nPlease be patient.\n \nRunning time: "+parseInt(count)+" seconds\nClick anywhere of the page \nif the running time does not change",                       
                //             button: false,
                //         });
                //     };
                // },   
                success: function(response){
                    // swal.close();
                    // clearInterval(tID);
                    // delete tID
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
                    table_detail_one = $('#result_table').DataTable({
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

})