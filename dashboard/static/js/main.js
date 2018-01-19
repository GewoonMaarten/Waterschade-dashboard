var editMode = false;

var user_data = {
    room: -1,
    sensor: -1,
    sensors: []
};

$(function() {
    loop();
    $('#edit-sensor-button').click(function () {
        editMode = !editMode;
        if (editMode) {
            $(this).find('i').removeClass('fa-pencil-square-o').addClass('fa-check');
            $('#sensors').find('div[data-role=collapsible]').removeClass('ui-disabled');
        } else {
            $(this).find('i').removeClass('fa-check').addClass('fa-pencil-square-o');
            $('#sensors').find('div[data-role=collapsible]').addClass('ui-disabled');
        }
    });
    $('#settings-rooms').find('.mobile-list').on('click', 'li a', function() {
        var id = parseInt($(this).parent().attr('value'));
        $('#room-title').text('Kamer ' + id);
    });

    $('#container').on('pagebeforeshow', 'div[data-role="page"]', function() {
        var id = $(this).attr('id').replace('#', '');
        console.log('switching to page=' + id);
        switch(id) {
            case 'home':
                //TODO Refresh dahsboard via ajax
                $('#sensor-count').text(random() + ' Sensoren actief');
                $('#damage-occurrences').text(random());
                $('#temperature').text(random() + '°C');
                break;
            case 'settings-rooms':
                $.get('/api/rooms', function(json) {
                    var list = $('#settings-rooms').find('.mobile-list');
                    list.empty();
                    for(var i in json) {
                        var room = json[i];
                        var item = $('<li value="' + room.id + '"><a href="#settings-room" data-transition="slide"><i class="fa fa-bed"></i>' + room.name + '</a></li>');
                        list.append(item);
                    }
                    user_data.rooms = json;
                    list.listview('refresh');
                });
                break;
            case 'settings-room':
                $.get('/api/rooms/' + user_data.room + '/sensors', function(json) {
                    var list = $('#sensors');
                    list.empty();
                    for(var i in json) {
                        var sensor = json[i];
                        var status = sensor.status === 1 ? 'active' : 'inactive';
                        var flipper = $('<input type="checkbox" data-role="flipswitch">');
                        var item = $('<li><a data-transition="slide"><i class="fa fa-bed"></i>' + sensor.name + '</a></li>');
                        item.append(flipper);
                        //var item = $('<div class="ui-disabled" data-role="collapsible" data-collapsed-icon="carat-d" data-expanded-icon="carat-u" data-iconpos="right"><h3><i class="fa fa-plug sensor-' + status + '"></i> ' + sensor.name + '</h3><div class="ui-field-contain"><label>Naam:</label><input type="text" placeholder="Voer een naam in..." value="' + sensor.name + '"></div></div>');
                        list.append(item);
                        item.find('input').flipswitch();
                    }
                    user_data.sensors = json;
                    list.listview("refresh");
                });
                break;
        }
    });
});

var nextColon = true;
var monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];
var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

function updateTime() {
    var date = new Date();
    var colon = (nextColon = !nextColon) ? ':' : ' ';
    var time = pad(date.getHours()) + colon + pad(date.getMinutes());
    var day = date.getDate() + ' ' + monthNames[date.getMonth()] + ' ' + date.getFullYear();
    $('#time').text(time);
    $('#date').text(days[date.getDay()]);
    $('#full-date').text(day);
}

 function pad(number) {
    return number < 10 ? 0 + '' + number : number;
}

function loop() {
    setTimeout(function () {
        updateTime();
        loop();
    }, 1000);
}

function random() {
    return parseInt(Math.random() * 10);
}