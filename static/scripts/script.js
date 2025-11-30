// const { createElement } = require("react");

document.addEventListener('contextmenu', event => event.preventDefault())

// websocket
const socket = io({ transports: ['websocket']});
document.getElementById('btn_send').addEventListener('click', () => {
    console.log('btn_send')
    const message = document.getElementById('resizeTextarea').value;
    if (message) {
        console.log(message)
        socket.emit('message', message);
        let reply_msg = document.getElementById("reply_msg");
        console.log('reply_msg: ', reply_msg);
        var reply_msg_id = reply_msg.dataset.messageId;
        console.log('reply_msg_id: ', reply_msg_id);

        fetch('/message', {
            method: 'POST',
            headers: {
                // 'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                msg: message,
                reply_id: reply_msg_id
            }),
            // body: new URLSearchParams({ message }),
        })
        .then((response) => {
            if (!response.ok) {
                console.error('Failed to send message through HTTP:', response.statusText);
            }
        })
        .catch((error) => {
            console.error('HTTP error:', error);
        });
        document.getElementById('resizeTextarea').value = ''; 
        console.log('Message: ', message)
        
    } 
});

socket.on('/message', (msg) => {
    window.location.reload();
    console.log('message')
    // console.log('MSG: ', msg);
});

socket.on('edit_message', () => {
    window.location.reload();
    console.log('edit_message')
    // console.log("msg: ", msg)
});

socket.on('chat_action', () => {
    window.location.reload();
    console.log('chat_action')
});

socket.on('new_message', () => {
    window.location.reload();
    console.log('new_message')
})


// more
var side_panel_displayed = false;
const panel = document.getElementById("panel");
const btn_panel = document.getElementById("btn_panel"); 
function display_side_panel(){
    if (side_panel_displayed){
        side_panel_displayed = false;
        panel.style.display = "none";
    }
    else{
        side_panel_displayed = true;
        panel.style.display = "flex";
    }
}
document.addEventListener("click", function(event) {
    if (!panel.contains(event.target) && !btn_panel.contains(event.target)) {
        panel.style.display = "none";
        side_panel_displayed = false;   
    }
});

// setting
var setting_panel_displayed = false;
function display_setting_panel(){
    if (setting_panel_displayed){
        setting_panel_displayed = false;
        setting_panel.style.display = "none";
    }
    else{
        setting_panel_displayed = true;
        setting_panel.style.display = "flex";
    }
}
document.addEventListener("click", function(event) {
    if (setting_panel_displayed && !setting_panel.contains(event.target) && !btn_panel_dots.contains(event.target)) {
        setting_panel.style.display = "none";
        setting_panel_displayed = false;
    }
});


// copy text
function copy_text(target) {
    if (target == 'name'){
        var elementToCopy = document.getElementById(target);
    }
    else if (target == 'username'){
        var elementToCopy = document.getElementById(target);
    }
    else if (target == 'bday'){
        var elementToCopy = document.getElementById(target);
    }
    else if (target == 'bio'){
        var elementToCopy = document.getElementById(target);
    }

    var copyText = elementToCopy.innerText;
    navigator.clipboard.writeText(copyText)
    message_copying(target)
    console.log("Text: ", copyText)
}
function message_copying(target) {
    message_copy = document.getElementById("message_copy");
    message_copy.style.display = "flex";
    document.getElementById("msg_target").innerHTML = target;
    setTimeout(2500);
    setting_panel.style.display = "none";
}

// textarea
const textarea = document.getElementById('resizeTextarea');
if (textarea){
textarea.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
});
}

// plus panel
var side_plus_panel_displayed = false;
const plus_panel = document.getElementById("plus_panel");
const btn_plus_panel = document.getElementById("btn_plus_panel"); 
function display_side_plus_panel(){
    if (side_plus_panel_displayed){
        side_plus_panel_displayed = false;
        plus_panel.style.display = "none";
    }
    else{
        side_plus_panel_displayed = true;
        plus_panel.style.display = "flex";
    }
}
document.addEventListener("click", function(event) {
    if (!plus_panel.contains(event.target) && !btn_plus_panel.contains(event.target)) {
        plus_panel.style.display = "none";
        side_plus_panel_displayed = false;
    }
});


