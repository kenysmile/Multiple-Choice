$(document).ready(function() {
    $('.updateButton').on('click', function(event) {

        var student_id = $(this).attr('student_id');
        //console.log($(event.target).closet('form'));
        var ten = $('#tenInput'+student_id).val();
        var tuoi = $('#tuoiInput'+student_id).val();
        var diachi = $('#diachiInput'+student_id).val();
        var tenid = $('#tenidInput'+student_id).val();


        // console.log(JSON.stringify({ todo : todo, ngay : ngay, id : todo_id }));

        req = $.ajax({
            url : '/api/student',
            type : 'POST',
            data: JSON.stringify({id: student_id, ten: ten, tuoi: tuoi, diachi: diachi, tenid: tenid}),
            // data: JSON.stringify({id: todo_id}),

            contentType: 'application/json',
            dataType: 'json'
        }).done(function(data) {
            data = 'Edit thành công'
            alert(data)
        });
    

    });

});
