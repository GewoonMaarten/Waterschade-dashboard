
var user_data = {
    room: -1,
    sensor: -1
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
            db.child("notifications").child(user.uid).on('value', function (snapshot) {
                snapshot.forEach(function(v) {
                    var object = v.val();
                    console.log(object);
                    for(var i in object.triggers) {
                        var trigger = object.triggers[i];
                        if (trigger.activated) {
                            var message;
                            if (i === 'wind_speed') {
                                message = 'Windkracht ' + object.windPower + ' in de ' + object.windDirection.toLowerCase() + ' richting.';
                            }
                            var type;
                            var icon;
                            switch(trigger.severity) {
                                case 0:
                                    type = 'info';
                                    icon = 'fa fa-info-circle';
                                    break;
                                case 1:
                                    type = 'warning';
                                    icon = 'fa fa-exclamation-triangle';
                                    break;
                                case 2:
                                    type = 'danger';
                                    icon = 'fa fa-exclamation-circle';
                                    break;
                            }
                            $.notify({
                                title: v.key,
                                message: message,
                                icon: icon
                            }, {
                                type: type,
                                allow_dismiss: true
                            });
                        }
                    }
                });
            });
        }
    });
}

function bindEvents() {
    $('#login-form').submit(function(e) {
        e.preventDefault();
        var helper = $('#login-form').find('small');
        helper.text('');
        var button = $('#login-form').find('button');
        button.find('i').show();
        button.find('span').text('');
        var data = {
            email: $('input[name=email]').val(),
            password: $('input[name=password]').val()
        };
        $.post('/login', data, function(json) {
            if (json.error) {
                helper.text(json.error);
                button.find('i').hide();
                button.find('span').text('Login');
                return;
            }
            document.location.href = '/';
        });
    });
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
        user_data.sensor = parseInt($(this).parent().attr('value'));
        $.get('/api/rooms/' + user_data.room + '/devices/' + user_data.sensor + '/name', function(json) {
            $('#sensor-name').val(json.name);
            popup.show();
            popup.popup();
            popup.popup("open");
        });
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
                    $('#sensors').find('li').each(function(i) {
                        if (parseInt($(this).attr('value')) === user_data.sensor) {
                            $(this).find('a span').text(json.name);
                        }
                    });
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
                        var item = $('<li value="' + sensor.id + '"><a data-transition="slide"><i class="fa fa-plug sensor-' + status + '"></i><span>' + sensor.name + '</span></a><input type="checkbox" data-role="flipswitch"' + (sensor.status === 1 ? ' checked=""' : '') + '></li>');
                        list.append(item);
                        item.find('input').flipswitch();
                        item.find('input').change(function() {
                            var input = $(this);
                            var value = input.is(':checked');
                            user_data.sensor = parseInt(input.parent().parent().attr('value'));
                            $.ajax({
                                url: '/api/rooms/' + user_data.room + '/devices/' + user_data.sensor,
                                type: 'PUT',
                                data: {
                                    active: value
                                },
                                success: function(response) {
                                    if (response.error) {
                                        $.notify('<strong>Er is een fout opgetreden!</strong><br/>' + response.error);
                                    } else {
                                        if (response.active) {
                                            input.parent().prev().find('i').removeClass('sensor-inactive').addClass('sensor-active');
                                        } else {
                                            input.parent().prev().find('i').removeClass('sensor-active').addClass('sensor-inactive');
                                        }
                                    }
                                }
                            });
                        });
                    }
                    list.listview('refresh');
                });
                break;
        }
    });
}

$(document).on('pageshow', '#new-devices-dialog', () => { 

    $("#loading").show();

    function call(limit, callback) {
        let i = 0;
        let call = setInterval(() => {

            $('#device-list').empty();

            $.get('/api/devices/new', (result) => {
                if(result.length <= 0){
                    return result;
                }
            }).then( devices => {
                console.log(devices);
                for(let device of devices){
                    $("#device-list").append(`            
                    <div class="device">
                        <i class="fa fa-cube"></i>
                        <b>Water Sensor</b>
                        <p>id: ${device['id']}</p>
                        <hr />
                    </div>
                `)
                }
                $("#loading").hide();
                clearInterval(call);
                callback('done');
            });

            console.log(i);
            if (i === limit - 1) {
                $("#loading").hide();
                clearInterval(call);
                callback('done');
            }
            i++;
        }, 2000);
    }
    
    call(5, (x) => {
      console.log(x);
    });
});