// panel create group
var side_create_panel_displayed = false;
const create_panel = document.getElementById("panel_create_group");
const btn_create_panel = document.getElementById("btn_panel_create_group"); 
function display_side_create_panel(){
    if (side_create_panel_displayed){
        side_create_panel_displayed = false;
        create_panel.style.display = "none";
    }
    else{
        side_create_panel_displayed = true;
        create_panel.style.display = "flex";
        plus_panel.style.display = "none";
        side_plus_panel_displayed = false;
    }
}
document.addEventListener("click", function(event) {
    if (!create_panel.contains(event.target) && !btn_create_panel.contains(event.target)) {
        create_panel.style.display = "none";
        side_create_panel_displayed = false;
    }
});


// panel join group
var side_join_panel_displayed = false;
const join_panel = document.getElementById("panel_join_group");
const btn_join_panel = document.getElementById("btn_panel_join_group"); 
function display_side_join_panel(){
    if (side_join_panel_displayed){
        side_join_panel_displayed = false;
        join_panel.style.display = "none";
    }
    else{
        side_join_panel_displayed = true;
        join_panel.style.display = "flex";
        plus_panel.style.display = "none";
        side_plus_panel_displayed = false;
    }
}
document.addEventListener("click", function(event) {
    if (!join_panel.contains(event.target) && !btn_join_panel.contains(event.target)) {
        join_panel.style.display = "none";
        side_join_panel_displayed = false;
    }
});


// panel create chat
var side_create_chat_displayed = false;
var create_chat = document.getElementById("panel_create_chat");
var btn_create_chat = document.getElementById("btn_panel_create_chat"); 
function display_side_create_chat(){
    if (side_create_chat_displayed){
        side_create_chat_displayed = false;
        create_chat.style.display = "none";
    }
    else{
        side_create_chat_displayed = true;
        create_chat.style.display = "flex";
        plus_panel.style.display = "none";
        side_plus_panel_displayed = false;
    }
}
document.addEventListener("click", function(event) {
    if (!create_chat.contains(event.target) && !btn_create_chat.contains(event.target)) {
        create_chat.style.display = "none";
        side_create_chat_displayed = false;
    }
});

async function copyCode(){
    try {
        const response = await fetch('/copy_inv_code');
        if (!response.ok) {
            throw new Error('Ошибка при загрузке чата');
        }
        const code = await response.text(); 
        navigator.clipboard.writeText(code)
            .then(() => {
                console.log('Code: ' + code);
                alert('The code has been copied\n Code to join: ' + code);
            })
            .catch(err => {
                console.error('Error: ', err);
                alert('Error');
            });
    } catch (error) {
        console.error('Ошибка:', error);
        chat_list.innerHTML = `<p>${error}</p>`;
    }
}


// display_chat_menu
var side_chat_menu_displayed = false;
const btn_chat_menu = document.getElementById("btn_chat_menu"); 
function display_chat_menu(){
    let chat_menu = document.getElementById("chat_menu");
    if (side_chat_menu_displayed){
        side_chat_menu_displayed = false;
        chat_menu.style.display = "none";
    }
    else{
        side_chat_menu_displayed = true;
        // console.log(chat_menu)
        chat_menu.style.display = "flex";
    }
}
document.addEventListener("click", function(event) {
    if (side_chat_menu_displayed && !chat_menu.contains(event.target) && !btn_chat_menu.contains(event.target)) {
        chat_menu.style.display = "none";
        side_chat_menu_displayed = false;
    }
});

// Update
document.addEventListener('DOMContentLoaded', function () {
    let chat_header = document.getElementById('chat_header'); 
    let messages = document.getElementById('messages'); 
    let chat_list = document.getElementById('chat_list');
    let members_list = document.getElementById('members_list'); 
    const setting_panel = document.getElementById("setting_panel");
    const btn_panel_dots = document.getElementById("btn_panel_dots"); 

    
    if (chat_header) {UpdateChatHeader();}
    if (messages) {UpdateChatMessages();}
    if (chat_list) {UpdateChatList();}
    if (members_list) {UpdateMembersList();}

});


