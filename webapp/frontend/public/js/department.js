$(document).ready(function () {

    (function () {




        $('#add-row').click(function (event) {
            event.preventDefault();
            $('#real-table').append('<tr><td style="width:40%"><input type="text" placeholder="Department Name" class = "course-name"/></td><td style="width:10%"><input type="text" placeholder="Team Size" class = "duration"/></td><td style="width:10%"><input type="text" placeholder="Responsible?" class = "duration"/></td></tr>');

            // $('#real-table').append('<tr>')
            // $('#real-table').append('<td style="width:30%"><input type="text" placeholder="School Address" class = "course-name"/></td>')
            // $('#real-table').append('<td style="width:5%"><input type="text" placeholder="Duration" class = "duration"/></td>')
            // $('#real-table').append('<td style="width:5%"><input type="text" placeholder="# of students" class = "num-student"/></td>')
            // $('#real-table').append('<td style="width:5%"><input type="text" placeholder="Grade" class = "grade"/></td>')
            // $('#real-table').append('</tr>')
        });

    })(); //end SIAF

}); //end document.ready
