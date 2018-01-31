
let user_data = {
    room: -1,
    sensor: -1,
    contact: -1
};

$(function() {
    $.get('/api/devices/active', function(json) {
        $('#sensor-count').text(json.length + ' Sensoren actief');
    });
    loop();
    bindEvents();
    $('#wifi-form').submit(function(e) {
        e.preventDefault();
        let helper = $('#wifi-form').find('small');
        helper.text('');
        let button = $('#wifi-form').find('button');
        button.find('i').show();
        button.find('span').text('');
        let data = {
            ssid: $('input[name=ssid]').val(),
            password: $('input[name=password]').val()
        };
        $.post('/setup', data, function(json) {
            if (json.error) {
                helper.text(json.error);
                button.find('i').hide();
                button.find('span').text('Instellen');
                return;
            }
            document.location.href = '/';
        });
    });
});

let nextColon = true;
let monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];
let days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

function updateTime() {
    let date = new Date();
    let colon = (nextColon = !nextColon) ? ':' : ' ';
    let time = pad(date.getHours()) + colon + pad(date.getMinutes());
    let day = date.getDate() + ' ' + monthNames[date.getMonth()] + ' ' + date.getFullYear();
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
    let config = {
        apiKey: "AIzaSyBQGAOw3TcQOhHd6ZMnFX8HraBtCsKxB7o",
        authDomain: "smartcities-d2e38.firebaseapp.com",
        databaseURL: "https://smartcities-d2e38.firebaseio.com/",
        storageBucket: "gs://smartcities-d2e38.appspot.com"
    };
    firebase.initializeApp(config);
    let auth = firebase.auth();
    auth.signInWithEmailAndPassword("admin@admin.nl", "adminadmin");
    auth.onAuthStateChanged(function(user) {
        if (user) {
            let db = firebase.database().ref();
            db.child("notifications").child(user.uid).on('value', function (snapshot) {
                snapshot.forEach(function(v) {
                    let object = v.val();
                    console.log(object);
                    for(let i in object.triggers) {
                        let trigger = object.triggers[i];
                        if (trigger.activated) {
                            let message;
                            if (i === 'wind_speed') {
                                message = 'Windkracht ' + object.windPower + ' in de ' + object.windDirection.toLowerCase() + ' richting.';
                            }
                            let type;
                            let icon;
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
        let helper = $('#login-form').find('small');
        helper.text('');
        let button = $('#login-form').find('button');
        button.find('i').show();
        button.find('span').text('');
        let data = {
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
        let menu = $(this).next();
        let hidden = menu.css('display') === 'none';
        if (hidden) {
            menu.show();
        } else {
            menu.hide();
        }
    });
    let popup = $('#sensor-popup');
    $('#settings-rooms').find('.mobile-list').on('click', 'li a', function() {
        let id = parseInt($(this).parent().attr('value'));
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
    $('#settings-ice').on('click', 'li > a', function() {
        user_data.contact = parseInt($(this).parent().attr('value'));
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
        let id = $(this).attr('id').replace('#', '');
        console.log('switching to page=' + id);
        switch(id) {
            case 'home':
                let city = 'Amersfoort';
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
                    let list = $('#settings-rooms').find('.mobile-list');
                    list.empty();
                    for(let i in json) {
                        let room = json[i];
                        let item = $('<li value="' + room.id + '"><a href="#settings-room" data-transition="slide"><i class="fa fa-bed"></i>' + room.name + '</a></li>');
                        list.append(item);
                    }
                    user_data.rooms = json;
                    list.listview('refresh');
                });
                break;
            case 'settings-room':
                $.get('/api/rooms/' + user_data.room + '/devices', function(json) {
                    let list = $('#sensors');
                    list.empty();
                    for(let i in json) {
                        let sensor = json[i];
                        let status = sensor.status === 1 ? 'active' : 'inactive';
                        let item = $('<li value="' + sensor.id + '"><a data-transition="slide"><i class="fa fa-plug sensor-' + status + '"></i><span>' + sensor.name + '</span></a><input type="checkbox" data-role="flipswitch"' + (sensor.status === 1 ? ' checked=""' : '') + '></li>');
                        list.append(item);
                        item.find('input').flipswitch();
                        item.find('input').change(function() {
                            let input = $(this);
                            let value = input.is(':checked');
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
            case 'settings-ice':
                $.get('/api/ice', function(json) {
                    let list = $('#settings-ice').find('.mobile-list');
                    list.empty();
                    for(let i in json) {
                        let contact = json[i];
                        list.append('<li value="' + contact.id + '"><a href="#ice-contact" data-transition="slide"><i class="fa fa-address-book"></i>' + contact.name + '</a></li>');
                    }
                    list.listview('refresh');
                });
                break;
            case 'ice-contact':
                $.get('/api/ice/' + user_data.contact, function(contact) {
                    let form = $('#ice-contact-form');
                    form.find('input[name="name"]').val(contact.name);
                    form.find('input[name="email"]').val(contact.email);
                    form.find('input[name="phone_number"]').val(contact.phone_number);
                });
                break;
        }
    });
    $('#ice-contact-form').submit(function(e) {
        console.log('hihi');
        let form = $('#ice-contact-form');
        e.preventDefault();
        let data = {
            name: form.find('input[name="name"]').val(),
            email: form.find('input[name="email"]').val(),
            phone_number: form.find('input[name="phone_number"]').val(),
        };
        $.post('/api/ice/' + user_data.contact, data, function(json) {
            if (json.error) {

            } else {
                $('#ice-contact').find('.back-button').click();
            }
        });
    });
}

$(document).on('pageshow', '#new-devices-dialog', () => { 
    // Execute every 4 secondes for a total of 5 times.
    function call(limit, callback) {
        let i = 0;
        let call = setInterval(() => {

            var roomsPromise = $.get('/api/rooms');
            var devicesPromise = $.get('/api/devices/new');
            
            $.when(roomsPromise, devicesPromise)
            .done((rooms, devices) => {

                let roomsSelect = '';
                for(let room of rooms[0]) {
                    roomsSelect += `<option value=${room.id}>${room.name}</option>\n`;
                }

                for(let device of devices[0]){
                    $("#device-list").append(
                        `<div class="device">
                            <i class="fa fa-cube"></i>
                            <b>Water Sensor</b>
                            <p>id: ${device['id']}</p>
                            <form id="form-device-${device['id']}">
                                <select class="room-selector ui-btn ui-icon-carat-d ui-btn-icon-right ui-corner-all ui-shadow">
                                    <option value="" selected disabled>Selecteer een kamer.</option>
                                    ${roomsSelect}
                                </select>
                                <input type="submit" class="room-save  ui-btn ui-shadow ui-corner-all" value="save"/>
                            </form>
                            <hr />
                        </div>`
                    )

                    $(`#form-device-${device['id']}`).submit(e => {
                        e.preventDefault();

                        const value = $(`#form-device-${device['id']}`).children('select').val();

                        if(value != null){
                            $.ajax({
                                url: `/api/rooms/${value}/devices/${device['id']}`,
                                type: 'PUT',
                                data: {
                                    rooms_id: value
                                }
                            }).done( () => {
                                refresh();
                            });
                        }
                    });
                }

                $("#loading").hide();
                clearInterval(call);
                callback('Done');
            });
            if (i === limit - 1) {
                $("#loading").hide();
                clearInterval(call);
                callback('Failed');
            }

            i++;
        }, 4000);
    }

    function refresh(){
        $('#device-list').empty();
        $("#loading").show();
        call(5, (status) => {
            console.log(status);

            if (!$.trim($('#device-list').html())){
                $('#device-list').append(
                    '<p style="text-align: center;">Geen sensoren gevonden.</p>'
                );
            }
        });
    }
    
    $('#devices-refresh').click(e => {
        e.preventDefault();
        refresh();
    });

    refresh();
});