// Update Chat List
async function UpdateChatList(){
    let chat_list = document.getElementById('chat_list');
    try {
        const response = await fetch('/upd_chat_list');
        if (!response.ok) {
            throw new Error('Ошибка при загрузке чата листа');
        }
        const data = await response.text(); 
        chat_list.innerHTML = data;
    } catch (error) {
        console.error('Ошибка:', error);
        chat_list.innerHTML = `<p>${error}</p>`;
    }
}

// Update Chat Messages
async function UpdateChatMessages(){
    let messages = document.getElementById('messages');
    try {
        const response = await fetch('/upd_chat_messages');
        if (!response.ok) {
            throw new Error('Ошибка при загрузке сообщений');
        }
        const data = await response.text(); 
        messages.innerHTML = data;
        // messages.scrollTop = messages.scrollHeight;
    } catch (error) {
        console.error('Ошибка:', error);
        messages.innerHTML = `<p>${error}</p>`;
    }
}

// Update Chat Header
async function UpdateChatHeader(){
    let chat_header = document.getElementById('chat_header');
    try {
        const response = await fetch('/upd_chat_header');
        if (!response.ok) {
            throw new Error('Ошибка при загрузке заголовка');
        }
        const data = await response.text(); 
        chat_header.innerHTML = data;
    } catch (error) {
        console.error('Ошибка:', error);
        chat_header.innerHTML = `<p>${error}</p>`;
    }
}

// search chat
const search_chat = document.getElementById('search_chat');
if (search_chat){
    search_chat.addEventListener('input', async () => {
        let input_chat = search_chat.value;
        let names_chats = []
        let chats = document.getElementsByClassName('body-element')
        for (const i of chats){
            let chat_name = i.querySelector(".chat-list-body-element-name")
            let chat_id = i.id;
            let name = chat_name.innerText;
            names_chats.push({[chat_id]: name})
        }
        for (let i=0; i<names_chats.length; i++){
            const [[key, value]] = Object.entries(names_chats[i]);
            if (!value.toLowerCase().includes(input_chat.toLowerCase())){
                document.getElementById(key).style.display = "none";
            }
            else if (value.toLowerCase().includes(input_chat.toLowerCase())){
                document.getElementById(key).style.display = "flex";
            }
        }
    })
}


