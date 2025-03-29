const btnEncrypt = document.getElementById("btnEncrypt");
const btnDecrypt = document.getElementById("btnDecrypt");
const messageInput = document.getElementById("message");
let encryptedMessage = document.getElementById("encryptedMessage");
const usersList = document.getElementById("usersList");

const chat = document.getElementById("chat");

const publicKey = document.getElementById("publicKey");
const privateKey = document.getElementById("privateKey");

const socket = io();

let users = {}

socket.on("connect", () => {
    console.log(`User Connected - Socket ID: ${socket.id}`);

    socket.on("public_key", (data) => {
        if (data.socket_id !== socket.id) {
            users[data.socket_id] = data.public_key;
        }

        publicKey.value = data.public_key;
        privateKey.value = data.private_key;
    });
});

socket.on("update_users", (userKeys) => {
    users = userKeys;
    usersList.innerHTML = "";

    for (let [id, publicKey] of Object.entries(users)) {
        if (id !== socket.id) {
            let option = document.createElement("option");
            option.value = id;
            option.textContent = `User ${id}`;
            usersList.appendChild(option);
        }
    }
});

btnEncrypt.addEventListener("click", () => {
    const recipientId = usersList.value;

    if (!recipientId) {
        alert("Selecione um usuário para enviar a mensagem!");
        return;
    }

    const data = {
        message: messageInput.value,
        recipient_id: recipientId,
    };

    chat.innerHTML += `
        <div class="border border-black rounded-md p-2.5 mb-2.5">
            <p><b>You (Encrypted):</b> ${messageInput.value}</p>
        </div>
    `;

    socket.emit("encrypt_message", data);
});

socket.on("encrypted_message", (data) => {
    chat.innerHTML += `
        <div class="border border-black rounded-md p-2.5 mb-2.5">
            <p><b>Encrypted:</b> ${data.ciphertext}</p>
        </div>
    `;

    encryptedMessage.value = data.ciphertext;
});

btnDecrypt.addEventListener("click", () => {
    const data = {
        message: encryptedMessage.value,
        privateKey: privateKey.value
    }

    socket.emit("decrypt_message", data);
});

socket.on("decrypted_message", (decryptedMessage) => {
    encryptedMessage.value = decryptedMessage;
});
