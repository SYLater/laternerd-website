var socket;
$(document).ready(function () {
    socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + '/chat');

    socket.on('connect', function () {
        socket.emit('joined', {});
    });

    //joined function
    socket.on('status', function (data) {
    });


    //messages
    socket.on('message', function (data) {
        // timestamp
        var momentfnc = moment(data.time);
        var timesent = momentfnc.calendar();
        
        var messageListItem = document.createElement("li");
        messageListItem.id = "chat-messages-" + data.message_id;
        document.getElementById('AllMessagesOL').appendChild(messageListItem);

        var messagecozyMessage = document.createElement("div");
        messagecozyMessage.setAttribute("class", "messagecozyMessage");
        messagecozyMessage.setAttribute("id", "messagecozyMessage-" + data.message_id);
        messagecozyMessage.setAttribute("data-list-item-id", "chat-messages___chat-messages-" + data.message_id);
        messagecozyMessage.setAttribute("role", "article");
        messagecozyMessage.setAttribute("tabindex", "-1");
        messagecozyMessage.setAttribute("aria-setsize", "-1");
        messagecozyMessage.setAttribute("aria-roledescription", "Message");

        document.getElementById('chat-messages-' + data.message_id).appendChild(messagecozyMessage);

        var contents = document.createElement("div");
        contents.setAttribute("class", "contents");
        contents.setAttribute("id", "contents-" + data.message_id);
        document.getElementById("messagecozyMessage-" + data.message_id).appendChild(contents);

        var avatar = document.createElement("img");
        avatar.setAttribute("class", "user-avatar");
        avatar.setAttribute("src", data.icon);
        document.getElementById("contents-" + data.message_id).appendChild(avatar);

        var h2 = document.createElement("h2");
        h2.setAttribute("class", "name-time-header");
        h2.setAttribute("id", "name-time-header-" + data.message_id);
        h2.setAttribute("aria-labelledby", "message-username-" + data.message_id + "-message-timestamp-" + data.message_id);
        document.getElementById("contents-" + data.message_id).appendChild(h2);

        var headerText = document.createElement("span");
        headerText.setAttribute('class', "headerText");
        headerText.setAttribute("id", "message-username-" + data.message_id);
        document.getElementById("name-time-header-" + data.message_id).appendChild(headerText);

        var name = document.createElement("span");
        name.setAttribute("class", "message-username-name");
        name.innerText = data.username;
        document.getElementById("name-time-header-" + data.message_id).appendChild(name);

        var timestamp = document.createElement("span");
        timestamp.setAttribute("class", "timestamp");
        timestamp.setAttribute("id", "timestamp-" + data.message_id);
        document.getElementById("name-time-header-" + data.message_id).appendChild(timestamp);

        var time = document.createElement('time');
        time.setAttribute("id", "message-timestamp-" + data.message_id);
        time.innerText = "" + timesent;
        document.getElementById("timestamp-" + data.message_id).appendChild(time);
        var i = document.createElement("i");
        i.setAttribute("class", "separator");
        i.setAttribute("id", "separator-" + data.message_id);
        document.getElementById("message-timestamp-" + data.message_id).appendChild(i);

        var messagecontent = document.createElement("div");
        messagecontent.setAttribute("class", "messageContent");
        messagecontent.setAttribute("id", "message-content-" + data.message_id);
        messagecontent.innerText = data.msg;
        document.getElementById("contents-" + data.message_id).appendChild(messagecontent);
    });

    socket.on('message', function (data) {
        checkTabFocused();
    });

    $('#text').keypress(function (e) {
        var code = e.keyCode || e.which;
        if (code == 13) {text = $('#text').val();
            $('#text').val('');
            socket.emit('text', { msg: text });}
    });
});