//display search message
var side_search_msg_displayed = false;
const btn_display_search_msg = document.getElementById('btn_display_search_msg');
function display_search_msg(){
    var search_msg = document.getElementById('search_msg');
    // console.log('search_msg: ', search_msg)
    if (side_search_msg_displayed){
        side_search_msg_displayed = false;
        search_msg.style.display = "none";
    }
    else {
        side_search_msg_displayed = true;
        search_msg.style.display = "flex";

        var all_blocks_dates = document.getElementsByClassName('date');
        // console.log('all_blocks_dates: ', all_blocks_dates);
        var blocks_dates = {};
        for (const i of all_blocks_dates){
            let date = i.id;
            let all_msges = i.getElementsByClassName('message');
            let msges = {};
            for (const j of all_msges){
                let msg = j.querySelector(".message-body-text");
                let txt_msg = msg.innerText;
                let msg_id = j.dataset.messageId;
                let name = j.dataset.username;
                let avatar = j.dataset.username;
                let time = j.querySelector(".message-body-date");
                let txt_time = time.innerText;
                // console.log('msg_id: ', msg_id, 'txt_msg: ', txt_msg);
                msges[msg_id] = [txt_msg, name, avatar, txt_time];
            }
            // console.log('date: ', date, 'msges: ', msges);
            blocks_dates[date] = msges;
        }
        // console.log('blocks_dates: ', blocks_dates);

        var input_msg = document.getElementById('input_msg');
        input_msg.addEventListener('input', async () => {
            let msg = input_msg.value;
            // console.log('blocks_dates: ', blocks_dates);
            var msges_area = document.getElementsByClassName('msges_area')[0];
            msges_area.innerHTML = '';
            for (let [date, messages] of Object.entries(blocks_dates)) {
                // console.log('Date: ', date, 'Messages: ', messages);
                for (let [msg_id, msg_inf] of Object.entries(messages)) {
                    // console.log('MSGINF: ', msg_inf)
                    let txt = msg_inf[0];
                    let name = msg_inf[1];
                    let avatar = msg_inf[2];
                    let time = msg_inf[3];
                    if (txt.toLowerCase().includes(msg.toLowerCase())){
                        // console.log('Date: ', date, 'Id: ', msg_id, 'Txt: ', txt, 'Name: ', name, 'Avatar: ', avatar, 'Time: ', time);

                        // searched_msg
                        const elem = document.createElement('a');
                        elem.classList.add('searched_msg');
                        elem.setAttribute('id', `search_${msg_id}`);
                        elem.addEventListener("click", () => {
                            // console.log('move');
                            let message_id = document.querySelector(`[data-message-id="${msg_id}"]`);
                            // console.log('msg_id: ', msg_id);
                            // console.log('message_id: ', message_id);
                            message_id.scrollIntoView({
                                behavior: "smooth",
                                block: "center"
                            });
                            const oldColor = message_id.style.backgroundColor;
                            message_id.style.transition = "background-color 0.5s ease";
                            message_id.style.backgroundColor = "lightgray";
                            setTimeout(() => {
                                message_id.style.backgroundColor = oldColor;
                            }, 500);
                        });
 
                        msges_area.appendChild(elem);

                        // avatar
                        let msg_avatar = document.createElement('div');
                        msg_avatar.classList.add('msg_avatar');
                        elem.appendChild(msg_avatar);

                        let avatar_img = document.createElement('img');
                        avatar_img.classList.add('avatar_img');
                        avatar_img.setAttribute('src', `../static/images/avatars/${avatar}.jpg`);
                        msg_avatar.appendChild(avatar_img);

                        // name msg
                        let name_msg = document.createElement('div');
                        name_msg.classList.add('name_msg');
                        elem.appendChild(name_msg);

                        let name_txt = document.createElement('p');
                        name_txt.classList.add('name_txt');
                        name_txt.innerHTML = name;
                        name_msg.appendChild(name_txt);

                        let msg_txt = document.createElement('p');
                        msg_txt.classList.add('msg_txt');
                        const replaced = txt.replace(new RegExp(msg, "g"), `<b style='background-color: rgba(255, 255, 255, 0.32);'>${msg}</b>`);
                        msg_txt.innerHTML = replaced;
                        name_msg.appendChild(msg_txt);

                        // date
                        let msg_date = document.createElement('div');
                        msg_date.classList.add('msg_date');
                        elem.appendChild(msg_date);

                        let date_txt = document.createElement('p');
                        date_txt.classList.add('date_txt');
                        date_txt.innerHTML = date;
                        msg_date.appendChild(date_txt);
                        
                        let time_txt = document.createElement('p');
                        time_txt.classList.add('date_txt');
                        time_txt.innerHTML = time;
                        msg_date.appendChild(time_txt);
                    }
                }
            }
        })
    }
}
document.addEventListener("click", function(event) {
    if (side_search_msg_displayed && !search_msg.contains(event.target) && !btn_display_search_msg.contains(event.target)) {
        search_msg.style.display = "none";
        side_search_msg_displayed = false;
    }
});

function ScrollToReplyMsg(msg_id){
    // console.log(msg_id)
    msg = document.querySelector(`[data-message-id="${msg_id}"]`);
    // console.log("msg: ", msg);
    msg.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
    const oldColor = msg.style.backgroundColor;
    msg.style.transition = "background-color 1s ease";
    msg.style.backgroundColor = "gray";
    setTimeout(() => {
        msg.style.backgroundColor = oldColor;
    }, 500);
}

