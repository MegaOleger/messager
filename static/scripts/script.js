// const { createElement } = require("react");

document.addEventListener('contextmenu', event => event.preventDefault())

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
const setting_panel = document.getElementById("setting_panel");
const btn_panel_dots = document.getElementById("btn_panel_dots"); 
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
    if (!setting_panel.contains(event.target) && !btn_panel_dots.contains(event.target)) {
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


// websocket
// const socket = io({ transports: ['websocket'], alwaysConnect: true });
// document.getElementById('btn_send').addEventListener('click', () => {
//     const message = document.getElementById('resizeTextarea').value;
//     if (message) {
//         socket.emit('message', message);
//         fetch('/message', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/x-www-form-urlencoded',
//             },
//             body: new URLSearchParams({ message }),
//         })
//         .then((response) => {
//             if (!response.ok) {
//                 console.error('Failed to send message through HTTP:', response.statusText);
//             }
//         })
//         .catch((error) => {
//             console.error('HTTP error:', error);
//         });
//         document.getElementById('resizeTextarea').value = ''; 
//         console.log('Message: ', message)
//     }
// });

// socket.on('new_message', (msg) => {
//     window.location.reload();
//     console.log('MSG: ', msg);
// });

// // chat_state
// socket.on('chat_action', () => {
//     window.location.reload();
//     // console.log('STATE: ', state)
// })

// scroll chat
// const observer = new MutationObserver(mutations => scrollChat);
// const messages = document.getElementById("messages");
// observer.observe(messages, {
//     attributes: true, 
//     childList: true,      
//     characterData: true,
//     subtree: true
// });

// function scrollChat(){
//     let messages = document.getElementById("messages");
//     console.log("1 Scroll True");
//     console.log(messages.scrollHeight);
//     messages.scrollTop = messages.scrollHeight;
//     console.log(messages.scrollHeight);
//     console.log("2 Scroll True");   
// }

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
    if (!chat_menu.contains(event.target) && !btn_chat_menu.contains(event.target)) {
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
        messages.scrollTop = messages.scrollHeight;
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
    if (!search_msg.contains(event.target) && !btn_display_search_msg.contains(event.target)) {
        search_msg.style.display = "none";
        side_search_msg_displayed = false;
    }
});

// right click message panel
let currentMessageId = null;
const messagePanel_user = document.getElementById("message_panel_user");
const messagePanel_friend = document.getElementById("message_panel_friend");

// Handler for all messages
document.addEventListener('contextmenu', function(event) {
    const messageElement_user = event.target.closest('.message-right');
    if (!messageElement_user) return;
    
    event.preventDefault();
    // currentMessageId = messageElement_user.dataset.messageId;
    // const messageBodyText = messageElement_user.querySelector('.message-body-text');
    // var MessageText = messageBodyText ? messageBodyText.innerText : '';
    // console.log('MessageText: ', MessageText)

    // Panel positioning
    var x = Math.min(event.clientX, window.innerWidth - messagePanel_user.offsetWidth - 5);
    var y = Math.min(event.clientY, window.innerHeight - messagePanel_user.offsetHeight - 5);
    
    messagePanel_user.style.display = "flex";
    messagePanel_user.style.left = `${x}px`;
    messagePanel_user.style.top = `${y}px`;
});

document.addEventListener('contextmenu', function(event) {
    const messageElement_friend = event.target.closest('.message-left');
    if (!messageElement_friend) return;
    
    event.preventDefault();
    // currentMessageId = messageElement_friend.dataset.messageId;
    // const messageBodyText = messageElement_friend.querySelector('.message-body-text');
    // var MessageText = messageBodyText ? messageBodyText.innerText : '';
    // console.log('MessageText: ', MessageText)

    // Panel positioning
    var x = Math.min(event.clientX, window.innerWidth - messagePanel_friend.offsetWidth - 5);
    var y = Math.min(event.clientY, window.innerHeight - messagePanel_friend.offsetHeight - 5);
    
    messagePanel_friend.style.display = "flex";
    messagePanel_friend.style.left = `${x}px`;
    messagePanel_friend.style.top = `${y}px`;
});

// Closing when clicked outside the panel
document.addEventListener('click', function(event) {
    if (!messagePanel_user.contains(event.target)) {
        messagePanel_user.style.display = "none";
    }
    if (!messagePanel_friend.contains(event.target)) {
        messagePanel_friend.style.display = "none";
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

if (messagePanel_friend){
    messagePanel_friend.addEventListener('click', function(event) {
        const button = event.target.closest('.msg_menu-btn');
        if (!button) return;
        
        const action = button.dataset.action;
        executeMenuAction(action, messageElement_user);
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
    switch(action) {
        case 'copy':
            console.log('COPY')
            copyMessage(msg);
            break;
        case 'reply':
            replyMessage(msg);
            break;
        case 'forward':
            forwardMessage(msg);
            break;
        case 'edit':
            editMessage(msg);
            break;
        case 'delete':
            deleteMessage(msg);
            break;
    }
    // console.log(`Action: ${action}, Message ID: ${messageId}`);
}

function copyMessage(id) { 
    console.log('COPPPYYY')
    // const messageBodyText = messageElement_user.querySelector('.message-body-text');
    var MessageText = messageBodyText ? messageBodyText.innerText : '';
    console.log('MessageText: ', MessageText)
    navigator.clipboard.writeText(MessageText)
}
function replyMessage(id) { 

}
function forwardMessage(id) { 

}
function editMessage(id) { 
    fetch(`/edit_message/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ id }),
    })
    .then((response) => {
        if (!response.ok) {
            console.error('Failed to send id through HTTP:', response.statusText);
        }
    })
    .catch((error) => {
        console.error('HTTP error:', error);
    });
}
function deleteMessage(id) {
    fetch(`/delete_message/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ id }),
    })
    .then((response) => {
        if (!response.ok) {
            console.error('Failed to send id through HTTP:', response.statusText);
        }
    })
    .catch((error) => {
        console.error('HTTP error:', error);
    });
}
