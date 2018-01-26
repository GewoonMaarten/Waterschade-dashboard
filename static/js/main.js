
var user_data = {
    room: -1,
    sensor: -1,
    sensors: []
};

$(function() {
    loop();
    connectSmartCities();
    bindEvents();
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

function connectSmartCities() {
    var config = {
        apiKey: "AIzaSyBQGAOw3TcQOhHd6ZMnFX8HraBtCsKxB7o",
        authDomain: "smartcities-d2e38.firebaseapp.com",
        databaseURL: "https://smartcities-d2e38.firebaseio.com/",
        storageBucket: "gs://smartcities-d2e38.appspot.com"
    };
    firebase.initializeApp(config);
    var auth = firebase.auth();
    auth.signInWithEmailAndPassword("admin@admin.nl", "adminadmin");
    auth.onAuthStateChanged(function(user) {
        if (user) {
            var db = firebase.database().ref();
            db.child("meldingen").child(user.uid).on('value', function (snapshot) {
                snapshot.forEach(function(v) {
                    var object = v.val();
                    console.log(object);
                    $.notify('<strong>' + v.key + '</strong><br/>Huidige regen status:' + object.regenStatus + '', { allow_dismiss: true });
                });
            });
        }
    });
}

function bindEvents() {
    $('.header-dropdown ul').click(function() {
        var menu = $(this).next();
        var hidden = menu.css('display') === 'none';
        if (hidden) {
            menu.show();
        } else {
            menu.hide();
        }
    });
    var popup = $('#sensor-popup');
    $('#settings-rooms').find('.mobile-list').on('click', 'li a', function() {
        var id = parseInt($(this).parent().attr('value'));
        user_data.room = id;
        $('#room-title').text('Kamer ' + id);
    });
    $('#sensors').on('click', 'li > a', function() {
        var sensor = user_data.sensors[parseInt($(this).parent().attr('value'))];
        $('#sensor-name').val(sensor.name);
        popup.show();
        popup.popup();
        popup.popup("open");
        user_data.sensor = sensor.id;
    });
    popup.find('button').click(function(e) {
        $.ajax({
            url: '/api/rooms/' + user_data.room + '/devices/' + user_data.sensor,
            type: 'PUT',
            data: {
                name: $('#sensor-name').val()
            },
            success: function(json) {
                if (json.error) {
                    $('#sensor-popup').find('.help-block').text(json.error);
                } else {
                    popup.popup("close");
                }
            }
        });
    });

    $('#container').on('pagebeforeshow', 'div[data-role="page"]', function() {
        var id = $(this).attr('id').replace('#', '');
        console.log('switching to page=' + id);
        switch(id) {
            case 'home':
                var city = 'Amersfoort';
                //TODO Refresh dahsboard via ajax
                $.get('/api/devices/active', function(result) {
                    $('#sensor-count').text(result + ' Sensoren actief');
                });
                $.get('/api/temperature/' + city, function(result) {
                    $('#temperature').text(result + '°C');
                });
                $.get('/api/damages', function(json) {
                    $('#damage-occurrences').text(json.length);
                });
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
                $.get('/api/rooms/' + user_data.room + '/devices', function(json) {
                    var list = $('#sensors');
                    list.empty();
                    for(var i in json) {
                        var sensor = json[i];
                        var status = sensor.status === 1 ? 'active' : 'inactive';
                        var item = $('<li value="' + i + '"><a data-transition="slide"><i class="fa fa-plug sensor-' + status + '"></i>' + sensor.name + '</a><input type="checkbox" data-role="flipswitch"' + (sensor.status === 1 ? ' checked=""' : '') + '></li>');
                        list.append(item);
                        item.find('input').flipswitch();
                        item.find('input').change(function() {
                            var value = $(this).is(':checked');
                            user_data.sensor = parseInt($(this).parent().parent().attr('value'));
                            $.ajax({
                                url: '/api/rooms/' + user_data.room + '/devices/' + user_data.sensor,
                                type: 'PUT',
                                data: {
                                    active: value
                                },
                                success: function(response) {
                                    if (response.error) {
                                        $.notify('<strong>Er is een fout opgetreden!</strong><br/>' + response.error);
                                    }
                                }
                            });
                        });
                    }
                    user_data.sensors = json;
                    list.listview('refresh');
                });
                break;
        }
    });
}