function OpenChatPreview(sender){
    console.log('sender: ', sender);
    fetch(`/open_forwarded_profile/${sender}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    })
    .then((response) => {
        if (!response.ok) {
            console.error('Failed to send id through HTTP:', response.statusText);
        }
        location.reload();
    })
    .catch((error) => {
        console.error('HTTP error:', error);
    });
}

// right click message panel
let currentMessageId = null;
const messagePanel_user = document.getElementById("message_panel_user");
const messagePanel_friend = document.getElementById("message_panel_friend");
const messagePanel_user_forwarded = document.getElementById("message_panel_user_forwarded");
var messageElement_user = null;

function positionPanel(panel, event) {
    const panelRect = panel.getBoundingClientRect();
    const viewportHeight = window.innerHeight;
    const viewportWidth = window.innerWidth;
    
    const footer = document.querySelector('.chat-footer');
    const footerRect = footer ? footer.getBoundingClientRect() : null;
    const footerTop = footerRect ? footerRect.top : viewportHeight;

    let x = Math.min(event.clientX, viewportWidth - panelRect.width - 5);
    
    let y;
    const spaceBelow = footerTop - (event.clientY + panelRect.height + 10);
    const spaceAbove = event.clientY - panelRect.height - 10;

    if (spaceBelow < 0 && spaceAbove >= 0) {
        y = Math.max(event.clientY - panelRect.height - 5, 5);
    } else if (spaceBelow >= 0) {
        y = Math.min(event.clientY, viewportHeight - panelRect.height - 5);
    } else {
        y = 5;
    }
    
    panel.style.left = `${x}px`;
    panel.style.top = `${y}px`;
}


// Handler for all messages
document.addEventListener('contextmenu', function(event) {
    messageElement_user = event.target.closest('.message-right');
    if (!messageElement_user) return;
    if (messageElement_user.querySelector('.forward-orig_sender')) {

        event.preventDefault();

        messagePanel_user_forwarded.style.display = "flex";
        messagePanel_user_forwarded.style.position = "absolute";
        positionPanel(messagePanel_user_forwarded, event);
        
    }
    else if (messageElement_user.querySelector('.message-body')) {
        
        event.preventDefault();

        messagePanel_user.style.display = "flex";
        messagePanel_user.style.position = "absolute";
        positionPanel(messagePanel_user, event);

    }
});

var messageElement_friend = null;
document.addEventListener('contextmenu', function(event) {
    messageElement_friend = event.target.closest('.message-left');
    if (!messageElement_friend) return;
    
    event.preventDefault();

    messagePanel_friend.style.display = "flex";
    messagePanel_friend.style.position = "absolute";
    positionPanel(messagePanel_friend, event);

});

// Closing when clicked outside the panel
document.addEventListener('click', function(event) {
    if (!messagePanel_user.contains(event.target)) {
        messagePanel_user.style.display = "none";
    }
    if (!messagePanel_friend.contains(event.target)) {
        messagePanel_friend.style.display = "none";
    } 
    if (!messagePanel_user_forwarded.contains(event.target)){
        messagePanel_user_forwarded.style.display = "none";

    }
});

// Handlers for menu buttons
if (messagePanel_user){
    messagePanel_user.addEventListener('click', function(event) {
        const button = event.target.closest('.msg_menu-btn');
        if (!button) return;
        
        const action = button.dataset.action;
        console.log('action: ', action)
        console.log('msg: ', messageElement_user)
        executeMenuAction(action, messageElement_user);
        messagePanel_user.style.display = "none";
    });
    
    // Closing when the cursor leaves
    messagePanel_user.addEventListener('mouseleave', function() {
        messagePanel_user.style.display = "none";
    });
}

if (messagePanel_user_forwarded){
    messagePanel_user_forwarded.addEventListener('click', function(event) {
        const button = event.target.closest('.msg_menu-btn');
        if (!button) return;
        
        const action = button.dataset.action;
        console.log('action: ', action)
        console.log('msg: ', messageElement_user)
        executeMenuAction(action, messageElement_user);
        messagePanel_user_forwarded.style.display = "none";
    });
    
    // Closing when the cursor leaves
    messagePanel_user_forwarded.addEventListener('mouseleave', function() {
        messagePanel_user_forwarded.style.display = "none";
    });
}

if (messagePanel_friend){
    messagePanel_friend.addEventListener('click', function(event) {
        const button = event.target.closest('.msg_menu-btn');
        if (!button) return;
        
        const action = button.dataset.action;
        executeMenuAction(action, messageElement_friend);
        messagePanel_friend.style.display = "none";
    });
    
    // Closing when the cursor leaves
    messagePanel_friend.addEventListener('mouseleave', function() {
        messagePanel_friend.style.display = "none";
    });
}


// Action functions
function executeMenuAction(action, msg) {
    console.log('act: ', action)
    console.log('msg: ', msg)
    let msg_txt = msg.getElementsByClassName('message-body-text')[0].innerText;
    let msg_id = msg.dataset.messageId
    let msg_username = msg.dataset.username
    switch(action) {
        case 'copy':
            navigator.clipboard.writeText(msg_txt);
            break;
        case 'reply':
            replyMessage(msg_txt, msg_username, msg_id);
            break;
        case 'forward':
            forwardMessage(msg_txt, msg_username);
            break;
        case 'edit':
            editMessage(msg_txt, msg_id);
            break;
        case 'delete':
            deleteMessage(msg_id);
            break;
    }
}

function replyMessage(msg_txt, msg_username, msg_id) { 
    console.log('reply');
    display_reply_box(msg_txt, msg_username, msg_id);
}
let forwardMessageData = null;
function forwardMessage(msg_txt, msg_username) { 
    console.log('forward');
    forwardMessageData = {
        text: msg_txt,
        username: msg_username
    };
    display_forward_box();
}

function editMessage(msg_txt, id) { 
    // console.log(msg_txt, id);
    textarea.innerHTML = msg_txt;
    display_edit_box(msg_txt, id);
}

const btn_edit = document.getElementById("btn_edit");
var edit = document.getElementById("edit");
btn_edit.addEventListener("click", function() {
    let msg = textarea.value;
    let msg_id = edit.dataset.messageId;
    // console.log('msg: ', msg);
    // console.log('msg_id: ', msg_id);
    fetch(`/edit_msg`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: msg_id,
            text: msg
        }),
    })
    .then((response) => {
        if (!response.ok) {
            console.error('Failed to send id through HTTP:', response.statusText);
        }
    })
    .catch((error) => {
        console.error('HTTP error:', error);
    });
    
})


function deleteMessage(id) {
    fetch(`/delete_msg/${id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    })
    .then((response) => {
        if (!response.ok) {
            console.error('Failed to send id through HTTP:', response.statusText);
        }
        location.reload();
    })
    .catch((error) => {
        console.error('HTTP error:', error);
    });

}


