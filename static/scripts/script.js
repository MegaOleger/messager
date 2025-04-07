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
textarea.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
});


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


// panel invitation code
// var side_inv_code_displayed = false;
// var inv_code = document.getElementById("panel_inv_code");
// var btn_inv_code = document.getElementById("btn_create_group"); 
// function display_side_inv_code(){
//     console.log("panel inv code", inv_code)
//     if (side_inv_code_displayed){
//         side_inv_code_displayed = false;
//         create_inv_code.style.display = "none";
//         console.log('1')
//     }
//     else{
//         side_inv_code_displayed = true;
//         inv_code.style.display = "flex";
//         plus_panel.style.display = "none";
//         side_plus_panel_displayed = false;
//         console.log('2')
//     }
// }
// document.addEventListener("click", function(event) {
//     if (!inv_code.contains(event.target) && !btn_inv_code.contains(event.target)) {
//         inv_code.style.display = "none";
//         side_inv_code_displayed = false;
//     }
// });


// copy code
// var copyBtn = document.getElementById('code');
// copyBtn.addEventListener('click', function(event) {
//     textToCopy = copyBtn.innerText;

//     navigator.clipboard.writeText(textToCopy)
//         .then(() => {
//             console.log('Code: ' + textToCopy);
//             alert('The code has been copied\n Code to join: ' + textToCopy);
//         })
//         .catch(err => {
//             console.error('Error: ', err);
//             alert('Error');
//         });
// });

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


// right click message panel
var side_msg_panel_displayed = false;
const message_panel = document.getElementById("message_panel"); 
const message = document.getElementById("message");
function display_msg_panel(){
    if (side_msg_panel_displayed){
        side_msg_panel_displayed = false;
        message_panel.style.display = "none";
    }
    else{
        side_msg_panel_displayed = true;
        message_panel.style.display = "flex";
    }
}
document.addEventListener('contextmenu', function(event) {
    const x = event.clientX; 
    const y = event.clientY;
    message_panel.style.left = `${x}px`;
    message_panel.style.top = `${y}px`;
});
document.addEventListener("click", function(event) {
    if (!message.contains(event.target) && !message_panel.contains(event.target)) {
        message_panel.style.display = "none";
        side_msg_panel_displayed = false;
    }
});


// websocket
const socket = io({ transports: ['websocket'], alwaysConnect: true });
document.getElementById('btn_send').addEventListener('click', () => {
    const message = document.getElementById('resizeTextarea').value;
    if (message) {
        socket.emit('message', message);
        fetch('/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ message }),
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

socket.on('new_message', (msg) => {
    window.location.reload();
    console.log('MSG: ', msg);
});

// chat_state
socket.on('chat_action', () => {
    window.location.reload();
    // console.log('STATE: ', state)
})

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
        console.log(chat_menu)
        chat_menu.style.display = "flex";
    }
}
document.addEventListener("click", function(event) {
    if (!chat_menu.contains(event.target) && !btn_chat_menu.contains(event.target)) {
        chat_menu.style.display = "none";
        side_chat_menu_displayed = false;
    }
});



// Update Chat List
document.addEventListener('DOMContentLoaded', function () {
    const uniqueElement = document.getElementById('chat_list'); // Укажите id уникального элемента
    if (uniqueElement) {
        UpdateChatList();
    }
});

async function UpdateChatList(){
    let chat_list = document.getElementById('chat_list');
    try {
        const response = await fetch('/upd_chat_list');
        if (!response.ok) {
            throw new Error('Ошибка при загрузке чата');
        }
        const data = await response.text(); 
        chat_list.innerHTML = data;
    } catch (error) {
        console.error('Ошибка:', error);
        chat_list.innerHTML = `<p>${error}</p>`;
    }
}

// Update Chat Messages
document.addEventListener('DOMContentLoaded', function () {
    const uniqueElement = document.getElementById('messages'); 
    if (uniqueElement) {
        UpdateChatMessages();
    }
});

async function UpdateChatMessages(){
    let messages = document.getElementById('messages');
    try {
        const response = await fetch('/upd_chat_messages');
        if (!response.ok) {
            throw new Error('Ошибка при загрузке сообщений');
        }
        const data = await response.text(); // Ожидаем HTML от сервера
        messages.innerHTML = data;
        // await new Promise(resolve => setTimeout(resolve, 1));
        messages.scrollTop = messages.scrollHeight;
        console.log(messages.scrollHeight, messages.clientHeight);
    } catch (error) {
        console.error('Ошибка:', error);
        messages.innerHTML = `<p>${error}</p>`;
    }
    // setTimeout(scrollChat, 1000);
    // requestAnimationFrame(() => {
    //     messages.scrollTop = messages.scrollHeight;
    //     console.log(messages.scrollHeight)
    // });
}


// Update Chat Header
document.addEventListener('DOMContentLoaded', function () {
    const uniqueElement = document.getElementById('chat_header'); 
    if (uniqueElement) {
        UpdateChatHeader();
    }
});

async function UpdateChatHeader(){
    let chat_header = document.getElementById('chat_header');
    try {
        const response = await fetch('/upd_chat_header');
        if (!response.ok) {
            throw new Error('Ошибка при загрузке сообщений');
        }
        const data = await response.text(); // Ожидаем HTML от сервера
        chat_header.innerHTML = data;
    } catch (error) {
        console.error('Ошибка:', error);
        chat_header.innerHTML = `<p>${error}</p>`;
    }
}

// Update members_list
document.addEventListener('DOMContentLoaded', function () {
    const uniqueElement = document.getElementById('members_list'); 
    if (uniqueElement) {
        UpdateMembersList();
    }
});

async function UpdateMembersList(){
    let members_list = document.getElementById('members_list');
    try {
        const response = await fetch('/upd_members_list');
        if (!response.ok) {
            throw new Error('Ошибка при загрузке сообщений');
        }
        const data = await response.text(); // Ожидаем HTML от сервера
        members_list.innerHTML = data;
    } catch (error) {
        console.error('Ошибка:', error);
        members_list.innerHTML = `<p>${error}</p>`;
    }
}