// display reply box
var side_reply_box_displayed = false;
const btn_close_reply = document.getElementById("close_reply");
let reply = document.getElementById("reply");

function display_reply_box(msg_txt, msg_username, msg_id){
    var footer_block_menu = document.getElementsByClassName('chat-footer-block_menu')[0]
    console.log('reply: ', footer_block_menu);
    if (side_reply_box_displayed){
        side_reply_box_displayed = false;
        footer_block_menu.style.display = "none";
        reply.style.display = "none";
    }
    else if (!side_edit_box_displayed){
        side_reply_box_displayed = true;
        footer_block_menu.style.display = "flex";
        reply.style.display = "inline-flex";
        reply_friend = document.getElementById("reply_friend");
        let reply_msg = document.getElementById("reply_msg");
        reply_msg.innerHTML = msg_txt;
        reply_msg.dataset.messageId = msg_id;
        friend_name = msg_username;
        // console.log('friend_name: ', friend_name);
        reply_friend.innerHTML = `Reply to ${friend_name}`;
    }
}
btn_close_reply.addEventListener("click", function() {
    reply.style.display = "none";
    footer_block_menu.style.display = "none";
    side_reply_box_displayed = false;
});
document.addEventListener("click", function(event) {
    if (side_reply_box_displayed && !reply.contains(event.target) && btn_close_reply.contains(event.target)) {
        reply.style.display = "none";
        footer_block_menu.style.display = "none";
        side_reply_box_displayed = false;
    }
});

// reply cont
async function fill_in_reply_cont(){
    let messages = document.getElementsByClassName('message')
    // console.log('messages: ', messages);
    // console.log('messages.length: ', messages.length);
    for (let msg of messages){
        var msg_id = msg.dataset.messageId;
        var reply_cont = document.getElementsByClassName('reply_cont');

        for (let reply of reply_cont){
            if (msg_id == reply.dataset.messageId){
                var reply_txt = document.getElementById('reply_txt_${{ msg_id }}');
                // console.log('reply_txt: ', reply_txt);
                var reply_friend = document.getElementById('reply_friend_${{ msg_id }}');
                // console.log('reply_friend: ', reply_friend);
                reply_friend.innerHTML = msg.dataset.username;
                reply_txt.innerHTML = msg.getElementsByClassName('message-body-text')[0].innerText;
            }
        }
    }
}


// display forward box
var side_forward_box_displayed = false;
var forward = document.getElementById("forward");
const btn_close_forward = document.getElementById("close_forward");
function display_forward_box(){
    if (side_forward_box_displayed){
        side_forward_box_displayed = false;
        forward.style.display = "none";
        forwardMessageData = null;
    }
    else{
        side_forward_box_displayed = true;
        forward.style.display = "flex";
        UpdateChatListForward();
    }
}
btn_close_forward.addEventListener("click", function() {
    forward.style.display = "none";
    side_forward_box_displayed = false;
});
document.addEventListener("click", function(event) {
    if (side_forward_box_displayed && !forward.contains(event.target) && btn_close_forward.contains(event.target)) {
        forward.style.display = "none";
        side_forward_box_displayed = false;
    }
});

// Update Chat List Forward
async function UpdateChatListForward(){
    let list_forward = document.getElementById('list_forward');
    // console.log("list: ", forward);
    try {
        const response = await fetch('/upd_chat_list_forward');
        if (!response.ok) {
            throw new Error('Ошибка при загрузке чата листа');
        }
        const data = await response.text(); 
        list_forward.innerHTML = data;
    
        // Инициализируем чекбоксы после загрузки, передавая текущие данные
        setTimeout(() => initializeForwardCheckboxes(forwardMessageData), 100);
        console.log("DATA loaded successfully");
    } catch (error) {
        console.error('Ошибка:', error);
        list_forward.innerHTML = `<p>${error}</p>`;
    }
}


// search chat forward
const input_forward = document.getElementById('input_forward');
if (input_forward){
    input_forward.addEventListener('input', async () => {
        let input_chat = input_forward.value;
        let names_chats = [];
        let chats = document.getElementsByClassName('body-element_fw');
        console.log("chats: ", chats);
        
        for (const i of chats){
            let chat_name = i.querySelector(".chat-list-body-element-name_fw");
            console.log('chat_name: ', chat_name);
            let chat_id = i.id;
            let name = chat_name.innerText;
            names_chats.push({[chat_id]: name});
        }
        console.log("names_chats: ", names_chats);
        for (let i=0; i<names_chats.length; i++){
            const [[key, value]] = Object.entries(names_chats[i]);
            if (!value.toLowerCase().includes(input_chat.toLowerCase())){
                document.getElementById(key).style.display = "none";
            }
            else if (value.toLowerCase().includes(input_chat.toLowerCase())){
                document.getElementById(key).style.display = "flex";
            }
        }
    })
}

// display edit box
var side_edit_box_displayed = false;
const btn_close_edit = document.getElementById("close_edit");
const btn_send = document.getElementById("btn_send");


function display_edit_box(msg_txt, id){
    var footer_block_menu = document.getElementsByClassName('chat-footer-block_menu')[0]
    console.log('edit: ', footer_block_menu)
    if (side_edit_box_displayed){
        side_edit_box_displayed = false;
        footer_block_menu.style.display = "none";
        edit.style.display = "none";
        btn_send.style.display = "flex";
        btn_edit.style.display = "none";
    }
    else if (!side_reply_box_displayed){
        side_edit_box_displayed = true;
        footer_block_menu.style.display = "flex";
        edit.style.display = "inline-flex";
        console.log("ID: ", id);
        edit.dataset.messageId = id;
        console.log("message_id: ", edit.dataset.messageId);
        btn_send.style.display = "none";
        btn_edit.style.display = "flex";
        edit_msg = document.getElementById("edit_msg");
        edit_msg.innerHTML = msg_txt;
    }
}
btn_close_edit.addEventListener("click", function() {
    side_edit_box_displayed = false;
    footer_block_menu.style.display = "none";
    edit.style.display = "none";
    btn_send.style.display = "flex";
    btn_edit.style.display = "none";
    textarea.innerHTML = "";
});
document.addEventListener("click", function(event) {
    if (side_edit_box_displayed && !edit.contains(event.target) && btn_close_edit.contains(event.target)) {
        side_edit_box_displayed = false;
        footer_block_menu.style.display = "none";
        edit.style.display = "none";
        btn_send.style.display = "flex";
        btn_edit.style.display = "none";
    }
});

// made block reply
const container = document.getElementById("messages");
const observer = new MutationObserver(() => {
    const messages = container.getElementsByClassName("message");
    
    for (let msg of messages){
        var msg_id = msg.dataset.messageId;
        var username = msg.dataset.username;
        // console.log('Elements:', msg.getElementsByClassName('message-body-text'));
        if (msg.getElementsByClassName('message-body-text')){
            var txt = msg.getElementsByClassName('message-body-text')[0].innerText;
            
            const reply_elements = document.querySelectorAll(`[data-message-id="${msg_id}"]`);
            
            if (reply_elements.length > 1){
                for (let i=1; i<reply_elements.length; i++){
                    let reply_friend = document.createElement('p');
                    let reply_txt = document.createElement('p');
                    reply_friend.innerText = username;
                    reply_txt.innerText = txt;
                    reply_elements[i].appendChild(reply_friend);
                    reply_elements[i].appendChild(reply_txt);
                }
            }
        }
    }
    msges = document.getElementById('messages');
    msges.scrollTop = msges.scrollHeight;
});
 
observer.observe(container, { childList: true});


// Иницилизация чек боксов
function initializeForwardCheckboxes(messageData) {
    const checkboxes = document.querySelectorAll('.chat-checkbox');
    const sendBtn = document.getElementById('send_forward_btn');
    
    // Сбрасываем предыдущее состояние
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
        const chatElement = checkbox.closest('.body-element_fw');
        chatElement.classList.remove('selected');
    });
    sendBtn.style.display = 'none';
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const chatElement = this.closest('.body-element_fw');
            if (this.checked) {
                chatElement.classList.add('selected');
            } else {
                chatElement.classList.remove('selected');
            }
            
            // Показываем/скрываем кнопку отправки
            const selectedChats = document.querySelectorAll('.chat-checkbox:checked');
            sendBtn.style.display = selectedChats.length > 0 ? 'flex' : 'none';
        });
    });
    
    // Обработчик кнопки отправки
    sendBtn.addEventListener('click', function() {
        const selectedChats = document.querySelectorAll('.chat-checkbox:checked');
        const chatIds = Array.from(selectedChats).map(checkbox => checkbox.dataset.chatId);
        
        console.log('Selected chats:', chatIds);
        console.log('Message data:', messageData);
        
        if (chatIds.length > 0 && messageData) {
            sendForwardMessage(chatIds, messageData);
        } else {
            console.error('No chats selected or no message data');
            if (!messageData) {
                console.error('forwardMessageData is null or undefined');
            }
        }
    });
}

// Функция отправки пересланного сообщения
function sendForwardMessage(chatIds, messageData) {
    console.log('Sending forward message to chats:', chatIds);
    console.log('Message data:', messageData);
    
    let successCount = 0;
    let errorCount = 0;
    
    // Отправляем каждому выбранному чату
    const promises = chatIds.map(chatId => {
        return fetch('/forward_msg', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                target_chat_id: chatId,
                orig_sender: messageData.username,
                msg: messageData.text
            }),
        })
        .then(response => {
            if (response.ok || response.redirected) {
                successCount++;
                console.log(`Successfully forwarded to chat ${chatId}`);
                return response.json();
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        })
        .catch(error => {
            console.error('Error forwarding message to chat', chatId, ':', error);
            errorCount++;
            return { error: error.message, chatId: chatId };
        });
    });
    
    // Ждем завершения всех запросов
    Promise.all(promises).then(() => {
        // Закрываем окно пересылки
        const forward = document.getElementById("forward");
        forward.style.display = "none";
        side_forward_box_displayed = false;
        
        forwardMessageData = null;
        
        // Обновляем чат, если нужно
        // UpdateChatMessages();
    });
}